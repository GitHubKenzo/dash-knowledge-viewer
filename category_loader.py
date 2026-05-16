import json
import os

BASE_DIR = os.environ.get("KNOWLEDGE_DB_PATH", "../knowledge-db")
CATEGORIES_PATH = os.path.join(BASE_DIR, "config", "categories.json")

_CATEGORIES_CACHE = None
_CATEGORIES_MTIME = 0


def load_categories():
    global _CATEGORIES_CACHE, _CATEGORIES_MTIME

    try:
        mtime = os.path.getmtime(CATEGORIES_PATH)
    except FileNotFoundError:
        return []

    if _CATEGORIES_CACHE is not None and mtime == _CATEGORIES_MTIME:
        return _CATEGORIES_CACHE

    try:
        with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ categories.json 読み込みエラー: {e}")
        return []

    if isinstance(data, list):
        data_sorted = sorted(data, key=lambda x: x.get("order", 9999))
    else:
        data_sorted = data

    _CATEGORIES_CACHE = data_sorted
    _CATEGORIES_MTIME = mtime

    return data_sorted
