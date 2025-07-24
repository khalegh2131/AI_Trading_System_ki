# D:\AI\AI_Trading_System_ki\ui\callbacks/vpn_callbacks.py

from dash import Input, Output, State, callback

def register_vpn_callbacks(app):
    """ثبت کال‌بک‌های پنل VPN"""
    
    @app.callback(
        Output("vpn-status", "children"),
        Output("vpn-status", "style"),
        Input("connect-vpn-btn", "n_clicks"),
        Input("disconnect-vpn-btn", "n_clicks"),
        State("vpn-servers", "value"),
        prevent_initial_call=True
    )
    def toggle_vpn(connect_clicks, disconnect_clicks, server):
        """تغییر وضعیت VPN"""
        ctx = callback.context
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == "connect-vpn-btn":
            if not server:
                return "لطفاً یک سرور انتخاب کنید.", {"color": "red"}
            return f"✅ متصل به سرور {server.upper()}", {"color": "green"}
        elif button_id == "disconnect-vpn-btn":
            return "قطع شده", {"color": "red"}
        
        return "قطع شده", {"color": "red"}