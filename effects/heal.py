import pygame
# from ..setup import BOARD_SIZE,SQ
BOARD_SIZE = 640
SQ = 80
def heal(board, pos):
    col, row = pos

    p = board[row][col]

    if p is not None:
        print('before heal')
        print(f'Col : {col}, Row: {row}')

        p.effects['freeze'] = max(0, p.effects['freeze'] -1 )
        p.message = 'hello'
    else:
        print('could not do heal')
        print(f'Col : {col}, Row: {row}')
    board[row][col] = p  

    return board