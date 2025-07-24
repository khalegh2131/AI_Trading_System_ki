# D:\AI\AI_Trading_System_ki\ui\components/api_panel.py

import dash_bootstrap_components as dbc
from dash import html, dcc

def create_api_panel():
    """ایجاد پنل APIها"""
    return dbc.Card([
        dbc.CardHeader("مدیریت APIها"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H5("اتصالات فعال:"),
                    html.Div(id="api-status", children="در حال بررسی...")
                ], width=12)
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.H5("افزودن API جدید:"),
                    dbc.Input(id="api-name", placeholder="نام API", type="text", className="mb-2"),
                    dbc.Input(id="api-key", placeholder="کلید API", type="password", className="mb-2"),
                    dbc.Input(id="api-secret", placeholder="رمز API", type="password", className="mb-2"),
                    dbc.Select(
                        id="api-type",
                        options=[
                            {"label": "کریپتو", "value": "crypto"},
                            {"label": "فارکس", "value": "forex"}
                        ],
                        className="mb-2"
                    ),
                    dbc.Button("➕ افزودن", color="primary", id="add-api-btn")
                ], width=6)
            ])
        ])
    ])