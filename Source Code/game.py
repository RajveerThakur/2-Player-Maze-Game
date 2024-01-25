# Simple Maze Game Using The Recursive Back-Tracker Algorithm
from enum import Enum
import random
import pygame as pg
import sys

# Global Settings
SHOW_DRAW = False  # Show the maze being created
SHOW_FPS = False  # Show frames per second in caption
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 960
# Maze Size: 36 X 30 is max size for screen of 1200 X 1024
MAZE_WIDTH = 36  # (original = 36) in cells
MAZE_HEIGHT = 28  # (original = 28) in cells
CELL_COUNT = MAZE_WIDTH * MAZE_HEIGHT
BLOCK_SIZE = 8  # Pixel size/Wall thickness
PATH_WIDTH = 3  # Width of pathway in blocks
CELL_SIZE = BLOCK_SIZE * PATH_WIDTH + BLOCK_SIZE  # extra BLOCK_SIZE to include wall to east and south of cell
MAZE_WIDTH_PX = CELL_SIZE * MAZE_WIDTH + BLOCK_SIZE  # extra BLOCK_SIZE to include left edge wall
MAZE_HEIGHT_PX = CELL_SIZE * MAZE_HEIGHT + BLOCK_SIZE  # extra BLOCK_SIZE to include top edge wall
MAZE_TOP_LEFT_CORNER = (SCREEN_WIDTH // 2 - MAZE_WIDTH_PX // 2, SCREEN_HEIGHT // 2 - MAZE_HEIGHT_PX // 2)

# Define the colors we'll need
BACK_COLOR = (100, 100, 100)
#WALL_COLOR = (18, 94, 32)
WALL_COLOR = (0, 0, 0)
MAZE_COLOR = (255, 255, 255)
UNVISITED_COLOR = (0, 0, 0)
PLAYER1_COLOR = (255, 0, 0)
PLAYER2_COLOR = (0, 0, 255)
MESSAGE_COLOR = (0, 255, 0)

class CellProp(Enum):
    Path_N = 1
    Path_E = 2
    Path_S = 4
    Path_W = 8
    Visited = 16

class Direction(Enum):
    North = (0, -1)
    East = (1, 0)
    South = (0, 1)
    West = (-1, 0)

class Player(pg.sprite.Sprite):
    def __init__(self, color, x, y, radius):

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Save the start position
        self.start_x = x
        self.start_y = y

        # Create the rectangular image, fill and set background to transparent
        self.image = pg.Surface([radius * 2, radius * 2])
        self.image.fill(MAZE_COLOR)
        self.image.set_colorkey(MAZE_COLOR)

        # Draw our player onto the transparent rectangle
        pg.draw.circle(self.image, color, (radius, radius), radius)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y

class MazeGenerator:
    direction_to_flag = {
        Direction.North: CellProp.Path_N,
        Direction.East: CellProp.Path_E,
        Direction.South: CellProp.Path_S,
        Direction.West: CellProp.Path_W
    }

    opposite_direction = {
        Direction.North: Direction.South,
        Direction.East: Direction.West,
        Direction.South: Direction.North,
        Direction.West: Direction.East
    }

    def __init__(self):
        # Need to initialize pygame before using it
        pg.init()

        # Create a display surface to draw our game on
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Set the title on the window
        pg.display.set_caption('2 Player Maze Game')

        # Use a single list to store 2D array
        self.maze = []
        random.seed()

        # Store maze as image after we create it so that we just have to redraw the image on update
        self.maze_image = None

        # Create players
        self.player1 = Player(PLAYER1_COLOR, MAZE_TOP_LEFT_CORNER[0] + BLOCK_SIZE, MAZE_TOP_LEFT_CORNER[1] + BLOCK_SIZE, (BLOCK_SIZE * 3) // 2)
        self.player2 = Player(PLAYER2_COLOR, MAZE_TOP_LEFT_CORNER[0] + MAZE_WIDTH_PX - CELL_SIZE, MAZE_TOP_LEFT_CORNER[1] + MAZE_HEIGHT_PX - CELL_SIZE, (BLOCK_SIZE * 3) // 2)

        self.all_sprites = pg.sprite.RenderUpdates()
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)

        self.player1_score = 0
        self.player2_score = 0

        self.win1_flag = False
        self.win2_flag = False

    @staticmethod
    def get_cell_index(position):
        x, y = position
        return y * MAZE_WIDTH + x

    def generate_maze(self):
        # Initialize maze with zero values
        self.maze = [0] * CELL_COUNT
        visited_count = 0

        # Start in middle of maze
        process_stack = [(18, 14)]
        self.maze[self.get_cell_index((18,14))] |= CellProp.Visited.value

        visited_count += 1
        while visited_count < CELL_COUNT:
            # Step 1 - Create a list of the unvisited neighbors
            x, y = process_stack[-1]  # get position of top item on stack
            current_cell_index = self.get_cell_index((x, y))

            # Find all unvisited neighbors
            neighbors = []
            for direction in Direction:
                dir = direction.value
                new_x, new_y = (x + dir[0], y + dir[1])
                if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT:
                    index = self.get_cell_index((new_x, new_y))
                    if not self.maze[index] & CellProp.Visited.value:
                        # Cell was not already visited so add to neighbors list with the direction
                        neighbors.append((new_x, new_y, direction))

            if len(neighbors) > 0:
                # Choose a random neighboring cell
                cell = neighbors[random.randrange(len(neighbors))]
                cell_x, cell_y, cell_direction = cell
                cell_position = (cell_x, cell_y)
                cell_index = self.get_cell_index(cell_position)

                # Create a path between the neighbor and the current cell by setting the direction property flag
                flag_to = MazeGenerator.direction_to_flag[cell_direction]
                flag_from = MazeGenerator.direction_to_flag[MazeGenerator.opposite_direction[cell_direction]]

                self.maze[current_cell_index] |= flag_to.value
                self.maze[cell_index] |= flag_from.value | CellProp.Visited.value

                process_stack.append(cell_position)
                visited_count += 1
            else:
                # Backtrack since there were no unvisited neighbors
                process_stack.pop()

            if SHOW_DRAW:
                self.draw_maze()
                pg.display.update()
                #pg.time.wait(500)
                pg.event.pump()

        # save image of completed maze
        self.draw_maze()
        pg.display.update()
        self.maze_image = self.screen.copy()

    def draw_maze(self):
        self.screen.fill(BACK_COLOR)
        pg.draw.rect(self.screen, WALL_COLOR, (MAZE_TOP_LEFT_CORNER[0], MAZE_TOP_LEFT_CORNER[1], MAZE_WIDTH_PX, MAZE_HEIGHT_PX))

        for x in range(MAZE_WIDTH):
            for y in range(MAZE_HEIGHT):
                for py in range(PATH_WIDTH):
                    for px in range(PATH_WIDTH):
                        cell_index = self.get_cell_index((x, y))
                        if self.maze[cell_index] & CellProp.Visited.value:
                            self.draw(MAZE_COLOR, x * (PATH_WIDTH + 1) + px, y * (PATH_WIDTH + 1) + py)
                        else:
                            self.draw(UNVISITED_COLOR, x * (PATH_WIDTH + 1) + px, y * (PATH_WIDTH + 1) + py)

                for p in range(PATH_WIDTH):
                    if self.maze[y * MAZE_WIDTH + x] & CellProp.Path_S.value:
                        self.draw(MAZE_COLOR, x * (PATH_WIDTH + 1) + p, y * (PATH_WIDTH + 1) + PATH_WIDTH)

                    if self.maze[y * MAZE_WIDTH + x] & CellProp.Path_E.value:
                        self.draw(MAZE_COLOR, x * (PATH_WIDTH + 1) + PATH_WIDTH, y * (PATH_WIDTH + 1) + p)

        # Color the player exits
        pg.draw.rect(self.screen, PLAYER2_COLOR, (MAZE_TOP_LEFT_CORNER[0], MAZE_TOP_LEFT_CORNER[1] + BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE * 3))

        pg.draw.rect(self.screen, PLAYER1_COLOR, (MAZE_TOP_LEFT_CORNER[0] + MAZE_WIDTH_PX - BLOCK_SIZE, MAZE_TOP_LEFT_CORNER[1] + MAZE_HEIGHT_PX - BLOCK_SIZE * 4, BLOCK_SIZE, BLOCK_SIZE * 3))

    def draw(self, color, x, y):
        x_offset = MAZE_TOP_LEFT_CORNER[0] + BLOCK_SIZE
        y_offset = MAZE_TOP_LEFT_CORNER[1] + BLOCK_SIZE
        pg.draw.rect(self.screen, color, (x * BLOCK_SIZE + x_offset, y * BLOCK_SIZE + y_offset, BLOCK_SIZE, BLOCK_SIZE))

    def draw_scores(self):
        # Display Scores
        font = pg.font.SysFont('dejavusansmono', 18, True)

        p1_msg = f'PLAYER 1: {self.player1_score}'
        p2_msg = f'PLAYER 2: {self.player2_score}'
        p1_size = font.size(p1_msg)
        p2_size = font.size(p2_msg)
        p1 = font.render(p1_msg, True, PLAYER1_COLOR)
        p2 = font.render(p2_msg, True, PLAYER2_COLOR)

        p1_x = MAZE_TOP_LEFT_CORNER[0]
        p1_y = MAZE_TOP_LEFT_CORNER[1] - p1_size[1]
        p1_w = p1.get_rect().w
        p1_h = p1.get_rect().h
        p2_x = MAZE_TOP_LEFT_CORNER[0] + MAZE_WIDTH_PX - p2_size[0]
        p2_y = MAZE_TOP_LEFT_CORNER[1] - p1_size[1]
        p2_w = p2.get_rect().w
        p2_h = p2.get_rect().h

        self.screen.blit(p1, (p1_x, p1_y))
        self.screen.blit(p2, (p2_x, p2_y))

        pg.display.update([(p1_x, p1_y, p1_w, p1_h), (p2_x, p2_y, p2_w, p2_h)])

    def draw_instructions(self):
        # Display instructions
        font = pg.font.SysFont('Arial', 18, True)

        p1_msg = 'w a s d to move'
        p2_msg = '↑ ← ↓ → to move'
        p2_size = font.size(p2_msg)
        p1 = font.render(p1_msg, True, PLAYER1_COLOR)
        p2 = font.render(p2_msg, True, PLAYER2_COLOR)

        p1_x = MAZE_TOP_LEFT_CORNER[0]
        p1_y = MAZE_TOP_LEFT_CORNER[1] + MAZE_HEIGHT_PX + 2
        p1_w = p1.get_rect().w
        p1_h = p1.get_rect().h
        p2_x = MAZE_TOP_LEFT_CORNER[0] + MAZE_WIDTH_PX - p2_size[0]
        p2_y = MAZE_TOP_LEFT_CORNER[1] + MAZE_HEIGHT_PX + 2
        p2_w = p2.get_rect().w
        p2_h = p2.get_rect().h

        self.screen.blit(p1, (p1_x, p1_y))
        self.screen.blit(p2, (p2_x, p2_y))

        pg.display.update([(p1_x, p1_y, p1_w, p1_h), (p2_x, p2_y, p2_w, p2_h)])

    def draw_goals(self):
        self.all_sprites.clear(self.screen, self.maze_image)
        dirty_recs = self.all_sprites.draw(self.screen)
        pg.display.update(dirty_recs)

    def initialize(self):
        self.draw_goals()
        self.generate_maze()
        self.draw_instructions()

    def run_game(self):
        clock = pg.time.Clock()
        self.initialize()

        # Main game loop
        run = True
        click = False
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pg.quit()
                        sys.exit()
       
                if self.win1_flag or self.win2_flag:
                    self.draw_win()
                    self.win1_flag = self.win2_flag = False
                    self.initialize()

                if not self.win1_flag and not self.win2_flag:
                    keys = pg.key.get_pressed()
                    if keys[pg.K_r]:
                        self.initialize()
                    if keys[pg.K_ESCAPE]:
                        run = False

                if SHOW_FPS:
                    pg.display.set_caption(f'PyMaze ({str(int(clock.get_fps()))} FPS)')
                    clock.tick()
                else:
                    clock.tick(200)

        pg.quit()

mg = MazeGenerator()



"""
START SCREEN CODE BEGINS HERE
"""



mainClock = pg.time.Clock()
from pygame.locals import *
pg.init()
pg.display.set_caption('2 Player Maze Game')
screen = pg.display.set_mode((1200, 960),0,32)
 
#setting font settings
font = pg.font.SysFont(None, 30)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
# A variable to check for the status later
click = False
 
# Main container function that holds the buttons and game functions
def main_menu():
    while True:
 
        screen.fill((38,38,38))
        draw_text('Main Menu', font, (0,255,0), screen, 550, 40)

        mx, my = pg.mouse.get_pos()

        #creating buttons
        button_1 = pg.Rect(500, 100, 200, 50)
        button_2 = pg.Rect(500, 180, 200, 50)

        #defining functions when a certain button is pressed
        if button_1.collidepoint((mx, my)):
            if click:
                mg.run_game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()

        pg.draw.rect(screen, (0, 255, 0), button_1) #button colors
        pg.draw.rect(screen, (0, 255, 0), button_2)
 
        #writing text on top of button
        draw_text('PLAY', font, (38,38,38), screen, 570, 115)
        draw_text('OPTIONS', font, (38,38,38), screen, 550, 195)

        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pg.display.update()
        mainClock.tick(60)


"""
This function is called when the "OPTIONS" button is clicked.
"""


def options():
    running = True
    while running:

        screen.fill((38,38,38))

        draw_text('OPTIONS SCREEN', font, (255, 255, 255), screen, 20, 20)
        draw_text('Background Colors', font, (255, 255, 255), screen, 90, 250)
        draw_text('Maze Colors', font, (255, 255, 255), screen, 90, 550)

        pg.draw.rect(screen, (227, 19, 29), pg.Rect(325, 225, 75, 75))
        pg.draw.rect(screen, (255, 217, 102), pg.Rect(450, 225, 75, 75))
        pg.draw.rect(screen, (39, 78, 19), pg.Rect(575, 225, 75, 75))
        pg.draw.rect(screen, (96, 193, 232), pg.Rect(700, 225, 75, 75))
        pg.draw.rect(screen, (24, 37, 71), pg.Rect(825, 225, 75, 75))
        pg.draw.rect(screen, (250, 81, 146), pg.Rect(950, 225, 75, 75))
        pg.draw.rect(screen, (91, 107, 170), pg.Rect(1075, 225, 75, 75))
        pg.draw.rect(screen, (0, 0, 0), pg.Rect(325, 525, 75, 75))

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
       
        pg.display.update()
        mainClock.tick(60)
 
main_menu()

