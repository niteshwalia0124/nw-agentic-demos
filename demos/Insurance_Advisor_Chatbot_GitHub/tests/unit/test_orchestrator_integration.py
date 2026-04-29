import asyncio
import pytest
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from insurance_advisor.agent import root_agent

@pytest.mark.asyncio
async def test_orchestrator_flow():
    session_service = InMemorySessionService()
    user_id = "test_user"
    session_id = "session_1"
    app_name = "insurance_advisor"

    await session_service.create_session(app_name=app_name, user_id=user_id, session_id=session_id)
    runner = Runner(agent=root_agent, app_name=app_name, session_service=session_service)

    print("--- Starting Chat ---")
    
    queries = [
        "Hi, I'm Rajesh Sharma (CUST-1001). Can you tell me what policies I have?",
    ]

    for query in queries:
        print(f"\nUser: {query}")
        msg = types.Content(role="user", parts=[types.Part.from_text(text=query)])
        
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=msg):
            if event.is_final_response():
                if event.content and event.content.parts:
                     # Join all text parts, ignoring function calls in the final output
                     text = "".join([p.text for p in event.content.parts if getattr(p, 'text', None)])
                     if text:
                         print(f"Advisor: {text}\n")
                         assert "Rajesh" in text or "CUST-1001" in text or "policy" in text.lower()
            elif event.author == app_name and event.content and event.content.parts:
                 for part in event.content.parts:
                     if getattr(part, 'text', None):
                         # Print the proactive/thought text
                         print(f"  [Advisor updating you...]: {part.text.strip()}")
                     if getattr(part, 'function_call', None):
                         print(f"  [Orchestrator] Delegating to: {part.function_call.name}")
            elif event.author != "user" and event.author != app_name:
                print(f"  [Internal] {event.author} is processing...")

if __name__ == "__main__":
    asyncio.run(test_orchestrator_flow())
