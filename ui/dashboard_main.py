# D:\AI\AI_Trading_System_ki\ui\dashboard_main.py

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import json
import requests
import threading
import time
import psutil
import base64

# محلی‌سازی logger
def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = get_logger("ProfessionalDashboard")

# ایجاد اپلیکیشن Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

app.title = "🧠 AI Trading System Pro"

# Layout اصلی - بدون تب‌های شلوغ
def create_professional_layout():
    return dbc.Container([
        # هدر حرفه‌ای
        dbc.Row([
            dbc.Col([
                html.H1("🧠 AI Trading System Professional", className="text-center text-primary"),
                html.P("داشبورد هوشمند معاملات الگوریتمی - کنترل کامل در یک صفحه", 
                      className="text-center text-muted"),
                html.Hr()
            ], width=12)
        ], className="mb-3"),
        
        # نوار کنترل بالا - همه چیز در دسترس
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            # کنترل سریع API
                            dbc.Col([
                                html.Div([
                                    html.Small("📡 API Status", className="text-muted"),
                                    html.Div(id="quick-api-status", children="Checking...", 
                                            style={"color": "orange", "fontSize": "12px"})
                                ])
                            ], width=2, className="text-center"),
                            
                            # کنترل سریع VPN
                            dbc.Col([
                                html.Div([
                                    html.Small("🔒 VPN", className="text-muted"),
                                    html.Div(id="quick-vpn-status", children="Disconnected", 
                                            style={"color": "red", "fontSize": "12px"})
                                ])
                            ], width=2, className="text-center"),
                            
                            # کنترل سریع AI
                            dbc.Col([
                                html.Div([
                                    html.Small("🤖 AI Engine", className="text-muted"),
                                    html.Div(id="quick-ai-status", children="Active", 
                                            style={"color": "green", "fontSize": "12px"})
                                ])
                            ], width=2, className="text-center"),
                            
                            # جفت‌ارز فعال
                            dbc.Col([
                                html.Div([
                                    html.Small("📊 Pairs", className="text-muted"),
                                    html.Div(id="quick-pairs-count", children="0 Active", 
                                            style={"color": "white", "fontSize": "12px"})
                                ])
                            ], width=2, className="text-center"),
                            
                            # حافظه سیستم
                            dbc.Col([
                                html.Div([
                                    html.Small("💾 Memory", className="text-muted"),
                                    html.Div(id="quick-memory", children="0%", 
                                            style={"color": "white", "fontSize": "12px"})
                                ])
                            ], width=2, className="text-center"),
                            
                            # زمان سیستم
                            dbc.Col([
                                html.Div([
                                    html.Small("⏰ Time", className="text-muted"),
                                    html.Div(id="quick-time", children=datetime.now().strftime("%H:%M:%S"), 
                                            style={"color": "white", "fontSize": "12px"})
                                ])
                            ], width=2, className="text-center")
                        ])
                    ])
                ], color="dark")
            ], width=12)
        ], className="mb-3"),
        
        # بخش اصلی - Grid Layout
        dbc.Row([
            # سمت چپ - نمودارها و تحلیل‌ها
            dbc.Col([
                # نمودار اصلی
                dbc.Card([
                    dbc.CardHeader([
                        html.Div([
                            "📈 Live Chart - ",
                            dcc.Dropdown(
                                id="main-chart-pair",
                                options=[
                                    {"label": "BTC/USDT", "value": "BTCUSDT"},
                                    {"label": "ETH/USDT", "value": "ETHUSDT"},
                                    {"label": "BNB/USDT", "value": "BNBUSDT"}
                                ],
                                value="BTCUSDT",
                                clearable=False,
                                style={"width": "150px", "display": "inline-block", "marginLeft": "10px"}
                            ),
                            " ",
                            dcc.Dropdown(
                                id="main-chart-timeframe",
                                options=[
                                    {"label": "1m", "value": "1m"},
                                    {"label": "5m", "value": "5m"},
                                    {"label": "15m", "value": "15m"},
                                    {"label": "1h", "value": "1h"},
                                    {"label": "4h", "value": "4h"},
                                    {"label": "1d", "value": "1d"}
                                ],
                                value="1h",
                                clearable=False,
                                style={"width": "80px", "display": "inline-block", "marginLeft": "10px"}
                            )
                        ], style={"display": "flex", "alignItems": "center"})
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id="main-live-chart", style={"height": "400px"}),
                        dcc.Interval(id="main-chart-interval", interval=5000, n_intervals=0)
                    ])
                ], color="dark", className="mb-3"),
                
                # تحلیل تکنیکال
                dbc.Card([
                    dbc.CardHeader("🔍 Technical Analysis"),
                    dbc.CardBody([
                        html.Div(id="technical-analysis", children="در حال تحلیل..."),
                        dcc.Interval(id="tech-analysis-interval", interval=10000, n_intervals=0)
                    ])
                ], color="dark", className="mb-3"),
                
                # تحلیل نهنگ‌ها
                dbc.Card([
                    dbc.CardHeader("🐳 Whale Analysis"),
                    dbc.CardBody([
                        html.Div(id="whale-analysis", children="در حال تحلیل نهنگ‌ها..."),
                        dcc.Interval(id="whale-analysis-interval", interval=30000, n_intervals=0)
                    ])
                ], color="dark")
            ], width=8),
            
            # سمت راست - کنترل‌ها و اطلاعات
            dbc.Col([
                # کنترل APIها
                dbc.Card([
                    dbc.CardHeader("🔌 API Connections"),
                    dbc.CardBody([
                        html.Div(id="api-connections-panel"),
                        dbc.Button("➕ Add New API", id="open-api-modal", color="primary", size="sm", className="mt-2")
                    ])
                ], color="dark", className="mb-3"),
                
                # کنترل VPN
                dbc.Card([
                    dbc.CardHeader("🔒 VPN Manager"),
                    dbc.CardBody([
                        html.Div(id="vpn-status-panel"),
                        dbc.Button("🔄 Refresh VPN", id="refresh-vpn-btn", color="info", size="sm", className="mt-2")
                    ])
                ], color="dark", className="mb-3"),
                
                # کنترل AI
                dbc.Card([
                    dbc.CardHeader("🤖 AI Control"),
                    dbc.CardBody([
                        html.Div(id="ai-control-panel"),
                        dbc.ButtonGroup([
                            dbc.Button("▶️ Start AI", id="start-ai-btn", color="success", size="sm"),
                            dbc.Button("⏹️ Stop AI", id="stop-ai-btn", color="danger", size="sm"),
                            dbc.Button("🔄 Retrain", id="retrain-ai-btn", color="warning", size="sm")
                        ], size="sm")
                    ])
                ], color="dark", className="mb-3"),
                
                # دانلود داده‌های تاریخی
                dbc.Card([
                    dbc.CardHeader("📥 Historical Data"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Symbol"),
                                dcc.Dropdown(
                                    id="hist-symbol",
                                    options=[
                                        {"label": "BTC/USDT", "value": "BTCUSDT"},
                                        {"label": "ETH/USDT", "value": "ETHUSDT"}
                                    ],
                                    value="BTCUSDT",
                                    clearable=False
                                )
                            ], width=6),
                            dbc.Col([
                                dbc.Label("Timeframe"),
                                dcc.Dropdown(
                                    id="hist-timeframe",
                                    options=[
                                        {"label": "1m", "value": "1m"},
                                        {"label": "5m", "value": "5m"},
                                        {"label": "15m", "value": "15m"},
                                        {"label": "1h", "value": "1h"},
                                        {"label": "4h", "value": "4h"},
                                        {"label": "1d", "value": "1d"}
                                    ],
                                    value="1h",
                                    clearable=False
                                )
                            ], width=6)
                        ], className="mb-2"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("From"),
                                dcc.DatePickerSingle(
                                    id="hist-start-date",
                                    date=datetime.now() - timedelta(days=30),
                                    display_format="YYYY-MM-DD",
                                    style={"width": "100%"}
                                )
                            ], width=6),
                            dbc.Col([
                                dbc.Label("To"),
                                dcc.DatePickerSingle(
                                    id="hist-end-date",
                                    date=datetime.now(),
                                    display_format="YYYY-MM-DD",
                                    style={"width": "100%"}
                                )
                            ], width=6)
                        ], className="mb-2"),
                        dbc.Button("📥 Download Data", id="download-hist-btn", color="primary", size="sm", className="w-100"),
                        html.Div(id="download-status", className="mt-2", style={"fontSize": "12px"})
                    ])
                ], color="dark", className="mb-3"),
                
                # وضعیت سیستم
                dbc.Card([
                    dbc.CardHeader("🖥️ System Status"),
                    dbc.CardBody([
                        html.Div(id="system-status-details", style={"fontSize": "12px"})
                    ])
                ], color="dark")
            ], width=4)
        ]),
        
        # Modal برای افزودن API جدید
        dbc.Modal([
            dbc.ModalHeader("➕ Add New API Connection"),
            dbc.ModalBody([
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("API Name"),
                            dbc.Input(type="text", id="new-api-name", placeholder="e.g., Binance Pro")
                        ], width=12)
                    ], className="mb-2"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("API Type"),
                            dbc.Select(
                                id="new-api-type",
                                options=[
                                    {"label": "Crypto (Binance)", "value": "crypto"},
                                    {"label": "Forex (MT4)", "value": "forex"},
                                    {"label": "Stocks", "value": "stocks"}
                                ]
                            )
                        ], width=12)
                    ], className="mb-2"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Base URL"),
                            dbc.Input(type="text", id="new-api-url", placeholder="https://api.binance.com")
                        ], width=12)
                    ], className="mb-2"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("API Key"),
                            dbc.Input(type="password", id="new-api-key")
                        ], width=12)
                    ], className="mb-2"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("API Secret"),
                            dbc.Input(type="password", id="new-api-secret")
                        ], width=12)
                    ], className="mb-2"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Checklist(
                                options=[{"label": "Use VPN Connection", "value": "vpn"}],
                                id="new-api-use-vpn",
                                switch=True
                            )
                        ], width=12)
                    ], className="mb-2")
                ])
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancel", id="close-api-modal", color="secondary"),
                dbc.Button("➕ Add API", id="add-api-btn", color="primary")
            ])
        ], id="api-modal"),
        
        # فوتر
        dbc.Row([
            dbc.Col([
                html.Hr(),
                html.P(f"© 2025 AI Trading System Pro - Last Update: {datetime.now().strftime('%Y/%m/%d %H:%M')}", 
                      className="text-center text-muted", style={"fontSize": "12px"})
            ], width=12)
        ])
    ], fluid=True, style={"background-color": "#121212", "min-height": "100vh"})

