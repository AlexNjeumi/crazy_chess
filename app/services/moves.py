import copy

def in_bounds(pos):
    x, y = pos
    return 0 <= x < 8 and 0 <= y < 8


def opposite(team):
    return 'b' if team == 'w' else 'w'



def pawn_attack_squares(x, y, team):
    direction = -1 if team == 'w' else 1
    attacks = []
    for dx in (-1, 1):
        nx, ny = x + dx, y + direction
        if in_bounds((nx, ny)):
            attacks.append((nx, ny))
    return attacks


def get_raw_moves(board, x, y):
    """Pseudo-legal moves: obeys piece movement + blocking, ignores checks."""
    piece = board[y][x]
    if piece is None:
        return []
    team = piece.team
    moves = []

    if piece.type == 'p':
        direction = -1 if team == 'w' else 1
        start_row = 6 if team == 'w' else 1

        ny = y + direction
        if in_bounds((x, ny)) and board[ny][x] is None:
            moves.append((x, ny))
            ny2 = y + 2 * direction
            if y == start_row and board[ny2][x] is None:
                moves.append((x, ny2))

        for (ax, ay) in pawn_attack_squares(x, y, team):
            target = board[ay][ax]
            if target is not None and target.team != team:
                moves.append((ax, ay))

    elif piece.type == 'n':
        deltas = [(1, 2), (2, 1), (-1, 2), (-2, 1),
                  (1, -2), (2, -1), (-1, -2), (-2, -1)]
        for dx, dy in deltas:
            nx, ny = x + dx, y + dy
            if in_bounds((nx, ny)):
                target = board[ny][nx]
                if target is None or target.team != team:
                    moves.append((nx, ny))

    elif piece.type in ('r', 'b', 'q'):
        directions = []
        if piece.type in ('r', 'q'):
            directions += [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if piece.type in ('b', 'q'):
            directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while in_bounds((nx, ny)):
                target = board[ny][nx]
                if target is None:
                    moves.append((nx, ny))
                else:
                    if target.team != team:
                        moves.append((nx, ny))
                    break
                nx += dx
                ny += dy

    elif piece.type == 'k':
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if in_bounds((nx, ny)):
                    target = board[ny][nx]
                    if target is None or target.team != team:
                        moves.append((nx, ny))

    
    return moves


def get_legal_moves(board, x, y):
    piece = board[y][x]

   
    if piece is None:
        return []

    if piece.effects.get('freeze', 0) > 0:
        return []
    raw = get_raw_moves(board, x, y)
    legal = []
    for (nx, ny) in raw:
        test_board = copy.deepcopy(board)
        moved_piece = test_board[y][x]
        test_board[ny][nx] = moved_piece
        test_board[y][x] = None
        if not is_in_check(test_board, piece.team):
            legal.append((nx, ny))
    return legal


def has_any_legal_move(board, team):
    for y in range(8):
        for x in range(8):
            p = board[y][x]
            if p is not None and p.team == team:
                if get_legal_moves(board, x, y):
                    return True
    return False


def make_move(board, old_pos, new_pos):
    old_x, old_y = old_pos
    new_x, new_y = new_pos
    piece = board[old_y][old_x]
    board[new_y][new_x] = piece
    board[old_y][old_x] = None
    piece.has_moved = True
    if piece.type == 'p' and (new_y == 0 or new_y == 7):
        piece.type = 'q'  # auto-promote to queen



def find_king(board, team):
    for y in range(8):
        for x in range(8):
            p = board[y][x]
            if p is not None and p.type == 'k' and p.team == team:
                return (x, y)
    return None


def is_square_attacked(board, pos, by_team):
    for y in range(8):
        for x in range(8):
            p = board[y][x]
            if p is not None and p.team == by_team:
                if p.type == 'p':
                    if pos in pawn_attack_squares(x, y, by_team):
                        return True
                else:
                    if pos in get_raw_moves(board, x, y):
                        return True
    return False


def is_in_check(board, team):
    king_pos = find_king(board, team)
    if king_pos is None:
        return False
    return is_square_attacked(board, king_pos, opposite(team))

