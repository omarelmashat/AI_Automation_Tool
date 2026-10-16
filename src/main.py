from pathlib import Path

from reader import list_inbox_files, read_file
from classifier import classify
from organizer import move_to_category, write_log

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
ORGANIZED = ROOT / "organized"
LOG = ROOT / "log.csv"

def process_file(path: Path) -> None:
    try:
        text = read_file(path)
        result = classify(text)
        move_to_category(path, result["category"], ORGANIZED)
        write_log(LOG, path.name, result["category"], result["summary"], "ok")
        print(f"✔ {path.name} -> {result['category']}: {result['summary']}")
    except Exception as e:
        write_log(LOG, path.name, "", "", f"error: {e}")
        print(f"✘ {path.name} failed: {e}")

def main() -> None:
    files = list_inbox_files(INBOX)
    if not files:
        print("Inbox is empty. Add .txt or .md files to inbox/ and run again.")
        return

    print(f"Processing {len(files)} file(s)...\n")
    for f in files:
        process_file(f)
    print(f"\nDone. See {LOG.name} for the full log.")


if __name__ == "__main__":
    main()