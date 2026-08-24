

def on_board(position):
    if position[0] > -1 and position[1] > -1 and position[0] < 8 and position[1] < 8:
        return True

def is_occupied(position, board):
    if board[position[0]][position[1]] is None:
        return False
    return True

def check_positions(positions, board, piece, check_on_board=False):

    valid_positions = []
    for position in positions:
        if board[position[0]][position[1]] is None:
            valid_positions.append(position)
        elif board[position[0]][position[1]].team != piece.team and piece.name != 'pawn':
            valid_positions.append(position)

    if not valid_positions:
        return None
    else:
        if not check_on_board:
            return valid_positions
        else:
            return [position for position in valid_positions if on_board(position)]


def default_moves(piece, board):
    name = piece.name
    x , y = piece.position
    if name == 'pawn':
        possible_attacks = [[x,y+1], [x, y+2]]
        delta_xs = [1, -1]
        for delta_x in delta_xs:
            if not x+delta_x > 7 and not y+1 > 7:
                if board[x+1,y+1].team != piece.team:
                    possible_attacks.append(board[x+delta_x,y+1])


    elif name == 'knight':
        delta_n = [1,-1]
        delta_m = [3,-3]
        possible_attacks = []
        for n in delta_n:
            for m in delta_m:
                if on_board([x+n,y+m]):
                    possible_attacks.append([x+n,y+m])
                elif on_board([x+m, y+n]):
                    possible_attacks.append([x+n,y+m])


    elif name == 'rook':
        possible_attacks = [[x+n, y] for n in range(-7,8) if n != 0]
        possible_attacks.extend([[x, y+n] for n in range(-7,8) if n != 0])

    elif name == 'bishop':
        possible_attacks = [[x+n, y+n] for n in range(-7,8) if n != 0]
        possible_attacks.extend([[x-n, y+n] for n in range(-7,8) if n != 0])
        possible_attacks.extend([[x+n, y-n] for n in range(-7,8) if n != 0])
        possible_attacks.extend([[x-n, y-n] for n in range(-7,8) if n != 0])

    elif name == 'queen':
        possible_attacks = [[x+n, y] for n in range(-7,8) if n != 0]
        possible_attacks.extend([[x, y+n] for n in range(-7,8) if n != 0])
        possible_attacks.extend([[x+n, y+n] for n in range(-7,8) if n != 0])
        possible_attacks.extend([[x-n, y+n] for n in range(-7,8) if n != 0])
        possible_attacks.extend([[x+n, y-n] for n in range(-7,8) if n != 0])
        possible_attacks.extend([[x-n, y-n] for n in range(-7,8) if n != 0])

    elif name == 'king':
        deltas = [1,0,-1]
        possible_attacks = []
        for n in deltas:
            for m in deltas:
                if n == 0 and m == 0:
                    continue
                else:
                    possible_attacks.append([x+m,y+n])


    valid_positions = check_positions(possible_attacks, board, piece, True)

    return valid_positions

def on_move(piece, new_pos,  board):
    x, y = new_pos
    board[x][y] = piece
    board[piece.position[0]][piece.position[1]] = None
    piece.position = new_pos

    return piece, board
