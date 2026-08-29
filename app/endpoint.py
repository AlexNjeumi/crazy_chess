from fastapi import FastAPI
from fastapi import APIRouter, Depends, Form, BackgroundTasks, Query, Response, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.connection import get_db_session
import json
import os
router = APIRouter(prefix="/api/crazy-chess", tags=["crazy-chess"])

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