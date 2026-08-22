# ==================================================
# TEST LLM SERVICE
# ==================================================

from llm_service import generate_ai_response


prompt = """
You are analyzing customer reviews for an e-commerce business.

Reply with exactly one short sentence explaining why
customer review analysis is useful for a business.
"""


try:

    response = generate_ai_response(prompt)

    print("✅ LLM service working!")
    print()
    print("🤖 Gemini response:")
    print(response)


except Exception as e:

    print("❌ LLM service failed!")
    print(type(e).__name__)
    print(e)