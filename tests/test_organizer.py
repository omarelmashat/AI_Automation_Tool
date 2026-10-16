import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from organizer import move_to_category, write_log


def test_file_moves_into_category_folder(tmp_path):
    source = tmp_path / "note.txt"
    source.write_text("hello")
    organized = tmp_path / "organized"

    dest = move_to_category(source, "work", organized)

    assert dest == organized / "work" / "note.txt"
    assert dest.exists()
    assert not source.exists()


def test_name_collision_does_not_overwrite(tmp_path):
    organized = tmp_path / "organized"
    for _ in range(2):
        source = tmp_path / "note.txt"
        source.write_text("hello")
        move_to_category(source, "work", organized)

    assert (organized / "work" / "note.txt").exists()
    assert (organized / "work" / "note_1.txt").exists()


def test_log_has_header_once_and_appends(tmp_path):
    log = tmp_path / "log.csv"
    write_log(log, "a.txt", "work", "First.", "ok")
    write_log(log, "b.txt", "study", "Second.", "ok")

    rows = list(csv.reader(log.open(encoding="utf-8")))
    assert rows[0][0] == "timestamp"
    assert len(rows) == 3