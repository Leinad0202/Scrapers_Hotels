import json
from typing import List

def save_json(data: List, path: str):
    serializable = [
        item.to_dict() if hasattr(item, "to_dict") else item
        for item in data
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)

def load_json(path: str) -> List:
    """Carrega JSON de um arquivo. Retorna lista vazia se não existir."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
