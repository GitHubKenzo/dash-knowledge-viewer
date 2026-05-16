from dash import html, dcc

def render_search_bar():
    return html.Div(
        id="search-bar",
        children=[
            dcc.Input(
                id="search-input",
                type="text",
                placeholder="キーワードで検索...",
                style={"width": "300px", "padding": "6px"}
            ),
            html.Button(
                "検索",
                id="search-button",
                n_clicks=0,
                style={"marginLeft": "8px"}
            )
        ],
        style={"marginBottom": "20px"}
    )
