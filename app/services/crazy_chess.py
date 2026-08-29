import pygame
import sys
import copy
import os
import random
from app.services.moves import get_legal_moves, get_raw_moves, make_move, has_any_legal_move, find_king, opposite, is_in_check
pygame.init()
from app.services.apply_effect import apply_effect
from app.services.setup import WHITE_FILL,WHITE_TEXT, WIDTH,PANEL_WIDTH,HEIGHT,STATUS_HEIGHT, BG_STATUS,BLACK_FILL,BLACK_TEXT,BOARD_SIZE, SELECT_COLOR,SQ,STATUS_TEXT, FPS, LIGHT, DARK,MOVE_DOT_COLOR, CAPTURE_RING, FROZEN_COLOR


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
piece_font = pygame.font.SysFont("arial", 30, bold=True)
status_font = pygame.font.SysFont("arial", 22, bold=True)

LETTERS = {'p': 'P', 'n': 'N', 'b': 'B', 'r': 'R', 'q': 'Q', 'k': 'K'}

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

future_effect = ['Warp', 'No Cowards', 'Time Bomb', 'Swap', 'Frenzy', 'Magnet', 'Serial Killer']
selected_effects = random.sample(EFFECTS, 3)

ICON_SIZE = 40

EFFECT_ICONS = {}
for filename in os.listdir("effect_icons"):
    if filename.endswith(".png"):
        effect_name = os.path.splitext(filename)[0].lower()
        effect_name = effect_name.replace('_', ' ')

        image = pygame.image.load(
            os.path.join("effect_icons", filename)
        ).convert_alpha()

        image = pygame.transform.smoothscale(
            image,
            (ICON_SIZE, ICON_SIZE)
        )

        EFFECT_ICONS[effect_name] = image
        print('Loaded ', effect_name.capitalize())

PIECE_ICONS = {}
t = { 'rook' : 'r', 'pawn' : 'p', 'king' : 'k', 'knight' : 'n', 'bishop' : 'b', 'queen' : 'q'}

for filename in os.listdir("piece_icons"):
    if filename.endswith(".png"):
        piece_name = os.path.splitext(filename)[0].lower()
        piece_name = piece_name.replace('_', ' ')

        image = pygame.image.load(
            os.path.join("piece_icons", filename)
        ).convert_alpha()

        image = pygame.transform.smoothscale(
            image,
            (ICON_SIZE, ICON_SIZE)
        )
        PIECE_ICONS[t[piece_name]] = image
        print('Loaded ', piece_name.capitalize())

