import pygame
import time
from enum import Enum


class Move(Enum):
    IDLE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 150, 150)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)


class RectSprite(pygame.sprite.Sprite):

    def __init__(self, path, width, height):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(width), int(height)))
        self.rect = self.image.get_rect()


class InteractiveViz:

    def __init__(self, grid, grid_size_x=500, grid_size_y=500, cell_margin=5):
        # cell dimensions
        self.GRID_SIZE = (grid_size_x, grid_size_y)
        self.WIDTH = int((grid_size_x / len(grid[0])) - cell_margin)
        self.HEIGHT = int((grid_size_y / len(grid)) - cell_margin)
        self.MARGIN = cell_margin

        # grid info
        self.grid = grid

        # simulation speed
        self.FPS = 60  # frames per second
        self.SPEED = 60  # frames per move
        self.frame_count = 0

        pygame.init()
        pygame.font.init()

        # set the width and height of the screen (width , height)
        screen_x = grid_size_x + 300    # for status panel
        screen_y = grid_size_y
        self.size = (screen_x, screen_y)
        self.screen = pygame.display.set_mode(self.size)

        self.font = pygame.font.SysFont('monospace', 20)
        pygame.display.set_caption("Interactive Visualization")

        # sprites
        self.sprites_list = pygame.sprite.Group()
        scaling_factor = 0.8
        self.robot_sprite = RectSprite('assets/robot.png', self.WIDTH * scaling_factor, self.HEIGHT * scaling_factor)
        self.person_sprite = RectSprite('assets/person.png', self.WIDTH * scaling_factor, self.HEIGHT * scaling_factor)
        self.sprites_list.add(self.robot_sprite)
        self.sprites_list.add(self.person_sprite)

        # loop variables
        self.running = True
        self.paused = False

    def render(self):
        self.screen.fill(Color.BLACK)

        # draw the grid
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                cell_color = Color.BLACK
                if self.grid[row][col] == 0:
                    cell_color = Color.WHITE

                cell_x = (self.MARGIN + self.WIDTH) * col + self.MARGIN / 2.
                cell_y = (self.MARGIN + self.HEIGHT) * row + self.MARGIN / 2.
                pygame.draw.rect(self.screen, cell_color, [cell_x, cell_y, self.WIDTH, self.HEIGHT])

        # draw the actors
        self.sprites_list.draw(self.screen)

        # status panel
        self.render_text("SPACE to pause/unpause", color=Color.WHITE, x=self.GRID_SIZE[0])
        self.render_text("WASD to move", color=Color.WHITE, x=self.GRID_SIZE[0], y=20)

        # flip the renderer buffer
        pygame.display.flip()

    def render_text(self, text, color=Color.BLACK, x=0, y=0):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def idle(self, idle_time):
        pass

    def run_step(self):
        if self.paused:
            return

        self.frame_count += 1
        if self.frame_count >= self.SPEED:
            self.frame_count = 0
            print("STEP")

    def handle_events(self):
        for event in pygame.event.get():
            # hit a key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC key
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused

            # press X in window
            if event.type == pygame.QUIT:
                self.running = False

    def run_loop(self):
        next_time = time.time()
        self.running = True
        self.paused = True
        while self.running:
            self.handle_events()
            self.render()
            now_time = time.time()
            self.idle(max(0., next_time - now_time))
            if now_time >= next_time:
                self.run_step()
                next_time = now_time + (1 / self.FPS)


if __name__ == "__main__":
    ex_grid = [[0 for col in range(10)] for row in range(10)]
    viz = InteractiveViz(grid=ex_grid)
    viz.run_loop()
