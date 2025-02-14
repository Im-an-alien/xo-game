import pygame
import sys
import numpy as np
import math
import random
import time

# ------------------------------
# Pygame Setup
# ------------------------------
pygame.init()

# ------------------------------
# Game Constants
# ------------------------------
WIDTH = 700
HEIGHT = 700
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 5
CROSS_WIDTH = 5
SPACE = SQUARE_SIZE // 4

# ------------------------------
# Retro Fonts Setup
# ------------------------------
# Ensure that "retro.ttf" is in your working directory, or change the filename accordingly.
FONT = pygame.font.Font("retro.ttf", 40)
POPUP_FONT = pygame.font.Font("retro.ttf", 50)
BUTTON_FONT = pygame.font.Font("retro.ttf", 35)
BIG_FONT = pygame.font.Font("retro.ttf", 70)

# ------------------------------
# Colors
# ------------------------------
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
BUTTON_COLOR = (174, 240, 234)
BUTTON_HOVER_COLOR = (0, 150, 137)
POPUP_COLOR = (0, 0, 0)
POPUP_BG_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

# ------------------------------
# Screen Setup
# ------------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Most Amazing X O Game Ever")
screen.fill(BG_COLOR)

# ------------------------------
# Board Setup
# ------------------------------
board = np.zeros((BOARD_ROWS, BOARD_COLS))
human_turn = True
game_over = False
winner = None
show_menu = True
menu_done = False  # Global flag for exiting the start menu

# ------------------------------
# Utility Functions
# ------------------------------
def draw_text(text, font, color, x, y):
    """Draw text centered at (x, y)."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, w, h, action=None):
    """Draw a button with a hover effect. If clicked, perform the action."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = BUTTON_HOVER_COLOR if (x < mouse[0] < x + w and y < mouse[1] < y + h) else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    draw_text(text, BUTTON_FONT, TEXT_COLOR, x + w // 2, y + h // 2)
    if click[0] == 1 and (x < mouse[0] < x + w and y < mouse[1] < y + h):
        pygame.time.delay(200)
        if action:
            action()

# ------------------------------
# Animation Functions
# ------------------------------
def animate_winning_line(start, end, color):
    """Animate drawing a winning line from start to end."""
    steps = 30
    for i in range(steps):
        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures()
        inter_x = start[0] + (end[0] - start[0]) * (i + 1) / steps
        inter_y = start[1] + (end[1] - start[1]) * (i + 1) / steps
        pygame.draw.line(screen, color, start, (inter_x, inter_y), 5)
        pygame.display.update()
        pygame.time.delay(20)

# ------------------------------
# Drawing Functions (Grid & Figures)
# ------------------------------
def draw_lines():
    """Draw the Tic Tac Toe grid."""
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), 5)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), 5)

