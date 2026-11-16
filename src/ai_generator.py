
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

MODEL_NAME = "qwen3.5:4b"


def generate_ai_business_report(prompt):

    if not prompt or not prompt.strip():
        raise ValueError("The prompt cannot be empty.")

    payload = {
        "model": MODEL_NAME,

        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],

        "think": False,
        "stream": False,

        "options": {
            "num_predict": 700,
            "temperature": 0.2
        }
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=(10, 600)
        )

        response.raise_for_status()

        result = response.json()

        report = result.get(
            "message", {}
        ).get(
            "content", ""
        ).strip()

        if not report:
            raise RuntimeError(
                "Ollama returned an empty report."
            )

        return report

    except requests.exceptions.ConnectionError as error:

        raise RuntimeError(
            "Cannot connect to Ollama. "
            "Make sure Ollama is running."
        ) from error

    except requests.exceptions.Timeout as error:

        raise RuntimeError(
            "The AI model took too long to respond."
        ) from error

    except requests.exceptions.HTTPError as error:

        raise RuntimeError(
            f"Ollama API error: {error}"
        ) from error
