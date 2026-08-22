import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY not found!")
    raise SystemExit

print("✅ API key loaded successfully!")

client = OpenAI(api_key=api_key)

try:
    response = client.responses.create(
        model="gpt-4o-mini",
        input="Reply with exactly: OpenAI connection successful!"
    )

    print("🤖", response.output_text)

except Exception as e:
    print("❌ OpenAI connection failed!")
    print(type(e).__name__)
    print(e)