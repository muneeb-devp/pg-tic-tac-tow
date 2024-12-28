import pygame
from sys import exit
from time import sleep
from typing import Optional, Tuple, List

pygame.init()

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
WIN_LINE_COLOR = (0, 155, 125)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

board: List[List[Optional[str]]] = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]


def draw_lines() -> None:
  # Horizontal lines
  pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
  pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
  # Vertical lines
  pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
  pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures() -> None:
  for row in range(BOARD_ROWS):
    for col in range(BOARD_COLS):
      if board[row][col] == 'O':
        pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
      elif board[row][col] == 'X':
        pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
        pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)


def draw_winning_line(start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> None:
  pygame.draw.line(screen, WIN_LINE_COLOR, start_pos, end_pos, LINE_WIDTH)


def check_win(player: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
  # Vertical win check
  for col in range(BOARD_COLS):
    if board[0][col] == board[1][col] == board[2][col] == player:
      return ((col * SQUARE_SIZE + SQUARE_SIZE // 2, 15), (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 15))
  # Horizontal win check
  for row in range(BOARD_ROWS):
    if board[row][0] == board[row][1] == board[row][2] == player:
      return ((15, row * SQUARE_SIZE + SQUARE_SIZE // 2), (WIDTH - 15, row * SQUARE_SIZE + SQUARE_SIZE // 2))
  # Ascending diagonal win check
  if board[0][0] == board[1][1] == board[2][2] == player:
    return ((15, 15), (WIDTH - 15, HEIGHT - 15))
  # Descending diagonal win check
  if board[2][0] == board[1][1] == board[0][2] == player:
    return ((15, HEIGHT - 15), (WIDTH - 15, 15))
  return None

player = 'X'
game_over = False
draw_lines()

while not game_over:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

    if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
      mouseX, mouseY = event.pos[0] // SQUARE_SIZE, event.pos[1] // SQUARE_SIZE

      if board[mouseY][mouseX] is None:
        board[mouseY][mouseX] = player
        win_line = check_win(player)

        if not win_line: player = 'O' if player == 'X' else 'X'

        draw_figures()

        if win_line:
          draw_winning_line(win_line[0], win_line[1])
          pygame.display.set_caption(f'Player {player} wins!')
          game_over = True
    

  pygame.display.update()
