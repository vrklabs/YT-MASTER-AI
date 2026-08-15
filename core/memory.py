import json
import os
from typing import Any, Dict

class Memory:
    def __init__(self, storage_path: str = "data/memory"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

    def save(self, key: str, value: Any):
        filepath = os.path.join(self.storage_path, f"{key}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(value, f, ensure_ascii=False, indent=2)

    def load(self, key: str):
        filepath = os.path.join(self.storage_path, f"{key}.json")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
