import os
import cohere
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("AI_PROVIDER", "cohere").lower()
COHERE_MODEL = os.getenv("COHERE_MODEL", "command-a-03-2025")

def _cohere_generate(prompt: str) -> str:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise RuntimeError("Cohere API key is missing. Check your .env file")

    client = cohere.ClientV2(api_key)
    response = client.chat(
        model=COHERE_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.message.content[0].text

def generate_text(prompt: str) -> str:
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty or whitespace.")

    if PROVIDER == "cohere":
        return _cohere_generate(prompt)

    raise ValueError(f"Unsupported AI provider: {PROVIDER}. Supported providers: cohere.")

if __name__ == "__main__":
    print(generate_text("Hello, how are you?"))