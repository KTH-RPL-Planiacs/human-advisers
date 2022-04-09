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