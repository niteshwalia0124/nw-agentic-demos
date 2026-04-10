import asyncio
import pytest
from insurance_advisor.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

@pytest.mark.asyncio
async def test_end_to_end():
    print("🚀 Starting End-to-End Persona Evaluation...\n")
    
    app_name = "insurance_advisor"
    user_id = "test_user"
    session_id = "session_persona_test"
    
    # 1. Setup Session with Mocked State
    session_service = InMemorySessionService()
    mock_state = {
        "policy_data": "Arogya Sanjeevani Policy is the standard IRDAI plan. Covers hospitalization up to ₹5 Lakhs. Includes AYUSH treatment.",
        "risk_data": "For a 35-year-old in Mumbai, monthly premium is approximately ₹450.",
        "claims_data": "Customer has 1 past claim for auto collision, but none for health.",
        "compliance_data": "Eligible for up to ₹25,000 deduction under Section 80D."
    }
    await session_service.create_session(
        app_name=app_name, 
        user_id=user_id, 
        session_id=session_id,
        state=mock_state
    )

    # 2. Initialize Runner
    runner = Runner(agent=root_agent, app_name=app_name, session_service=session_service)

    # 3. Simulate a User Request
    user_query = "Namaste! My name is Rajesh Sharma. I live in Mumbai and I am looking for a health insurance plan for my family. What do you suggest, and can I save tax?"
    print(f"👤 User: {user_query}")
    print("-" * 50)

    print("🤖 Bima Sahayak is thinking (Synthesizing Data)...")
    
    msg = types.Content(role="user", parts=[types.Part.from_text(text=user_query)])
    final_response_text = ""
    
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=msg):
        if event.is_final_response():
            if event.content and event.content.parts:
                 final_response_text = "".join([p.text for p in event.content.parts if getattr(p, 'text', None)])

    print("\n✨ Bima Sahayak's Response:")
    print("=" * 50)
    print(final_response_text)
    print("=" * 50)
    
    assert "Rajesh" in final_response_text
    # Relaxing assertions slightly for LLM variability while ensuring grounding
    assert any(word in final_response_text for word in ["Mumbai", "Maharashtra", "City"]) 
    assert any(word in final_response_text.lower() for word in ["tax", "80d", "bachat", "saving"])

if __name__ == "__main__":
    asyncio.run(test_end_to_end())
