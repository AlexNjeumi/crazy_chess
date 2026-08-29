
class Piece:
    def __init__(self, team, ptype):
        self.team = team      # 'w' or 'b'
        self.type = ptype     # 'p','n','b','r','q','k'
        self.has_moved = False
        self.effects = {'shield': 0,
                        'freeze' : 0}
        self.message = 'normal'

class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.piece = None
        self.effects = None

def create_board(rows=8, cols=8):
    # board = [[None] * cols for _ in range(rows)]
    board = [[Square(x, y) for x in range(cols)] for y in range(rows)]
    back_row = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
    for col in range(8):
        board[0][col].piece = Piece('b', back_row[col])
        board[1][col].piece = Piece('b', 'p')
        board[6][col].piece = Piece('w', 'p')
        board[7][col].piece = Piece('w', back_row[col])
    return board
