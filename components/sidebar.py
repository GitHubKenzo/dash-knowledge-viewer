from dash import html, dcc
from category_loader import load_categories

def render_sidebar():
    """
    左側固定のカテゴリサイドバーを返す。
    """
    categories = load_categories()

    return html.Div(
        id="sidebar",
        children=[
            html.H2("カテゴリ", className="sidebar-title"),

            # カテゴリ一覧
            html.Ul(
                [
                    html.Li(
                        html.A(
                            cat["name"],
                            href=f"/category/{cat['id']}",
                            className="sidebar-link"
                        )
                    )
                    for cat in categories
                ],
                className="sidebar-list"
            )
        ],
        style={
            "width": "240px",
            "padding": "20px",
            "backgroundColor": "#f5f5f5",
            "position": "fixed",
            "top": "0",
            "left": "0",
            "bottom": "0",
            "overflowY": "auto",
            "borderRight": "1px solid #ddd"
        }
    )
