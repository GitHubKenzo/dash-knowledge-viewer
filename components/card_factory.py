from dash import html
from datetime import datetime

def format_date(date_str):
    """YYYY-MM-DD → YYYY/MM/DD に整形"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y/%m/%d")
    except Exception:
        return date_str


def create_card(entry):
    """
    Knowledge DB の entry からカード UI を生成する。
    """
    updated = format_date(entry.get("updated_at", ""))
    keywords = entry.get("keywords", [])
    category = entry.get("category", "")

    return html.Div(
        className="result-card",
        children=[
            # タイトル
            html.H3(entry["title"], className="card-title"),

            # カテゴリバッジ
            html.Span(
                category,
                className="badge-category"
            ),

            # 更新日
            html.Div(
                f"更新日: {updated}",
                className="card-updated"
            ),

            # キーワードタグ
            html.Div(
                [
                    html.Span(kw, className="tag") for kw in keywords
                ],
                className="tag-container"
            ),

            # summary
            html.P(entry["summary"], className="card-summary"),

            # 「開く」ボタン
            html.A(
                "開く",
                href="#",
                id={"type": "entry-link", "id": entry["id"]},
                className="card-open-link"
            )
        ]
    )