def draw_figures():
    """Draw the X's and O's on the board."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

# ------------------------------
# Game Functions
# ------------------------------
def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    return not any(0 in row for row in board)

def check_win(player):
    """Check if a player has won and animate the winning line if so."""
    global game_over, winner
    # Vertical win
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            draw_vertical_winning_line(col, player)
            pygame.time.delay(500)
            winner = player
            game_over = True
            return True
    # Horizontal win
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            draw_horizontal_winning_line(row, player)
            pygame.time.delay(500)
            winner = player
            game_over = True
            return True
    # Diagonals
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        draw_desc_diagonal(player)
        pygame.time.delay(500)
        winner = player
        game_over = True
        return True
    if all(board[i][BOARD_ROWS - i - 1] == player for i in range(BOARD_ROWS)):
        draw_asc_diagonal(player)
        pygame.time.delay(500)
        winner = player
        game_over = True
        return True
    return False

def restart_game():
    global board, game_over, winner, human_turn, show_menu, menu_done
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    game_over = False
    winner = None
    human_turn = True
    show_menu = False
    screen.fill(BG_COLOR)
    draw_lines()
    pygame.display.update()

def quit_game():
    pygame.quit()
    sys.exit()

# ------------------------------
# CPU AI: Minimax Algorithm
# ------------------------------
def check_win_board(b, player):
    for col in range(BOARD_COLS):
        if b[0][col] == player and b[1][col] == player and b[2][col] == player:
            return True
    for row in range(BOARD_ROWS):
        if b[row][0] == player and b[row][1] == player and b[row][2] == player:
            return True
    if b[0][0] == player and b[1][1] == player and b[2][2] == player:
        return True
    if b[0][2] == player and b[1][1] == player and b[2][0] == player:
        return True
    return False

def is_board_full_board(b):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if b[row][col] == 0:
                return False
    return True

def minimax(b, depth, is_maximizing):
    if check_win_board(b, 2):
        return 1
    if check_win_board(b, 1):
        return -1
    if is_board_full_board(b):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if b[row][col] == 0:
                    b[row][col] = 2
                    score = minimax(b, depth + 1, False)
                    b[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if b[row][col] == 0:
                    b[row][col] = 1
                    score = minimax(b, depth + 1, True)
                    b[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def get_cpu_move():
    best_score = -math.inf
    best_move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move

# ------------------------------
# Winning Line Animations
# ------------------------------
def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    start = (posX, 15)
    end = (posX, HEIGHT - 15)
    animate_winning_line(start, end, (0, 0, 0))

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    start = (15, posY)
    end = (WIDTH - 15, posY)
    animate_winning_line(start, end, (0, 0, 0))

def draw_asc_diagonal(player):
    start = (15, HEIGHT - 15)
    end = (WIDTH - 15, 15)
    animate_winning_line(start, end, (0, 0, 0))

def draw_desc_diagonal(player):
    start = (15, 15)
    end = (WIDTH - 15, HEIGHT - 15)
    animate_winning_line(start, end, (0, 0, 0))

# ------------------------------
# Menus
# ------------------------------
menu_done = False
def start_menu():
    """Show start menu with a play button that has a hover effect."""    
    global menu_done
    menu_done = False
    button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2, 300, 50)
    while not menu_done:
        screen.fill(BG_COLOR)
        draw_text("Ready To Lose?", POPUP_FONT, POPUP_COLOR, WIDTH // 2, HEIGHT // 3)
        draw_button("Let's Play", button_rect.x, button_rect.y, button_rect.width, button_rect.height, action=exit_menu)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

def exit_menu():
    global menu_done
    menu_done = True

def end_popup():
    """Show popup when the game ends."""
    screen.fill(BG_COLOR)
    if winner is None:
        message = "a draw!! You lucky"
    else:
        message = "YOU CHEAT!!" if winner == 1 else "HAHAHAHA YOU LOST"
    draw_text(message, POPUP_FONT, POPUP_COLOR, WIDTH // 2 , HEIGHT // 2 - 30)
    button_restart = pygame.Rect(WIDTH // 3, HEIGHT // 2 + 20, 300, 50)
    button_quit = pygame.Rect(WIDTH // 3, HEIGHT // 2 + 80, 300, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, button_restart, border_radius=10)
    pygame.draw.rect(screen, BUTTON_COLOR, button_quit, border_radius=10)
    draw_text("Try Again?", BUTTON_FONT, TEXT_COLOR, button_restart.centerx, button_restart.centery)
    draw_text("I Quit :((", BUTTON_FONT, TEXT_COLOR, button_quit.centerx, button_quit.centery)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_restart.collidepoint(event.pos):
                    restart_game()
                    waiting = False
                    return
                if button_quit.collidepoint(event.pos):
                    quit_game()

# ------------------------------
# Additional Cheat Functions
# ------------------------------
def ghost_move():
    """Occasionally shift one of the player's moves to a less strategic location."""
    if random.random() < 0.2:  # 20% chance to trigger ghost move
        player_moves = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == 1]
        empty_moves = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == 0]
        if player_moves and empty_moves:
            selected = random.choice(player_moves)
            new_pos = random.choice(empty_moves)
            board[selected[0]][selected[1]] = 0  # Remove player's move
            board[new_pos[0]][new_pos[1]] = 1    # Place it in a new position
            pygame.display.update()
            pygame.time.delay(500)

def flash_effect(rect, color=(255, 0, 0), duration=200):
    """Flash a rectangle area with a color effect."""
    flash_surface = pygame.Surface((rect[2], rect[3]))
    flash_surface.fill(color)
    for alpha in range(255, 0, -15):
        flash_surface.set_alpha(alpha)
        screen.blit(flash_surface, (rect[0], rect[1]))
        pygame.display.update()
        pygame.time.delay(duration // 17)

# ------------------------------
# Main Game Loop
# ------------------------------
start_menu()
draw_lines()
human_turn = True
game_over = False

while True:
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    
    if game_over:
        end_popup()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            clicked_row, clicked_col = mouseY // SQUARE_SIZE, mouseX // SQUARE_SIZE
            if available_square(clicked_row, clicked_col):
                ghost_move()
                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, 1)
                draw_figures()
                if check_win(1):
                    winner = 2
                    game_over = True
                elif is_board_full():
                    game_over = True
                else:
                    move = get_cpu_move()
                    if move is not None:
                        mark_square(move[0], move[1], 2)
                        draw_figures()
                        if check_win(2):
                            game_over = True
                        elif is_board_full():
                            game_over = True
                        pygame.time.delay(500)
                human_turn = True
    pygame.display.update()
