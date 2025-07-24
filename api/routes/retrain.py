# api/routes/retrain.py
from fastapi import APIRouter
from strategies.strategy_manager import StrategyManager

router = APIRouter()
manager = StrategyManager()

@router.post("/strategy/rl/train")
async def rl_train():
    manager.train()
    return {"status": "Training started"}

@router.post("/strategy/rl/backtest")
async def rl_backtest():
    result = manager.backtest()
    return {"status": "Backtest completed", "result": result}

@router.post("/strategy/rl/replay")
async def rl_replay():
    result = manager.replay()
    return {"status": "Replay started", "result": result}

@router.get("/strategy/rl/status")
async def rl_status():
    return manager.status()
