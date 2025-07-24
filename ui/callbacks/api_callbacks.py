# D:\AI\AI_Trading_System_ki\ui\callbacks/api_callbacks.py

from dash import Input, Output, State, callback
import json

def register_api_callbacks(app):
    """ثبت کال‌بک‌های پنل API"""
    
    @app.callback(
        Output("api-status", "children"),
        Input("add-api-btn", "n_clicks"),
        State("api-name", "value"),
        State("api-key", "value"),
        State("api-secret", "value"),
        State("api-type", "value"),
        prevent_initial_call=True
    )
    def add_api(n_clicks, name, key, secret, api_type):
        """افزودن API جدید"""
        if not all([name, key, secret, api_type]):
            return "لطفاً تمام فیلدها را پر کنید."
            
        # در اینجا می‌توانید API را ذخیره کنید
        return f"✅ API '{name}' با موفقیت اضافه شد."