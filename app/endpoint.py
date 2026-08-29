import random

from fastapi import FastAPI
from fastapi import APIRouter, Depends, Form, BackgroundTasks, Query, Response, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.create_board import create_board
from db.connection import get_db_session
import json
import os
import random
from app.services.create_board import create_board
from app.services.get_effects import get_random_effects

from db.schemas import Games
router = APIRouter(prefix="/api/crazy-chess", tags=["crazy-chess"])


@router.post("/new-game")
async def new_game(effects: list[str] = Form(...), num_effects: int = Form(...), db_session: AsyncSession = Depends(get_db_session)):


    board = create_board()
    new_game = Games(board_state=board, effects=effects)
    db_session.add(new_game)
    await db_session.commit()
    await db_session.refresh(new_game)

    return {"game_id": new_game.id, "board_state": new_game.board_state, "effects": get_random_effects(num_effects)}

@router.get("/get-effects")
async def get_effects(num: int = Form(...), db_session: AsyncSession = Depends(get_db_session)):


    selected_effects = get_random_effects(num)
    return selected_effects

@router.post("/apply-effect")
async def apply_effect(game_id: int = Form(...), position: tuple = Form(...), effect: str = Form(...), db_session: AsyncSession = Depends(get_db_session)):
    pass

@router.post("/move")
async def move_piece():
    pass




# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}