# تنظیم layout
app.layout = create_professional_layout()

# Callback برای نمودار اصلی
@app.callback(
    Output("main-live-chart", "figure"),
    Input("main-chart-interval", "n_intervals"),
    Input("main-chart-pair", "value"),
    Input("main-chart-timeframe", "value")
)
def update_main_chart(n_intervals, selected_pair, timeframe):
    """بروزرسانی نمودار اصلی"""
    try:
        # داده‌های نمونه برای نمایش
        dates = pd.date_range(end=datetime.now(), periods=100, freq='1min')
        prices = 50000 + np.cumsum(np.random.randn(100) * 100)
        volumes = np.random.uniform(1000, 5000, 100)
        
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                           vertical_spacing=0.05,
                           row_heights=[0.7, 0.3])
        
        # نمودار قیمت
        fig.add_trace(
            go.Candlestick(
                x=dates,
                open=prices[:-1],
                high=prices + np.random.uniform(0, 200, len(prices)),
                low=prices - np.random.uniform(0, 200, len(prices)),
                close=prices,
                name="Price"
            ), row=1, col=1
        )
        
        # نمودار حجم
        fig.add_trace(
            go.Bar(x=dates, y=volumes, name="Volume", marker_color='rgba(100, 149, 237, 0.5)'),
            row=2, col=1
        )
        
        fig.update_layout(
            title=f"Live Chart - {selected_pair} ({timeframe})",
            showlegend=False,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis_rangeslider_visible=False
        )
        
        return fig
    except Exception as e:
        logger.error(f"Error updating chart: {str(e)}")
        return go.Figure()

