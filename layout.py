from dash import html, dcc
from components.sidebar import render_sidebar
from components.search_bar import render_search_bar   # ← 追加

def render_layout():
    """
    アプリ全体の2カラムレイアウトを返す。
    左：サイドバー（固定）
    右：メインコンテンツ（動的）
    """
    return html.Div(
        id="app-container",
        children=[
            # 左カラム：サイドバー
            render_sidebar(),

            # 右カラム：メインコンテンツ
            html.Div(
                id="main-content",
                children=[
                    dcc.Location(id="url", refresh=False),

                    render_search_bar(),     # ← これを追加（上部に検索バー）

                    html.Div(id="page-content")
                ],
                style={
                    "marginLeft": "260px",
                    "padding": "20px"
                }
            )
        ]
    )
