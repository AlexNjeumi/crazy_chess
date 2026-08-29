import pygame
from app.services.setup import WHITE_FILL,WHITE_TEXT, WIDTH,PANEL_WIDTH,HEIGHT,STATUS_HEIGHT, BG_STATUS,BLACK_FILL,BLACK_TEXT,BOARD_SIZE, SELECT_COLOR,SQ,STATUS_TEXT, FPS, LIGHT, DARK,MOVE_DOT_COLOR, CAPTURE_RING, FROZEN_COLOR

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

        if effect == selected_effect:
            button_color = (100, 150, 100)
        else:
            button_color = (70, 70, 70)

        pygame.draw.rect(
            screen,
            button_color,
            (button_x, button_y, button_width, button_height),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (180, 180, 180),
            (button_x, button_y, button_width, button_height),
            2,
            border_radius=10
        )

        text = status_font.render(effect, True, (255, 255, 255))

        text_rect = text.get_rect(
            center=(
                button_x + button_width // 2,
                button_y + button_height // 2
            )
        )

        screen.blit(text, text_rect)
