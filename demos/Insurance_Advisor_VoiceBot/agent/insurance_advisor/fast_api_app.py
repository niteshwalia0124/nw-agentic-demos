# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import google.auth
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from google.adk.cli.fast_api import get_fast_api_app
from google.cloud import logging as google_cloud_logging
from google.adk.agents.live_request_queue import LiveRequestQueue
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.plugins import DebugLoggingPlugin
from insurance_advisor.agent import root_agent


from insurance_advisor.app_utils.telemetry import setup_telemetry
from insurance_advisor.app_utils.typing import Feedback

setup_telemetry()
_, project_id = google.auth.default()
logging_client = google_cloud_logging.Client()
logger = logging_client.logger(__name__)
allow_origins = (
    os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None
)

# Artifact bucket for ADK (created by Terraform, passed via env var)
logs_bucket_name = os.environ.get("LOGS_BUCKET_NAME")

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# In-memory session configuration - no persistent storage
session_service_uri = None

artifact_service_uri = f"gs://{logs_bucket_name}" if logs_bucket_name else None

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
    artifact_service_uri=artifact_service_uri,
    allow_origins=allow_origins,
    session_service_uri=session_service_uri,
    otel_to_cloud=True,
    auto_create_session=True,
)
app.title = "insurance-advisor"
app.description = "API for interacting with the Agent insurance-advisor"


@app.post("/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback.

    Args:
        feedback: The feedback data to log

    Returns:
        Success message
    """
    logger.log_struct(feedback.model_dump(), severity="INFO")
    return {"status": "success"}
session_service = InMemorySessionService()
runner = Runner(app_name="insurance_advisor", agent=root_agent, session_service=session_service)

@app.websocket("/ws/voice/{user_id}/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
    session_id: str,
) -> None:
    """WebSocket endpoint for bidirectional streaming with ADK."""
    logger.log_text(f"WebSocket connection request: user_id={user_id}, session_id={session_id}", severity="INFO")
    await websocket.accept()
    logger.log_text("WebSocket connection accepted", severity="INFO")

    model_name = "gemini-3.1-flash-live-preview"
    
    response_modalities = ["AUDIO"]
    run_config = RunConfig(
        streaming_mode=StreamingMode.BIDI,
        response_modalities=response_modalities,
        input_audio_transcription=types.AudioTranscriptionConfig(),
        output_audio_transcription=types.AudioTranscriptionConfig(),
    )

    # Ensure session exists
    session = await session_service.get_session(
        app_name="insurance_advisor", user_id=user_id, session_id=session_id
    )
    if not session:
        await session_service.create_session(
            app_name="insurance_advisor", user_id=user_id, session_id=session_id
        )

    live_request_queue = LiveRequestQueue()

    async def upstream_task() -> None:
        """Receives messages from WebSocket and sends to LiveRequestQueue."""
        logger.log_text("upstream_task started", severity="DEBUG")
        while True:
            message = await websocket.receive()
            if "bytes" in message:
                audio_data = message["bytes"]
                audio_blob = types.Blob(
                    mime_type="audio/pcm;rate=16000", data=audio_data
                )
                live_request_queue.send_realtime(audio_blob)
            elif "text" in message:
                text_data = message["text"]
                json_message = json.loads(text_data)
                if json_message.get("type") == "text":
                    content = types.Content(
                        parts=[types.Part(text=json_message["text"])]
                    )
                    live_request_queue.send_content(content)
                elif json_message.get("type") == "interruption":
                    logger.log_text("Received interruption signal", severity="INFO")
                    live_request_queue.send_activity_start()
                elif json_message.get("type") == "turn_complete":
                    logger.log_text("Received turn complete signal", severity="INFO")
                    live_request_queue.send_activity_end()

    async def downstream_task() -> None:
        """Receives Events from run_live() and sends to WebSocket."""
        logger.log_text("downstream_task started", severity="DEBUG")
        async for event in runner.run_live(
            user_id=user_id,
            session_id=session_id,
            live_request_queue=live_request_queue,
            run_config=run_config,
        ):
            event_json = event.model_dump_json(exclude_none=True, by_alias=True)
            if "functionCall" in event_json or "function_call" in event_json:
                logger.log_text(f"Tool Call Event: {event_json}", severity="INFO")
            await websocket.send_text(event_json)

    async def keep_alive_task() -> None:
        """Sends a ping to keep connection alive."""
        logger.log_text("keep_alive_task started", severity="DEBUG")
        while True:
            await asyncio.sleep(20)
            try:
                await websocket.send_text(json.dumps({"type": "ping"}))
                logger.log_text("Sent ping", severity="DEBUG")
            except Exception as e:
                logger.log_text(f"Failed to send ping: {e}", severity="DEBUG")
                break

    try:
        await asyncio.gather(upstream_task(), downstream_task(), keep_alive_task())
    except WebSocketDisconnect:
        logger.log_text("Client disconnected normally", severity="INFO")
    except Exception as e:
        logger.log_text(f"Unexpected error in streaming tasks: {e}", severity="ERROR")
    finally:
        logger.log_text("Closing live_request_queue", severity="DEBUG")
        live_request_queue.close()


# Main execution

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
