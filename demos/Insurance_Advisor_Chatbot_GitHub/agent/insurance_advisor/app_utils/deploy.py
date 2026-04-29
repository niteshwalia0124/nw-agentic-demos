import copy
import datetime
import json
import os
from pathlib import Path
from typing import Any

import vertexai
from google.adk.artifacts import GcsArtifactService
from google.cloud import logging as google_cloud_logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

# Import your existing root agent
from insurance_advisor.agent import root_agent

class AgentEngineApp(AdkApp):
    """ADK Application wrapper for Agent Engine deployment."""

    def set_up(self) -> None:
        """Set up logging and tracing for the agent engine app."""
        super().set_up()
        # Initialize Google Cloud Logging and OpenTelemetry Tracing
        try:
            logging_client = google_cloud_logging.Client()
            self.logger = logging_client.logger(__name__)
        except Exception:
            pass
        
        provider = TracerProvider()
        trace.set_tracer_provider(provider)
        self.enable_tracing = True

    def register_operations(self) -> dict[str, list[str]]:
        """Register available operations for the agent."""
        operations = super().register_operations()
        return operations

    def clone(self) -> "AgentEngineApp":
        template_attributes = self._tmpl_attrs
        return self.__class__(
            agent=copy.deepcopy(template_attributes["agent"]),
            enable_tracing=bool(template_attributes.get("enable_tracing", False)),
            session_service_builder=template_attributes.get("session_service_builder"),
            artifact_service_builder=template_attributes.get("artifact_service_builder"),
            env_vars=template_attributes.get("env_vars"),
        )


def deploy_agent_engine_app() -> agent_engines.AgentEngine:
    print("🚀 Starting Agent Engine deployment...")

    # Step 1: Configure the project and bucket options
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "butterfly-987")
    LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    STAGING_BUCKET = f"{PROJECT_ID}-agent-engine-staging"

    # Step 2: Inject MCP Server URLs & Gemini Key from your active .env
    env_vars = {
        "GOOGLE_API_KEY": os.environ.get("GOOGLE_API_KEY"),
        "CLAIMS_MCP_URL": os.environ.get("CLAIMS_MCP_URL"),
        "COMPLIANCE_MCP_URL": os.environ.get("COMPLIANCE_MCP_URL"),
        "POLICY_MCP_URL": os.environ.get("POLICY_MCP_URL"),
        "RAG_MCP_URL": os.environ.get("RAG_MCP_URL"),
        "RISK_MCP_URL": os.environ.get("RISK_MCP_URL"),
        "NUM_WORKERS": "1",
    }

    # Step 3: Set up the artifacts and logs bucket
    artifacts_bucket_name = f"{PROJECT_ID}-insurance-advisor-logs"

    # Initialize Vertex AI Client
    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
        staging_bucket=f"gs://{STAGING_BUCKET}",
    )

    # Step 4: Specify dependencies to install on the platform
    requirements = [
        "google-adk[eval]",
        "google-cloud-logging",
        "opentelemetry-sdk",
        "google-cloud-firestore"
    ]

    # Step 5: Create the Agent Engine App instance
    agent_engine_app = AgentEngineApp(
        agent=root_agent,
        artifact_service_builder=lambda: GcsArtifactService(
            bucket_name=artifacts_bucket_name
        ),
        env_vars=env_vars
    )

    agent_config = {
        "agent_engine": agent_engine_app,
        "display_name": "insurance-advisor-agent",
        "description": "Insurance Advisor coordinating specialist agents for comprehensive advisory services.",
        "requirements": requirements,
        "env_vars": env_vars,
    }

    # Step 6: Deploy or Update the agent on the Platform
    existing_agents = list(
        agent_engines.list(filter="display_name=insurance-advisor-agent")
    )

    if existing_agents:
        print(f"🔄 Updating existing agent: insurance-advisor-agent")
        remote_agent = existing_agents[0].update(**agent_config)
    else:
        print(f"🆕 Creating new agent on the Platform: insurance-advisor-agent")
        remote_agent = agent_engines.create(**agent_config)

    # Step 7: Save local deployment metadata
    metadata = {
        "remote_agent_engine_id": remote_agent.resource_name,
        "deployment_timestamp": datetime.datetime.now().isoformat(),
        "agent_name": "insurance-advisor-agent",
        "project": PROJECT_ID,
        "location": LOCATION,
    }

    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    metadata_file = logs_dir / "deployment_metadata.json"

    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)

    print("✅ Agent deployed successfully to the platform!")
    print(f"📄 Deployment metadata saved to: {metadata_file}")
    return remote_agent

if __name__ == "__main__":
    deploy_agent_engine_app()
