import pygame
# from ..setup import BOARD_SIZE,SQ
BOARD_SIZE = 640
SQ = 80
def freeze(board, pos):
    col, row = pos

    p = board[row][col]

    if p is not None:
        print('before heal')
        print(f'Col : {col}, Row: {row}')

        if p.effects['shield'] < 1:
            p.effects['freeze'] += 1
        else:
            p.effects['shield'] = max(0, p.effects['freeze'] -1 )
        p.message = 'hello'
    else:
        print('could not do heal')
        print(f'Col : {col}, Row: {row}')
    board[row][col] = p  

    return board