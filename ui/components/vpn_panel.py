# D:\AI\AI_Trading_System_ki\ui\components/vpn_panel.py

import dash_bootstrap_components as dbc
from dash import html, dcc

def create_vpn_panel():
    """ایجاد پنل VPN"""
    return dbc.Card([
        dbc.CardHeader("مدیریت VPN"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H5("وضعیت اتصال:"),
                    html.Div(id="vpn-status", children="قطع شده", style={"color": "red"})
                ], width=12)
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.H5("سرورهای موجود:"),
                    dcc.Dropdown(
                        id="vpn-servers",
                        options=[
                            {"label": "سرور آلمان", "value": "de"},
                            {"label": "سرور فرانسه", "value": "fr"},
                            {"label": "سرور هلند", "value": "nl"}
                        ],
                        placeholder="انتخاب سرور..."
                    ),
                    html.Br(),
                    dbc.Button("🔌 اتصال", color="success", id="connect-vpn-btn"),
                    dbc.Button("🚫 قطع اتصال", color="warning", id="disconnect-vpn-btn", className="ms-2")
                ], width=12)
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H5("تست اتصال:"),
                    dbc.Button("🔍 تست دسترسی صرافی‌ها", color="info", id="test-connectivity-btn"),
                    html.Div(id="connectivity-test-result", className="mt-2")
                ], width=12)
            ])
        ])
    ])