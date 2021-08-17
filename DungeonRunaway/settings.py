from pygame.math import Vector2

# Screen settings, for the game class
WIDTH, HEIGHT = 610, 670
TOP_BOTTOM_PADDING = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_PADDING, HEIGHT-TOP_BOTTOM_PADDING
CELL_WIDTH = MAZE_WIDTH // 28  # Cols
CELL_HEIGHT = MAZE_HEIGHT // 30  # Rows

ROWS = 30
COLS = 28

# colour settings
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
PLAYER_COLOUR = (190, 194, 15)

# player settings
PLAYER_START_POSITION = Vector2(1, 1)


# enemy settings


# FPS settings
FPS = 60

# Start Text Settings
START_TEXT_SIZE = 16
START_TEXT_FONT = 'arial black'
