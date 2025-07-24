# D:\AI\AI_Trading_System_ki\ui\dashboard_main.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import requests

# محلی‌سازی logger
def get_logger(name: str):
    import logging
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

log = get_logger("dashboard")

def run_dashboard(cfg: dict):
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.FLATLY],
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    )
    app.title = cfg["app"]["name"]

    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Backtest", href="/backtest")),
            dbc.NavItem(dbc.NavLink("VPN", href="/vpn")),
            dbc.NavItem(dbc.NavLink("AI Strategy", href="/ai")),
        ],
        brand=cfg["app"]["name"],
        brand_href="/",
        color="primary",
        dark=True,
    )

    app.layout = dbc.Container(
        [
            dcc.Location(id="url", refresh=False),
            navbar,
            dbc.Row(dbc.Col(html.Div(id="page-content"), width=12)),
            dcc.Interval(id="status-interval", interval=5000, n_intervals=0),
        ],
        fluid=True,
    )

    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def display_page(pathname):
        if pathname == "/backtest":
            return backtest_layout(cfg)
        elif pathname == "/vpn":
            return vpn_layout(cfg)
        elif pathname == "/ai":
            return ai_layout()
        else:
            return home_layout()

    @app.callback(
        Output("backtest-result", "children"),
        Input("run-backtest", "n_clicks"),
        State("input-cash", "value"),
        State("input-pair", "value"),
    )
    def run_backtest(n, cash, pair):
        if not n:
            raise dash.exceptions.PreventUpdate
        # engine = BacktestEngine(cfg)
        # stats = engine.run(pair, initial_cash=cash)
        stats = {"status": "Backtest completed", "pair": pair, "cash": cash}
        return html.Pre(str(stats))

    @app.callback(
        Output("rl-status-output", "children"),
        [Input("btn-train-rl", "n_clicks"),
         Input("btn-backtest-rl", "n_clicks"),
         Input("btn-replay-rl", "n_clicks")],
        prevent_initial_call=True
    )
    def handle_rl_buttons(n1, n2, n3):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        btn = ctx.triggered[0]["prop_id"].split('.')[0]
        url = "http://localhost:8000"

        try:
            if btn == "btn-train-rl":
                res = requests.post(f"{url}/retrain/strategy/rl/train")
            elif btn == "btn-backtest-rl":
                res = requests.post(f"{url}/retrain/strategy/rl/backtest")
            elif btn == "btn-replay-rl":
                res = requests.post(f"{url}/retrain/strategy/rl/replay")
            else:
                return "❌ Unknown button"

            if res.status_code == 200:
                return f"✅ {res.json().get('status', 'Success')}"
            else:
                return f"❌ Error: {res.status_code} – {res.text}"
        except Exception as e:
            return f"❌ Exception: {e}"

    # ✅ تغییر این خط:
    app.run(debug=True, host='0.0.0.0', port=8050, use_reloader=False)

def home_layout():
    return dbc.Container(
        [
            html.H2("System Status"),
            dbc.Row(
                [
                    dbc.Col(dbc.Card(dbc.CardBody("VPN Server: ✅"), color="success", inverse=True), md=4),
                    dbc.Col(dbc.Card(dbc.CardBody("API Connection: ✅"), color="success", inverse=True), md=4),
                    dbc.Col(dbc.Card(dbc.CardBody("Last Backtest: 2 min ago"), color="info", inverse=True), md=4),
                ]
            ),
        ]
    )

def backtest_layout(cfg):
    return dbc.Container(
        [
            html.H2("Quick Backtest"),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label("Initial Capital (USDT)"),
                            dbc.Input(id="input-cash", type="number", value=10000, min=100),
                        ],
                        md=4,
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Pair"),
                            dcc.Dropdown(
                                id="input-pair",
                                options=[{"label": "BTC/USDT", "value": "BTC/USDT"}],
                                value="BTC/USDT",
                            ),
                        ],
                        md=4,
                    ),
                    dbc.Col(
                        dbc.Button("Run", id="run-backtest", color="primary", className="mt-4"),
                        md=4,
                    ),
                ]
            ),
            html.Hr(),
            html.Div(id="backtest-result"),
        ]
    )

def vpn_layout(cfg):
    return dbc.Container(
        [
            html.H2("VPN Manager"),
            dbc.Button("Refresh Servers", id="refresh-vpn", color="secondary", className="mb-3"),
            html.Div(id="vpn-status", children="(VPN status coming soon...)"),
        ]
    )

def ai_layout():
    return dbc.Container([
        html.H2("AI Strategy Control (RL-based)"),
        dbc.Row([
            dbc.Col(dbc.Button("Train Model", id="btn-train-rl", color="primary", className="me-2"), md=4),
            dbc.Col(dbc.Button("Run Backtest", id="btn-backtest-rl", color="secondary", className="me-2"), md=4),
            dbc.Col(dbc.Button("Replay Market", id="btn-replay-rl", color="info"), md=4),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(html.Div(id="rl-status-output"))
        ])
    ])

# برای تست مستقیم
if __name__ == "__main__":
    cfg = {
        "app": {
            "name": "AI Trading Dashboard",
            "debug": True,
            "host": "0.0.0.0",
            "port": 8050
        },
        "pairs": [
            {"symbol": "BTC/USDT"},
            {"symbol": "ETH/USDT"}
        ]
    }
    run_dashboard(cfg)