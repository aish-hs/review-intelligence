# ==================================================
# LLM SERVICE
# ==================================================

import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI


# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()


# ==================================================
# GET API KEY
# ==================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


if not GOOGLE_API_KEY:

    raise ValueError(
        "GOOGLE_API_KEY not found in .env"
    )


# ==================================================
# CREATE GEMINI MODEL
# ==================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GOOGLE_API_KEY
)


# ==================================================
# GENERATE AI RESPONSE
# ==================================================

def generate_ai_response(prompt):

    response = llm.invoke(prompt)

    content = response.content

    # Gemini may return structured content
    # instead of a plain string.

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                if item.get("type") == "text":

                    text_parts.append(
                        item.get("text", "")
                    )

            elif isinstance(item, str):

                text_parts.append(item)

        return "".join(text_parts).strip()

    return str(content).strip()