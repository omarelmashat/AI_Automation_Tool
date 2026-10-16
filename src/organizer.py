import csv
import shutil
from datetime import datetime
from pathlib import Path

LOG_HEADERS = ["timestamp", "filename", "category", "summary", "status"]

def unique_destination(folder: Path, filename: str) -> Path:
    dest = folder / filename
    counter = 1
    while dest.exists():
        dest = folder /f"{Path(filename).stem}_{counter}{Path(filename).suffix}"
        counter += 1
    return dest

def move_to_category(file_path: Path, category: str, organized_dir: Path) -> Path:
    folder = organized_dir / category
    folder.mkdir(parents = True, exist_ok = True)
    dest = unique_destination(folder,file_path.name)
    shutil.move(str(file_path), str(dest))
    return dest

def write_log(log_path: Path, filename:str, category: str, summary: str, status: str) -> None:
    new_file = not log_path.exists()
    with log_path.open("a", newline = "", encoding = "utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(LOG_HEADERS)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            filename,category, summary, status,
        ])
        