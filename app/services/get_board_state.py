
from sqlalchemy import select

from select import select


async def get_board_state(game_id: int, db_session):
    from db.schemas import Game

    stmt = select(Game.board_state).where(Game.id == game_id)
    result = await db_session.execute(stmt)
    board_state = result.scalar_one_or_none()
    return board_state