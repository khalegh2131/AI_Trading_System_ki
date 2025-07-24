# D:\AI\AI_Trading_System_ki\ui\callbacks/strategy_callbacks.py

from dash import Input, Output, State, callback

def register_strategy_callbacks(app):
    """ثبت کال‌بک‌های پنل استراتژی"""
    
    @app.callback(
        Output("strategy-parameters", "children"),
        Input("strategy-dropdown", "value")
    )
    def update_strategy_parameters(selected_strategy):
        """بروزرسانی پارامترهای استراتژی"""
        if not selected_strategy:
            return "لطفاً یک استراتژی انتخاب کنید."
            
        param_map = {
            "dqn": [
                "Epochs: 100",
                "Learning Rate: 0.001",
                "Gamma: 0.95"
            ],
            "ma": [
                "Fast MA Period: 10",
                "Slow MA Period: 50"
            ],
            "rsi": [
                "RSI Period: 14",
                "Overbought Level: 70",
                "Oversold Level: 30"
            ]
        }
        
        params = param_map.get(selected_strategy, [])
        return html.Ul([html.Li(p) for p in params])
    
    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "active_tab")
    )
    def render_tab_content(active_tab):
        """رندر محتوای تب‌ها"""
        from ui.components.strategy_panel import create_strategy_panel
        from ui.components.api_panel import create_api_panel
        from ui.components.vpn_panel import create_vpn_panel
        from ui.components.analytics_panel import create_analytics_panel
        from ui.components.logs_panel import create_logs_panel
        
        if active_tab == "tab-strategy":
            return create_strategy_panel()
        elif active_tab == "tab-api":
            return create_api_panel()
        elif active_tab == "tab-vpn":
            return create_vpn_panel()
        elif active_tab == "tab-analytics":
            return create_analytics_panel()
        elif active_tab == "tab-logs":
            return create_logs_panel()
        return "محتوایی برای این تب وجود ندارد."