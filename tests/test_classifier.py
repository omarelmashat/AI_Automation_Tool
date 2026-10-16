import sys
from pathlib import Path    

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from classifier import parse_response , classify

def test_valid_json():
    raw = '{"category": "work", "summary": "Meeting moved."}'
    assert parse_response(raw) == {"category": "work", "summary": "Meeting moved."}

def test_json_wrapped_in_markdown_and_text():
    raw = 'Sure! ```json\n{"category": "study", "summary": "Exam info."}\n```'
    assert parse_response(raw)["category"] == "study"


def test_unknown_category_becomes_other():
    raw = '{"category": "sports", "summary": "Match report."}'
    assert parse_response(raw)["category"] == "other"


def test_garbage_returns_fallback():
    assert parse_response("I cannot do that")["category"] == "other"


def test_empty_text_raises():
    with pytest.raises(ValueError):
        classify("   ")