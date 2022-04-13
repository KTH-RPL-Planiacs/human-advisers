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
    def set_robot_move(self, move):
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

    def set_robot_move(self, move):
        pass

    def is_satisfied(self):
        return True

    def is_violated(self):
        return False

    def get_safety_adv(self):
        return {Move.UP, Move.DOWN}

    def get_fairness_adv(self):
        return {Move.LEFT}


class AdviserRobotController(RobotController):
    def __init__(self, game, strategy, safety, fairness):
        super().__init__()
        self.game = game
        self.strategy = strategy
        self.current_state = game.graph["init"]
        self.safety_adv = safety
        self.fairness_adv = fairness

    def get_next_move(self):
        if self.current_state in self.strategy.keys():
            strat_move = self.strategy[self.current_state]
            if strat_move == "up":
                return Move.UP
            if strat_move == "left":
                return Move.LEFT
            if strat_move == "right":
                return Move.RIGHT
            if strat_move == "down":
                return Move.DOWN
            if strat_move == "stay":
                return Move.IDLE

        return Move.IDLE

    def set_human_move(self, move):
        assert self.game.nodes[self.current_state]["player"] == 2
        act = game_action_from_move(move)
        prob_state = None
        for succ in self.game.successors(self.current_state):
            if self.game.edges[self.current_state, succ]["act"] == act:
                prob_state = succ
                break
        assert prob_state is not None, "invalid move"
        # assume moving succeeds
        for succ in self.game.successors(prob_state):
            if succ != self.current_state or move == Move.IDLE:
                self.current_state = succ
                return

        assert False,  "no successor state found"

    def set_robot_move(self, move):
        assert self.game.nodes[self.current_state]["player"] == 1
        act = game_action_from_move(move)
        prob_state = None
        for succ in self.game.successors(self.current_state):
            if self.game.edges[self.current_state, succ]["act"] == act:
                prob_state = succ
                break
        assert prob_state is not None, "invalid move"
        # assume moving succeeds
        for succ in self.game.successors(prob_state):
            if succ != self.current_state or move == Move.IDLE:
                self.current_state = succ
                return

        assert False, "no successor state found"

    def is_satisfied(self):
        return self.current_state in self.game.graph["acc"]

    def is_violated(self):
        return False

    def get_safety_adv(self):
        return {}

    def get_fairness_adv(self):
        return {}


def game_action_from_move(move):
    if move == Move.UP:
        return "up"
    if move == Move.DOWN:
        return "down"
    if move == Move.LEFT:
        return "left"
    if move == Move.RIGHT:
        return "right"
    if move == Move.IDLE:
        return "stay"
