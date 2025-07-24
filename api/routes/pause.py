# api/routes/pause.py
from fastapi import APIRouter

router = APIRouter()

paused = False

@router.post("/")
def pause_trading():
    global paused
    paused = True
    return {"paused": True}

@router.delete("/")
def resume_trading():
    global paused
    paused = False
    return {"paused": False}