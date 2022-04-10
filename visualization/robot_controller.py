from abc import ABC, abstractmethod

from visualization.constants import Move


class RobotController(ABC):

    @abstractmethod
    def get_next_move(self):
        pass

    @abstractmethod
    def get_safety_adv(self):
        pass

    @abstractmethod
    def get_fairness_adv(self):
        pass

    @abstractmethod
    def set_human_move(self, move):
        pass

    @abstractmethod
    def is_satisfied(self):
        pass

    @abstractmethod
    def is_violated(self):
        pass


class DummyController(RobotController):
    def get_next_move(self):
        return Move.IDLE

    def set_human_move(self, move):
        pass

    def is_satisfied(self):
        return True

    def is_violated(self):
        return False

    def get_safety_adv(self):
        return {Move.UP, Move.DOWN}

    def get_fairness_adv(self):
        return {Move.LEFT}
