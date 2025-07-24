# D:\AI\AI_Trading_System_ki\ui\components/logs_panel.py

import dash_bootstrap_components as dbc
from dash import html, dcc

def create_logs_panel():
    """ایجاد پنل لاگ‌ها"""
    return dbc.Card([
        dbc.CardHeader("لاگ‌های سیستم"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("فیلتر:"),
                        dbc.Input(type="text", id="log-filter", placeholder="جستجو در لاگ‌ها...")
                    ], className="mb-2")
                ], width=6),
                dbc.Col([
                    dbc.Button("🔄 بارگذاری مجدد", color="secondary", id="refresh-logs-btn"),
                    dbc.Button("📥 دانلود لاگ‌ها", color="info", id="download-logs-btn", className="ms-2")
                ], width=6)
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div(
                        id="logs-display",
                        children="هیچ لاگی موجود نیست.",
                        style={
                            "background-color": "#f8f9fa",
                            "border": "1px solid #dee2e6",
                            "border-radius": "4px",
                            "padding": "10px",
                            "height": "300px",
                            "overflow-y": "scroll",
                            "font-family": "monospace",
                            "font-size": "12px"
                        }
                    )
                ], width=12)
            ])
        ])
    ])