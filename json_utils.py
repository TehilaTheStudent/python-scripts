# json_utils.py
# Utilities for reading and writing JSON files
import json
from typing import Any

def save_json(data: Any, filepath: str) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(filepath: str) -> Any:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
