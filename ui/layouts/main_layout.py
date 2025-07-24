# D:\AI\AI_Trading_System_ki\ui\layouts/main_layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc

def create_main_layout():
    """ایجاد لایه اصلی داشبورد"""
    return dbc.Container([
        # هدر
        dbc.Row([
            dbc.Col([
                html.H2("📈 AI Trading System Dashboard", className="text-center text-primary"),
                html.Hr()
            ], width=12)
        ]),
        
        # تب‌ها
        dbc.Tabs([
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        html.H4("🎛️ Strategy Panel"),
                        html.P("مدیریت استراتژی‌های معاملاتی")
                    ], width=12)
                ])
            ], label="استراتژی", tab_id="tab-strategy"),
            
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        html.H4("🌐 API Panel"),
                        html.P("مدیریت اتصال به صرافی‌ها")
                    ], width=12)
                ])
            ], label="API", tab_id="tab-api"),
            
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        html.H4("🔒 VPN Panel"),
                        html.P("مدیریت اتصالات امن")
                    ], width=12)
                ])
            ], label="VPN", tab_id="tab-vpn"),
            
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        html.H4("📊 Analytics Panel"),
                        html.P("تحلیل عملکرد سیستم")
                    ], width=12)
                ])
            ], label="تحلیل", tab_id="tab-analytics"),
            
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        html.H4("📝 Logs Panel"),
                        html.P("مشاهده لاگ‌های سیستم")
                    ], width=12)
                ])
            ], label="لاگ‌ها", tab_id="tab-logs"),
        ], id="tabs", active_tab="tab-strategy"),
        
        # محتوای تب‌ها
        html.Div(id="tab-content"),
        
        # فوتر
        dbc.Row([
            dbc.Col([
                html.Hr(),
                html.P("© 2025 AI Trading System - Qwen-3", className="text-center text-muted")
            ], width=12)
        ])
    ], fluid=True)