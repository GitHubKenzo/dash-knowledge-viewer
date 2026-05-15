import markdown
import os
from search_engine import BODY_PATH_CACHE

def load_markdown(body_filename):
    path = BODY_PATH_CACHE.get(body_filename)
    if not path:
        return "<p>本文ファイルが見つかりません。</p>"

    try:
        with open(path, "r", encoding="utf-8") as f:
            md = f.read()
            return markdown.markdown(md, extensions=["fenced_code", "tables"])
    except Exception as e:
        return f"<p>Markdown 読み込みエラー: {str(e)}</p>"
