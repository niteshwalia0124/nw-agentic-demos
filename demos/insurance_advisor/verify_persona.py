import asyncio
from agent import root_agent
from google.adk.agents.callback_context import CallbackContext

async def main():
    # Mocking state as if it was already gathered for a demo
    state = {
        "policy_data": "Arogya Sanjeevani Policy offers standard coverage with AYUSH benefits. Sum insured up to ₹5 Lakhs.",
        "risk_data": "Base premium ₹450/month. Multi-policy discount applied.",
        "claims_data": "No prior claims.",
        "compliance_data": "Eligible for ₹25,000 tax deduction under Section 80D."
    }
    
    # We just want to see how the Root Agent synthesizes this into the Bima Sahayak persona
    prompt = "I want to buy a health policy for my daughter. What are the benefits and can I save tax?"
    
    # Note: In a real run, it would delegate. Here we check the instruction adherence.
    print(f"User: {prompt}\n")
    print("--- Bima Sahayak Response ---\n")
    
    # We can't easily run the full MCP stack here, but we can verify the prompt rendering
    # and the logic by looking at the Agent's instruction property.
    print(root_agent.instruction)

if __name__ == "__main__":
    asyncio.run(main())
