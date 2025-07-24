# D:\AI\AI_Trading_System_ki\app.py
import os
import yaml
import threading
import uvicorn
from utils.logger import setup_logger
from api.main_api import create_fastapi_app
from ui.dashboard_main import run_dashboard
from utils.vpn_manager import VPNManager

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_fastapi(cfg):
    fast_app = create_fastapi_app(cfg)
    uvicorn.run(
        fast_app,
        host=cfg["app"]["host"],
        port=8000,
        log_level="info",
    )

def main():
    cfg = load_config()
    setup_logger(cfg["paths"]["log_dir"])

    vpn = VPNManager(cfg["vpn"])
    vpn.start_monitor()

    # FastAPI در thread جدا
    api_thread = threading.Thread(
        target=run_fastapi,
        args=(cfg,),
        daemon=True,
    )
    api_thread.start()

    # Dash در thread اصلی
    run_dashboard(cfg)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()