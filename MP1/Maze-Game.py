# %% [markdown]
# Libraries

# %%
import pygame
import sys
import random
import time

# %% [markdown]
# Initialize Pygame

# %%
pygame.init()

# %% [markdown]
# Constants

# %%
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 30
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
FPS = 30  # Adjust the FPS for slower movement

# %% [markdown]
# Colors

# %%
WHITE = (255, 255, 255)
GRAY = (181, 176, 173)
DARK_BLUE = (3, 102, 150)
MEDIUM_BLUE = (7, 87, 91)
LIGHT_BLUE = (173, 216, 230)
RED = (255, 0, 0)

# %% [markdown]
# Initialize clock

# %%
clock = pygame.time.Clock()

# %% [markdown]
# Initialize serial communication with Arduino

# %%
# Add your code here to connect the python to the serial port.

# %% [markdown]
# Maze generation - DO NOT CHANGE THIS FUNCTION!

# %%
def generate_maze():
    maze = [[0] * COLS for _ in range(ROWS)]
    stack = []
    start_cell = (1, 1)
    end_cell = (ROWS - 3, COLS - 3)
    stack.append(start_cell)
    maze[start_cell[0]][start_cell[1]] = 1

    while stack:
        current_cell = stack[-1]
        neighbors = [
            (current_cell[0] - 2, current_cell[1]),
            (current_cell[0] + 2, current_cell[1]),
            (current_cell[0], current_cell[1] - 2),
            (current_cell[0], current_cell[1] + 2),
        ]
        unvisited_neighbors = [neighbor for neighbor in neighbors if 0 < neighbor[0] < ROWS - 1 and 0 < neighbor[1] < COLS - 1 and maze[neighbor[0]][neighbor[1]] == 0]

        if unvisited_neighbors:
            chosen_neighbor = random.choice(unvisited_neighbors)
            maze[chosen_neighbor[0]][chosen_neighbor[1]] = 1
            maze[(chosen_neighbor[0] + current_cell[0]) // 2][(chosen_neighbor[1] + current_cell[1]) // 2] = 1
            stack.append(chosen_neighbor)
        else:
            stack.pop()

    return maze, start_cell, end_cell

maze, start_point, end_point = generate_maze()

# Player position
player_row, player_col = start_point

# %% [markdown]
# Game

# %%
# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Read data from MPU-6050 sensor through serial communication
    """
    Add your code here to use the data from serial print for next step.
    """

    # Adjust player position based on MPU-6050 data
    """
    This Code uses "W-A-S-S" keys to move the ball.
    After you read the data, you should change these following conditions and replace them with the ones that changes the position of the ball using the data from the previous step.
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_col > 0 and maze[player_row][player_col - 1] == 1:
        player_col -= 1
    if keys[pygame.K_d] and player_col < COLS - 1 and maze[player_row][player_col + 1] == 1:
        player_col += 1
    if keys[pygame.K_w] and player_row > 0 and maze[player_row - 1][player_col] == 1:
        player_row -= 1
    if keys[pygame.K_s] and player_row < ROWS - 1 and maze[player_row + 1][player_col] == 1:
        player_row += 1

    # Draw maze
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, MEDIUM_BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for row in range(ROWS):
        for col in range(COLS):
            if (row, col) == start_point:
                pygame.draw.rect(screen, LIGHT_BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif (row, col) == end_point:
                pygame.draw.rect(screen, LIGHT_BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw player
    pygame.draw.circle(screen, GRAY, (player_col * CELL_SIZE + CELL_SIZE // 2, player_row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    
    # Check if the player reaches the end point
    if (player_row, player_col) == end_point:
        pygame.display.flip()
        print("Congratulations! You reached the end of the maze.")
        time.sleep(5)
        pygame.quit()
        sys.exit()
    pygame.display.flip()
    clock.tick(FPS)