# D:\AI\AI_Trading_System_ki\ui\components/analytics_panel.py

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go

def create_analytics_panel():
    """ایجاد پنل تحلیل‌ها"""
    # نمودار نمونه
    fig = go.Figure(data=go.Scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13]))
    fig.update_layout(title="نمودار عملکرد")
    
    return dbc.Card([
        dbc.CardHeader("تحلیل عملکرد"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=fig)
                ], width=12)
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.H5("آمار کلی:"),
                    html.Ul([
                        html.Li("سود کل: 0.00%"),
                        html.Li("تعداد معاملات: 0"),
                        html.Li("درصد موفقیت: 0.00%")
                    ])
                ], width=6),
                dbc.Col([
                    html.H5("تحلیل احساسات:"),
                    html.Ul([
                        html.Li("اخبار مثبت: 0"),
                        html.Li("اخبار منفی: 0"),
                        html.Li("اخبار خنثی: 0")
                    ])
                ], width=6)
            ])
        ])
    ])