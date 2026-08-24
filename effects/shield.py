import pygame
# from ..setup import BOARD_SIZE,SQ
BOARD_SIZE = 640
SQ = 80
def shield(board, pos):
    col, row = pos

    p = board[row][col]

    if p is not None:
        print('before shield')
        print(f'Col : {col}, Row: {row}')

        p.effects['shield'] += 1
        p.message = 'hello'
    else:
        print('could not do shield')
        print(f'Col : {col}, Row: {row}')
    board[row][col] = p  

    return board