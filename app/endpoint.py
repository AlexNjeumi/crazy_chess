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
from app.services.moves import get_legal_moves

from db.schemas import Game
router = APIRouter(prefix="/api/crazy-chess", tags=["crazy-chess"])

from pydantic import BaseModel

class NewGameRequest(BaseModel):
    rows: int
    columns: int
    num_effects: int
    effects: list[str]


@router.post("/new-game")
async def new_game(payload: NewGameRequest, db_session: AsyncSession = Depends(get_db_session)):

    print('SUCCESSFULLY RECEIVED NEW GAME REQUEST')
    board = create_board(payload.rows, payload.columns)
    new_game = Game(board_state=board, effects=payload.effects, num_effects=payload.num_effects)
    db_session.add(new_game)
    await db_session.commit()
    await db_session.refresh(new_game)

    return {"game_id": new_game.id, "board_state": new_game.board_state, "effects": await get_random_effects(db_session, new_game.id, payload.num_effects)}

@router.get("/get-effects")
async def get_effects(game_id: int = Query(...), db_session: AsyncSession = Depends(get_db_session)):

    selected_effects = await get_random_effects(db_session, game_id)
    return selected_effects


@router.get("/legal-moves")
async def legal_moves(game_id: int = Query(...), position: tuple = Query(...), db_session: AsyncSession = Depends(get_db_session)):

    board_state = await get_board_state(game_id, db_session)
    if board_state is None:
        raise HTTPException(status_code=404, detail="Game not found")
    moves = get_legal_moves(board_state, position[0], position[1])
    return {"legal_moves": moves}


@router.get("/get-board-state")
async def get_board_state(game_id: int = Query(...), db_session: AsyncSession = Depends(get_db_session)):
    from app.services.get_board_state import get_board_state
    board_state = await get_board_state(game_id, db_session)
    if board_state is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"board_state": board_state}



@router.post("/apply-effect")
async def apply_effect(game_id: int = Form(...), position: tuple = Form(...), effect: str = Form(...), db_session: AsyncSession = Depends(get_db_session)):
    pass

@router.post("/move")
async def move_piece(old_position: tuple = Form(...), new_position: tuple = Form(...), game_id: int = Form(...), db_session: AsyncSession = Depends(get_db_session)):
    pass
