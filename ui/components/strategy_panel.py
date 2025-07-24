# D:\AI\AI_Trading_System_ki\ui\components/strategy_panel.py

import dash_bootstrap_components as dbc
from dash import html, dcc

def create_strategy_panel():
    """ایجاد پنل استراتژی‌ها"""
    return dbc.Card([
        dbc.CardHeader("مدیریت استراتژی‌ها"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("➕ افزودن استراتژی", color="primary", className="me-2"),
                    dbc.Button("🔄 بارگذاری مجدد", color="secondary")
                ], width=12)
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id="strategy-dropdown",
                        options=[
                            {"label": "استراتژی DQN", "value": "dqn"},
                            {"label": "استراتژی MA", "value": "ma"},
                            {"label": "استراتژی RSI", "value": "rsi"}
                        ],
                        placeholder="انتخاب استراتژی..."
                    )
                ], width=6),
                dbc.Col([
                    dbc.Button("▶️ اجرا", color="success", id="run-strategy-btn"),
                    dbc.Button("⏹️ توقف", color="danger", id="stop-strategy-btn", className="ms-2")
                ], width=6)
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H5("پارامترهای استراتژی:"),
                    html.Div(id="strategy-parameters")
                ], width=12)
            ])
        ])
    ])