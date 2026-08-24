from effects import freeze, heal, shield

def apply_effect(effect,board, pos):

 

    if effect.lower() == 'freeze':
        # print('applying ffreeze...')
        board = freeze.freeze(board, pos)
    elif effect.lower() == 'heal':
        # print('applying ffreeze...')
        board = heal.heal(board, pos)
    elif effect.lower() == 'shield':
        # print('applying ffreeze...')
        board = shield.shield(board, pos)



    return board