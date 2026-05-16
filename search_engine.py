import json
import os

BASE_DIR = os.environ.get("KNOWLEDGE_DB_PATH", "../knowledge-db")
INDEX_PATH = os.path.join(BASE_DIR, "index.json")

# グローバルキャッシュ
INDEX_CACHE = []
BODY_PATH_CACHE = {}
INDEX_MTIME = 0

def reload_data_if_updated():
    """index.json の更新を検知してキャッシュを全更新する"""
    global INDEX_MTIME

    try:
        current_mtime = os.path.getmtime(INDEX_PATH)
    except FileNotFoundError:
        return  # index.json が存在しない場合は何もしない

    if current_mtime != INDEX_MTIME:
        # -------------------------
        # index.json の再読み込み
        # -------------------------
        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                new_index = json.load(f)
        except Exception as e:
            print(f"❌ index.json 読み込みエラー: {e}")
            return

        # 参照を切り替えず、中身だけ更新
        INDEX_CACHE.clear()
        INDEX_CACHE.extend(new_index)

        # -------------------------
        # Markdown パスの再スキャン
        # -------------------------
        new_path_cache = {}
        for root, dirs, files in os.walk(BASE_DIR):
            for file in files:
                if file.endswith(".md"):
                    new_path_cache[file] = os.path.join(root, file)

        # 参照を切り替えず、中身だけ更新
        BODY_PATH_CACHE.clear()
        BODY_PATH_CACHE.update(new_path_cache)

        INDEX_MTIME = current_mtime
        print(f"🔄 Knowledge DB reloaded (Total: {len(INDEX_CACHE)} entries)")

def search_entries(query=None, category=None, include_body=False):
    """検索ロジック（カテゴリフィルタ + スコアリング検索）"""
    reload_data_if_updated()

    results = []

    # -------------------------
    # ① カテゴリフィルタ（query が None でも動く）
    # -------------------------
    filtered_entries = INDEX_CACHE
    if category:
        filtered_entries = [
            e for e in INDEX_CACHE
            if e.get("category") == category
        ]

    # -------------------------
    # ② キーワード検索（query が None の場合はカテゴリ一覧を返す）
    # -------------------------
    if not query:
        return filtered_entries

    query = query.lower()

    for entry in filtered_entries:
        score = 0

        # title
        if query in entry["title"].lower():
            score += 5

        # keywords
        for kw in entry["keywords"]:
            kw_l = kw.lower()
            if query == kw_l:
                score += 5
            elif query in kw_l:
                score += 3

        # summary
        if query in entry["summary"].lower():
            score += 2

        # body（全文検索）
        if include_body:
            body_file = entry["body"]
            path = BODY_PATH_CACHE.get(body_file)
            if path:
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        if query in f.read().lower():
                            score += 1
                except Exception:
                    pass

        if score > 0:
            results.append((score, entry))

    # スコア順に並べる
    results.sort(key=lambda x: x[0], reverse=True)
    return [entry for score, entry in results]
