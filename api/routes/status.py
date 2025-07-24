# api/routes/status.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_status():
    return {"status": "running", "version": "7.0.0"}