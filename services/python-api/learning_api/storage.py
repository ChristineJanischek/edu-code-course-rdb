import json
import os
from pathlib import Path


def load_json_file(path_value: str) -> dict:
    json_path = Path(path_value)
    if not json_path.exists():
        return {"error": f"JSON-Datei nicht gefunden: {json_path}"}
    with json_path.open("r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def load_json_db() -> dict:
    return load_json_file(os.getenv("JSON_DB_PATH", "/app/data.json"))


def load_curriculum_index() -> dict:
    return load_json_file(os.getenv("CURRICULUM_INDEX_PATH", "/app/generated/lehrplaene/index.json"))
