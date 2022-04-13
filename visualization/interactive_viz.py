import pygame
import time

from visualization.robot_controller import DummyController
from visualization.constants import Move, Color


class RectSprite(pygame.sprite.Sprite):

    def __init__(self, path, width, height):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(width), int(height)))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class InteractiveViz:

    def __init__(self, robot_controller, grid, grid_size_x=500, grid_size_y=500, cell_margin=5):
        self.robot_controller = robot_controller

        # cell dimensions
        self.GRID_SIZE = (grid_size_x, grid_size_y)
        self.WIDTH = int((grid_size_x / len(grid[0])) - cell_margin)
        self.HEIGHT = int((grid_size_y / len(grid)) - cell_margin)
        self.MARGIN = cell_margin

        # grid info
        self.grid = grid
        self.robot_pos = (0, 0)
        self.next_robot_pos = (0, 0)
        self.human_pos = (0, 0)
        self.next_human_pos = (0, 0)

        # simulation speed
        self.FPS = 60  # frames per second
        self.SPEED = 60  # frames per move
        self.frame_count = 0

        pygame.init()
        pygame.font.init()

        # set the width and height of the screen (width , height)
        self.PANEL_WIDTH = 300
        screen_x = grid_size_x + self.PANEL_WIDTH    # for status panel
        screen_y = grid_size_y
        self.size = (screen_x, screen_y)
        self.screen = pygame.display.set_mode(self.size)

        self.font = pygame.font.SysFont('monospace', 20)
        pygame.display.set_caption("Interactive Visualization")

        # sprites
        # actors
        self.actor_sprites = pygame.sprite.Group()
        scaling_factor = 0.8
        self.robot_sprite = RectSprite('visualization/assets/robot.png', self.WIDTH * scaling_factor, self.HEIGHT * scaling_factor)
        self.human_sprite = RectSprite('visualization/assets/person.png', self.WIDTH * scaling_factor, self.HEIGHT * scaling_factor)
        self.actor_sprites.add(self.robot_sprite)
        self.actor_sprites.add(self.human_sprite)
        # arrows
        self.ARROW_SIZE = 100
        self.white_arrows = {
            Move.UP: RectSprite('visualization/assets/up.png', self.ARROW_SIZE, self.ARROW_SIZE),
            Move.LEFT: RectSprite('visualization/assets/left.png', self.ARROW_SIZE, self.ARROW_SIZE),
            Move.RIGHT: RectSprite('visualization/assets/right.png', self.ARROW_SIZE, self.ARROW_SIZE),
            Move.DOWN: RectSprite('visualization/assets/down.png', self.ARROW_SIZE, self.ARROW_SIZE),
            Move.IDLE: RectSprite('visualization/assets/idle.png', self.ARROW_SIZE, self.ARROW_SIZE),
        }
        self.init_arrow_positions(self.white_arrows)
        self.red_arrows = {
            Move.UP: RectSprite('visualization/assets/up_r.png', self.ARROW_SIZE, self.ARROW_SIZE),
            Move.LEFT: RectSprite('visualization/assets/left_r.png', self.ARROW_SIZE, self.ARROW_SIZE),
            Move.RIGHT: RectSprite('visualization/assets/right_r.png', self.ARROW_SIZE, self.ARROW_SIZE),
            Move.DOWN: RectSprite('visualization/assets/down_r.png', self.ARROW_SIZE, self.ARROW_SIZE),
            Move.IDLE: RectSprite('visualization/assets/idle_r.png', self.ARROW_SIZE, self.ARROW_SIZE),
        }
        self.init_arrow_positions(self.red_arrows)
        self.green_arrows = {
            Move.UP: RectSprite('visualization/assets/up_g.png', self.ARROW_SIZE, self.ARROW_SIZE),
            Move.LEFT: RectSprite('visualization/assets/left_g.png', self.ARROW_SIZE, self.ARROW_SIZE),
            Move.RIGHT: RectSprite('visualization/assets/right_g.png', self.ARROW_SIZE, self.ARROW_SIZE),
            Move.DOWN: RectSprite('visualization/assets/down_g.png', self.ARROW_SIZE, self.ARROW_SIZE),
            Move.IDLE: RectSprite('visualization/assets/idle_g.png', self.ARROW_SIZE, self.ARROW_SIZE),
        }
        self.init_arrow_positions(self.green_arrows)

        # loop variables
        self.running = True
        self.paused = False

    def init_arrow_positions(self, arrows):
        x_panel_center = self.GRID_SIZE[0] + self.PANEL_WIDTH / 2.
        y_start = 100. + self.ARROW_SIZE / 2.
        arrows[Move.UP].rect.center = (x_panel_center, y_start)
        arrows[Move.IDLE].rect.center = (x_panel_center, y_start + self.ARROW_SIZE)
        arrows[Move.LEFT].rect.center = (x_panel_center - self.ARROW_SIZE, y_start + self.ARROW_SIZE)
        arrows[Move.RIGHT].rect.center = (x_panel_center + self.ARROW_SIZE, y_start + self.ARROW_SIZE)
        arrows[Move.DOWN].rect.center = (x_panel_center, y_start + 2. * self.ARROW_SIZE)

    def init_human_pos(self, x, y):
        self.human_pos = (x, y)
        self.next_human_pos = (x, y)

    def init_robot_pos(self, x, y):
        self.robot_pos = (x, y)
        self.next_robot_pos = (x, y)

    def render(self):
        self.screen.fill(Color.BLACK)
        self.render_grid()
        self.render_actors()
        self.render_status_panel()

        # flip the renderer buffer
        pygame.display.flip()

    def render_status_panel(self):
        # status panel
        self.render_text("SPACE to pause/unpause", color=Color.WHITE, x=self.GRID_SIZE[0])
        self.render_text("WASD to move", color=Color.WHITE, x=self.GRID_SIZE[0], y=20)
        if self.paused:
            self.render_text("PAUSED", color=Color.WHITE, x=self.GRID_SIZE[0], y=40)

        satisfied_str = "satisfied: "
        if self.robot_controller.is_satisfied():
            satisfied_str += "true"
        else:
            satisfied_str += "false"
        self.render_text(satisfied_str, color=Color.WHITE, x=self.GRID_SIZE[0], y=60)

        violated_str = "safety violated: "
        if self.robot_controller.is_violated():
            violated_str += "true"
        else:
            violated_str += "false"
        self.render_text(violated_str, color=Color.WHITE, x=self.GRID_SIZE[0], y=80)

        # adviser arrows
        for arrow_sprite in self.white_arrows.values():
            arrow_sprite.draw(self.screen)

        for saf_adv in self.robot_controller.get_safety_adv():
            self.red_arrows[saf_adv].draw(self.screen)

        for fair_adv in self.robot_controller.get_fairness_adv():
            self.green_arrows[fair_adv].draw(self.screen)

    def render_actors(self):
        # interpolation
        t = self.frame_count / self.SPEED
        t = t * t * (3 - 2 * t)

        # update robot pos
        r_dx = ((self.WIDTH + self.MARGIN / 2.) / 2.) - (self.robot_sprite.rect.width / 2.)
        r_dy = ((self.HEIGHT + self.MARGIN / 2.) / 2.) - (self.robot_sprite.rect.height / 2.)
        r_x = (self.MARGIN + self.WIDTH) * self.robot_pos[0] + r_dx
        r_y = (self.MARGIN + self.HEIGHT) * self.robot_pos[1] + r_dy
        r_nx = (self.MARGIN + self.WIDTH) * self.next_robot_pos[0] + r_dx
        r_ny = (self.MARGIN + self.HEIGHT) * self.next_robot_pos[1] + r_dy
        self.robot_sprite.rect.x = int(r_x * (1. - t) + r_nx * t)
        self.robot_sprite.rect.y = int(r_y * (1. - t) + r_ny * t)

        # update human pos
        h_dx = ((self.WIDTH + self.MARGIN / 2.) / 2.) - (self.human_sprite.rect.width / 2.)
        h_dy = ((self.HEIGHT + self.MARGIN / 2.) / 2.) - (self.human_sprite.rect.height / 2.)
        h_x = (self.MARGIN + self.WIDTH) * self.human_pos[0] + self.MARGIN / 2. + h_dx
        h_y = (self.MARGIN + self.HEIGHT) * self.human_pos[1] + self.MARGIN / 2. + h_dy
        h_nx = (self.MARGIN + self.WIDTH) * self.next_human_pos[0] + self.MARGIN / 2. + h_dx
        h_ny = (self.MARGIN + self.HEIGHT) * self.next_human_pos[1] + self.MARGIN / 2. + h_dy
        self.human_sprite.rect.x = int(h_x * (1 - t) + h_nx * t)
        self.human_sprite.rect.y = int(h_y * (1 - t) + h_ny * t)

        # draw the actors
        self.actor_sprites.draw(self.screen)

    def render_grid(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                cell_color = Color.BLACK
                if self.grid[row][col] == 0:
                    cell_color = Color.WHITE

                cell_x = (self.MARGIN + self.WIDTH) * col + self.MARGIN / 2.
                cell_y = (self.MARGIN + self.HEIGHT) * row + self.MARGIN / 2.
                pygame.draw.rect(self.screen, cell_color, [cell_x, cell_y, self.WIDTH, self.HEIGHT])

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
            self.step()

    def step(self):
        # new human position
        self.human_pos = tuple(self.next_human_pos)
        nx = self.human_pos[0]
        ny = self.human_pos[1]

        human_move = self.get_human_move()
        if human_move == Move.UP:
            ny -= 1
        if human_move == Move.DOWN:
            ny += 1
        if human_move == Move.LEFT:
            nx -= 1
        if human_move == Move.RIGHT:
            nx += 1

        self.next_human_pos = (nx, ny)

        # new robot position
        self.robot_pos = tuple(self.next_robot_pos)
        nx = self.robot_pos[0]
        ny = self.robot_pos[1]

        robot_move = self.robot_controller.get_next_move()
        if robot_move == Move.UP:
            ny -= 1
        if robot_move == Move.DOWN:
            ny += 1
        if robot_move == Move.LEFT:
            nx -= 1
        if robot_move == Move.RIGHT:
            nx += 1

        self.next_robot_pos = (nx, ny)

        # update robot controller
        self.robot_controller.set_robot_move(robot_move)
        self.robot_controller.set_human_move(human_move)

    def get_human_move(self):
        human_move = Move.IDLE
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.constants.K_w]:
            if self.human_pos[1] > 0:
                human_move = Move.UP
        if pressed_keys[pygame.constants.K_s]:
            if self.human_pos[1] < len(self.grid)-1:
                human_move = Move.DOWN
        if pressed_keys[pygame.constants.K_a]:
            if self.human_pos[0] > 0:
                human_move = Move.LEFT
        if pressed_keys[pygame.constants.K_d]:
            if self.human_pos[0] < len(self.grid[0])-1:
                human_move = Move.RIGHT

        return human_move

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

