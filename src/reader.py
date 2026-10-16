from pathlib import Path

SUPPORTED = {".txt",".md"}
MAX_CHARS = 4000

def list_inbox_files(inbox_dir: Path) -> list[Path]:
    if not inbox_dir.exists():
        raise FileNotFoundError(f"Inbox folder not found: {inbox_dir}")
    return sorted(p for p in inbox_dir.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED )

def read_file(path: Path) -> str:
    text = path.read_text(encoding = "utf-8", errors = "ignore".strip())
    return text[:MAX_CHARS]

if __name__ == "__main__":
    inbox = Path(__file__).resolve().parent.parent / "inbox"
    for f in list_inbox_files(inbox):
        print(f"{f.name}: {len(read_file(f))} characters")