def draw_effect_panel(effects, selected_effect):
    panel_x = BOARD_SIZE

    # Panel background
    pygame.draw.rect(
        screen,
        (45, 45, 45),
        (panel_x, 0, PANEL_WIDTH, HEIGHT)
    )

    # Title
    title = status_font.render("Effects", True, (255, 255, 255))
    title_rect = title.get_rect(
        center=(panel_x + PANEL_WIDTH // 2, 40)
    )
    screen.blit(title, title_rect)

    # Effect buttons
    button_width = PANEL_WIDTH - 40
    button_height = 80
    button_x = panel_x + 20
    start_y = 100
    gap = 20

    for i, effect in enumerate(effects):

        button_y = start_y + i * (button_height + gap)

        pygame.draw.rect(
            screen,
            (70, 70, 70),
            (button_x, button_y, button_width, button_height),
            border_radius=10
        )

        # Get icon
        icon = EFFECT_ICONS.get(effect.lower())

        if icon is not None:

            icon_rect = icon.get_rect(
                midleft=(button_x + 10,
                        button_y + button_height // 2)
            )

            screen.blit(icon, icon_rect)

        # Effect name
        text = status_font.render(
            effect,
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(
            midleft=(
                button_x + 60,
                button_y + button_height // 2
            )
        )

        screen.blit(text, text_rect)

class Piece:
    def __init__(self, team, ptype):
        self.team = team      # 'w' or 'b'
        self.type = ptype     # 'p','n','b','r','q','k'
        self.has_moved = False
        self.effects = {'shield': 0,
                        'freeze' : 0}
        self.message = 'normal'


def create_board():
    board = [[None] * 8 for _ in range(8)]
    back_row = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
    for col in range(8):
        board[0][col] = Piece('b', back_row[col])
        board[1][col] = Piece('b', 'p')
        board[6][col] = Piece('w', 'p')
        board[7][col] = Piece('w', back_row[col])
    return board


# def draw_board(board, selected, legal_moves, turn, status_msg):
def draw_board(
    board,
    selected,
    legal_moves,
    turn,
    status_msg,
    effects,
    selected_effect
):
    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, (col * SQ, row * SQ, SQ, SQ))

    if selected is not None:
        sx, sy = selected
        piece = board[sy][sx]
        # if 'freeze' in piece.power_up:
        #     pygame.draw.rect(screen, SELECT_COLOR, (sx * SQ, sy * SQ, SQ, SQ))
        # else:
        pygame.draw.rect(screen, SELECT_COLOR, (sx * SQ, sy * SQ, SQ, SQ))

    for (mx, my) in legal_moves:
        center = (mx * SQ + SQ // 2, my * SQ + SQ // 2)
        if board[my][mx] is not None:
            pygame.draw.circle(screen, CAPTURE_RING, center, SQ // 2 - 4, 4)
        else:
            pygame.draw.circle(screen, MOVE_DOT_COLOR, center, 10)

    for row in range(8):
        for col in range(8):
            p = board[row][col]
            if p is not None:
                center = (col * SQ + SQ // 2, row * SQ + SQ // 2)
                fill = WHITE_FILL if p.team == 'w' else BLACK_FILL
                text_color = WHITE_TEXT if p.team == 'w' else BLACK_TEXT
                pygame.draw.circle(screen, fill, center, SQ // 2 - 6)
                pygame.draw.circle(screen, (0, 0, 0), center, SQ // 2 - 6, 2)
                icon = PIECE_ICONS.get(p.type.lower())
                
                if icon is not None:
        
                    icon_rect = icon.get_rect(
                        center=(col * SQ + SQ // 2 ,
                                row * SQ + SQ // 2)
                    )
        
                    screen.blit(icon, icon_rect)
                # label = piece_font.render(LETTERS[p.type], True, text_color)
                # screen.blit(label, label.get_rect(center=center))

    pygame.draw.rect(screen, BG_STATUS, (0, BOARD_SIZE, WIDTH, STATUS_HEIGHT))
    turn_text = "White" if turn == 'w' else "Black"
    msg = status_msg if status_msg else f"{turn_text} to move"
    text = status_font.render(msg, True, STATUS_TEXT)
    screen.blit(text, (10, BOARD_SIZE + STATUS_HEIGHT // 2 - text.get_height() // 2))
    draw_effect_panel(effects, selected_effect)


def main():
    board = create_board()
    turn = 'w'
    selected = None
    legal_moves = []
    game_over = False
    status_msg = ""

    selected_effect = None
    effects = random.sample(EFFECTS, 3)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:

                mx, my = event.pos

                # -------------------------
                # Effect panel
                # -------------------------

                if mx >= BOARD_SIZE:

                    button_width = PANEL_WIDTH - 40
                    button_height = 80
                    button_x = BOARD_SIZE + 20
                    start_y = 100
                    gap = 20

                    for i, effect in enumerate(effects):

                        button_y = start_y + i * (button_height + gap)
                        rect = pygame.Rect(
                            button_x,
                            button_y,
                            button_width,
                            button_height
                        )

                        if rect.collidepoint(mx, my):
                            selected_effect = effect
                            status_msg = f"Select piece to {effect}"
                            print("Selected effect:", selected_effect)
                # -------------------------
                # Chess board
                # -------------------------

                elif my < BOARD_SIZE:

                    col, row = mx // SQ, my // SQ

                    if selected_effect is not None and selected_effect != 'Double Move':

                        board = apply_effect(
                            selected_effect,
                            board,
                            (col, row)
                        )
                        print(selected_effect)
                        print(board[row][col].effects)
                        print(board[row][col].message)
                        print(board[row][col].type)
                        print(f'Col : {col}, Row: {row}')
                        status_msg = f"{selected_effect} applied!"

                        selected_effect = None

                        continue
                    if selected is None:
                        p = board[row][col]
                        if p is not None and p.team == turn:
                            selected = (col, row)
                            legal_moves = get_legal_moves(board,col,row)

                    else:
                        if (col, row) in legal_moves:
                            make_move(
                                board,
                                selected,
                                (col, row)
                            )

                            
                            
                            turn = opposite(turn) if selected_effect != 'Double Move' else turn
                            effects = random.sample(EFFECTS, 3)
                            selected_effect = None
                            selected = None
                            legal_moves = []

                            if is_in_check(board, turn):
                                if not has_any_legal_move(board, turn):
                                    winner = 'White' if turn == 'b' else 'Black'
                                    status_msg = f"Checkmate! {winner} wins"
                                    game_over = True
                                else:
                                    who = 'White' if turn == 'w' else 'Black'
                                    status_msg = f"{who} is in check"
                            else:
                                if not has_any_legal_move(board, turn):
                                    status_msg = "Stalemate!"
                                    game_over = True
                                else:
                                    status_msg = ""
                        else:
                            p = board[row][col]
                            if p is not None and p.team == turn:
                                selected = (col, row)
                                legal_moves = get_legal_moves(board, col, row)
                            else:
                                selected = None
                                legal_moves = []

        draw_board(board,selected,legal_moves,turn,status_msg,effects,selected_effect)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()