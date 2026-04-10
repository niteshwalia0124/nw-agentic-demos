import asyncio
import os
from agent import root_agent
from google.adk.agents.callback_context import CallbackContext

async def test_end_to_end():
    print("🚀 Starting End-to-End Persona Evaluation...\n")
    
    # 1. Simulate a User Request
    user_query = "Namaste! My name is Rajesh Sharma. I live in Mumbai and I am looking for a health insurance plan for my family. What do you suggest, and can I save tax?"
    
    print(f"👤 User: {user_query}")
    print("-" * 50)

    # 2. Mock the state as if tools were just run
    # (Since we want to show the 'Persona' synthesis)
    mock_state = {
        "policy_data": "Arogya Sanjeevani Policy is the standard IRDAI plan. Covers hospitalization up to ₹5 Lakhs. Includes AYUSH treatment.",
        "risk_data": "For a 35-year-old in Mumbai, monthly premium is approximately ₹450.",
        "claims_data": "Customer has 1 past claim for auto collision, but none for health.",
        "compliance_data": "Eligible for up to ₹25,000 deduction under Section 80D."
    }

    # 3. Create a mock context with this state
    context = CallbackContext(state=mock_state)

    # 4. Run the agent logic
    # Note: We are testing the Root Agent's ability to SYNTHESIZE into the Bima Sahayak persona.
    # The instruction template uses these keys: {policy_data}, {risk_data}, {claims_data}, {compliance_data}
    
    print("🤖 Bima Sahayak is thinking (Synthesizing Data)...")
    
    # We execute the agent directly to see the final response
    # In a real eval, ADK would do this and compare with a ground truth.
    response = await root_agent.model.generate_content(
        root_agent.instruction.format(**mock_state) + f"\n\nUser query: {user_query}"
    )

    print("\n✨ Bima Sahayak's Response:")
    print("=" * 50)
    print(response.text)
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_end_to_end())
