import random   

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

def get_random_effects(num=3):
    return random.sample(EFFECTS, num)