from effects import freeze

def apply_effect(effect,board, pos):

 

    if effect.lower() == 'freeze':
        print('applying ffreeze...')
        board = freeze.freeze(board, pos)


    return board