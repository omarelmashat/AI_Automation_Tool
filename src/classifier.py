import json

from api_client import generate_text

CATEGORIES = ["work", "study", "finance", "personal", "other"]

def build_prompt(text: str) -> str:
    return (
        "Classify the following text and summarize it.\n"
        f"Allowed categories: {', '.join(CATEGORIES)}.\n"
        'Respond with ONLY a JSON object in exactly this format: '
        '{"category": "<one allowed category>", "summary": "<one short sentence>"}\n'
        "No markdown, no extra text.\n\n"
        f"Text:\n{text}"
    )

def parse_response(raw: str) -> dict:
    fallback = {"category": "other", "summary": "Could not parse AI response."}

    start,end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1 or end < start:
        return fallback

    try:
        data = json.loads(raw[start:end + 1])
    except json.JSONDecodeError:
        return fallback

    category = str(data.get("category", "other")).lower().strip()
    if category not in CATEGORIES:
        category = "other"
    summary = str(data.get("summary", "")).strip() or "No summary"

    return {"category": category, "summary": summary}

def classify(text: str) -> dict:
    if not text or not text.strip():
        raise ValueError("Cannot classify empty text.")
    return parse_response(generate_text(build_prompt(text)))

if __name__ == "__main__":
    from pathlib import Path
    from reader import list_inbox_files, read_file

    inbox = Path(__file__).resolve().parent.parent / "inbox"
    for f in list_inbox_files(inbox):
        print(f.name, "->", classify(read_file(f)))