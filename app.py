import dash
from dash import html, dcc, Input, Output
import json
from search_engine import INDEX_CACHE
from markdown_loader import load_markdown

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Knowledge DB Viewer"),

    dcc.Input(
        id="search-box",
        type="text",
        placeholder="検索ワードを入力...",
        style={"width": "400px", "marginBottom": "20px"}
    ),

    html.Div(id="search-results"),
    html.Hr(),
    html.Div(id="content-area")
])

@app.callback(
    Output("search-results", "children"),
    Input("search-box", "value")
)
def update_results(query):
    from search_engine import search_entries

    if not query:
        return "検索ワードを入力してください。"

    results = search_entries(query)

    if not results:
        return "一致するナレッジはありません。"

    return html.Ul([
        html.Li([
            html.A(
                f"{entry['title']}（{entry['category']}）",
                href="#",
                id={"type": "entry-link", "id": entry["id"]}
            )
        ])
        for entry in results
    ])

@app.callback(
    Output("content-area", "children"),
    Input({"type": "entry-link", "id": dash.ALL}, "n_clicks"),
    prevent_initial_call=True
)
def display_content(n_clicks):
    ctx = dash.callback_context
    if not ctx.triggered or all(c is None for c in n_clicks):
        return ""

    # {"type":"entry-link","id":"xxx"} を安全にパース
    raw = ctx.triggered[0]["prop_id"].split(".")[0]
    entry_info = json.loads(raw.replace("'", '"'))
    entry_id = entry_info["id"]

    # INDEX_CACHE を直接参照（高速）
    entry = next((e for e in INDEX_CACHE if e["id"] == entry_id), None)

    if not entry:
        return "エントリが見つかりません。"

    html_body = load_markdown(entry["body"])

    return html.Div([
        html.H2(entry["title"]),
        dcc.Markdown(html_body, dangerously_allow_html=True)
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)