# Callback برای وضعیت سریع
@app.callback(
    [Output("quick-api-status", "children"),
     Output("quick-api-status", "style"),
     Output("quick-vpn-status", "children"),
     Output("quick-vpn-status", "style"),
     Output("quick-ai-status", "children"),
     Output("quick-ai-status", "style"),
     Output("quick-pairs-count", "children"),
     Output("quick-memory", "children"),
     Output("quick-time", "children")],
    Input("main-chart-interval", "n_intervals")
)
def update_quick_status(n_intervals):
    """بروزرسانی وضعیت‌های سریع"""
    # شبیه‌سازی وضعیت‌ها
    api_status = "Connected" if n_intervals % 3 != 0 else "Connecting"
    api_color = "green" if api_status == "Connected" else "orange"
    
    vpn_status = "Connected" if n_intervals % 5 != 0 else "Disconnected"
    vpn_color = "green" if vpn_status == "Connected" else "red"
    
    ai_status = "Active"
    ai_color = "green"
    
    pairs_count = f"{n_intervals % 10} Active"
    
    memory_percent = psutil.virtual_memory().percent
    current_time = datetime.now().strftime("%H:%M:%S")
    
    return (
        api_status, {"color": api_color, "fontSize": "12px"},
        vpn_status, {"color": vpn_color, "fontSize": "12px"},
        ai_status, {"color": ai_color, "fontSize": "12px"},
        pairs_count, {"color": "white", "fontSize": "12px"},
        f"{memory_percent}%", {"color": "white", "fontSize": "12px"},
        current_time, {"color": "white", "fontSize": "12px"}
    )

