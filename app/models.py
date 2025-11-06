import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / 'checklist.json'


def load_checklist():
    if not DATA_FILE.exists():
        return {'items': [], 'last_reset': None}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_checklist(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
