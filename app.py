from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from layout import render_layout
from search_engine import search_entries
from components.card_factory import create_card
from markdown_loader import load_markdown
from urllib.parse import urlparse, parse_qs

app = Dash(__name__, suppress_callback_exceptions=True)

# 全体レイアウト（サイドバー + 検索バー + ページコンテンツ）
app.layout = render_layout()


# -----------------------------
# URL ルーティング
# -----------------------------
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):

    # トップページ
    if pathname == "/" or pathname is None:
        return html.Div([
            html.H2("ナレッジベースへようこそ"),
            html.P("左のカテゴリ、または検索バーから検索できます。")
        ])

    # カテゴリページ
    if pathname.startswith("/category/"):
        category_id = pathname.split("/")[-1]
        results = search_entries(category=category_id)

        return html.Div([
            html.H2(f"カテゴリ: {category_id}"),
            html.Div([create_card(e) for e in results])
        ])

    # 検索ページ
    if pathname.startswith("/search"):
        # /search?q=xxx をパース
        parsed = urlparse(pathname + "?")
        query = parse_qs(parsed.query).get("q", [""])[0]

        results = search_entries(query=query)

        return html.Div([
            html.H2(f"検索結果: {query}"),
            html.Div([create_card(e) for e in results])
        ])

    # エントリ詳細ページ
    if pathname.startswith("/entry/"):
        entry_id = pathname.split("/")[-1]
        md = load_markdown(entry_id)

        return html.Div([
            dcc.Markdown(md)
        ])

    # 404
    return html.Div("404 Not Found")


# -----------------------------
# 検索ボタン → URL 書き換え
# -----------------------------
@app.callback(
    Output("url", "pathname"),
    Input("search-button", "n_clicks"),
    Input("search-input", "value"),
    prevent_initial_call=True
)
def update_search(n_clicks, value):
    if value:
        return f"/search?q={value}"
    return "/"


# -----------------------------
# サーバー起動（Dash 3.x）
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
