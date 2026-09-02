import random
from sqlalchemy import select   

EFFECTS = [
    "Shield",
    "Double Move",
    "Double Move",
    "Double Move",
    "Freeze",
    "Freeze",
    "Freeze",
    "Freeze",
    "Heal",
]


future_effects = ['Warp', 'No Cowards', 'Time Bomb', 'Swap', 'Frenzy', 'Magnet', 'Serial Killer']

from db.schemas import Game
async def get_random_effects(db_session, id , num=3):

    stmt = select(Game).where(Game.id == id)
    result = await db_session.execute(stmt)
    game = result.scalar_one_or_none()

    return random.sample(game.effects, game.num_effects) if game else []