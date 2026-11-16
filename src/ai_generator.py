
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Locate the main project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load API key from the project's .env file
load_dotenv(PROJECT_ROOT / ".env", override=True)


def generate_ai_business_report(prompt):

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. Check your .env file."
        )

    if not prompt or not prompt.strip():
        raise ValueError("The prompt cannot be empty.")

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )

    report = response.output_text

    if not report:
        raise RuntimeError("The AI model returned an empty report.")

    return report