# Callback برای Modal API
@app.callback(
    Output("api-modal", "is_open"),
    [Input("open-api-modal", "n_clicks"),
     Input("close-api-modal", "n_clicks"),
     Input("add-api-btn", "n_clicks")],
    [State("api-modal", "is_open")]
)
def toggle_api_modal(open_clicks, close_clicks, add_clicks, is_open):
    """کنترل Modal افزودن API"""
    if open_clicks or close_clicks or add_clicks:
        return not is_open
    return is_open

# Callback برای افزودن API
@app.callback(
    Output("api-connections-panel", "children"),
    Input("add-api-btn", "n_clicks"),
    [State("new-api-name", "value"),
     State("new-api-type", "value"),
     State("new-api-url", "value"),
     State("new-api-key", "value"),
     State("new-api-secret", "value"),
     State("new-api-use-vpn", "value")]
)
def add_new_api(n_clicks, name, api_type, url, key, secret, use_vpn):
    """افزودن API جدید"""
    if not n_clicks:
        # نمایش APIهای موجود
        return html.Div([
            html.Small("Binance API - Connected", style={"color": "green"}),
            html.Br(),
            html.Small("MT4 Demo - Disconnected", style={"color": "red"})
        ])
    
    if not all([name, api_type, url, key, secret]):
        return html.Div("Please fill all fields", style={"color": "red"})
    
    # شبیه‌سازی افزودن API
    return html.Div([
        html.Small(f"{name} - Added Successfully", style={"color": "green"}),
        html.Br(),
        html.Small(f"Type: {api_type}", style={"color": "white", "fontSize": "10px"})
    ])

# Callback برای دانلود داده‌های تاریخی
@app.callback(
    Output("download-status", "children"),
    Input("download-hist-btn", "n_clicks"),
    [State("hist-symbol", "value"),
     State("hist-timeframe", "value"),
     State("hist-start-date", "date"),
     State("hist-end-date", "date")],
    prevent_initial_call=True
)
def download_historical_data(n_clicks, symbol, timeframe, start_date, end_date):
    """دانلود داده‌های تاریخی"""
    if not all([symbol, timeframe, start_date, end_date]):
        return html.Div("Please select all parameters", style={"color": "red"})
    
    try:
        # شبیه‌سازی دانلود
        return html.Div([
            html.Small(f"📥 Downloading {symbol} data...", style={"color": "orange"}),
            html.Br(),
            html.Small(f"Timeframe: {timeframe} | Period: {start_date} to {end_date}", 
                      style={"color": "gray", "fontSize": "10px"})
        ])
    except Exception as e:
        return html.Div(f"❌ Error: {str(e)}", style={"color": "red"})

# اجرای سرور
if __name__ == '__main__':
    logger.info("🚀 Starting Professional Dashboard...")
    app.run(debug=True, host='0.0.0.0', port=8050, use_reloader=False)