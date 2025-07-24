# D:\AI\AI_Trading_System_ki\api\main_api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import status, pause, retrain

def create_fastapi_app(cfg: dict) -> FastAPI:
    """
    ساخت instance FastAPI با CORS و روت‌های ماژولار
    """
    app = FastAPI(
        title=cfg["app"]["name"],
        version=cfg["app"]["version"],
        description="REST API برای کنترل سیستم تریدر هوشمند v7",
    )

    # CORS برای دسترسی داشبورد (در صورت اجرا از مرورگر دیگر)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ثبت روت‌ها
    app.include_router(status.router, prefix="/status", tags=["Status"])
    app.include_router(pause.router, prefix="/pause", tags=["Control"])
    app.include_router(retrain.router, prefix="/retrain", tags=["Control"])

    return app