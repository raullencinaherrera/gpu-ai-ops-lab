import json
from pathlib import Path

DATA_FILE = Path("data/current_state.json")


def save_state(state: dict) -> None:
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(state, indent=2))


def load_state() -> dict:
    if not DATA_FILE.exists():
        return {}
    return json.loads(DATA_FILE.read_text())
