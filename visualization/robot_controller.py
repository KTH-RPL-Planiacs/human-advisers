from abc import ABC, abstractmethod
import copy

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
        self.safety_violated = False

    def get_next_move(self):
        assert self.game.nodes[self.current_state]["player"] == 1
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
        old_state = copy.deepcopy(self.current_state)
        prob_state = self.next_prob_state(move)
        self.current_state = self.next_state(move)
        # check safety violation
        if (old_state, prob_state) in self.safety_adv:
            self.safety_violated = True

    def set_robot_move(self, move):
        assert self.game.nodes[self.current_state]["player"] == 1
        self.current_state = self.next_state(move)

    def next_prob_state(self, move):
        act = game_action_from_move(move)
        prob_state = None
        for succ in self.game.successors(self.current_state):
            if self.game.edges[self.current_state, succ]["act"] == act:
                prob_state = succ
                break
        assert prob_state is not None, "invalid move"
        return prob_state

    def next_state(self, move):
        prob_state = self.next_prob_state(move)
        # assume moving succeeds
        for succ in self.game.successors(prob_state):
            if succ != self.current_state or move == Move.IDLE:
                return succ

        assert False, "no successor state found"

    def is_satisfied(self):
        return self.current_state in self.game.graph["acc"]

    def is_violated(self):
        return self.safety_violated

    def get_safety_adv(self):
        assert self.game.nodes[self.current_state]["player"] == 1
        adv = set()
        next_state = self.next_state(self.get_next_move())
        for succ in self.game.successors(next_state):
            if (next_state, succ) in self.safety_adv:
                adv.add(move_from_game_action(self.game.edges[next_state, succ]["act"]))
        return adv

    def get_fairness_adv(self):
        assert self.game.nodes[self.current_state]["player"] == 1
        adv = set()
        next_state = self.next_state(self.get_next_move())
        for succ in self.game.successors(next_state):
            if (next_state, succ) in self.fairness_adv:
                adv.add(move_from_game_action(self.game.edges[next_state, succ]["act"]))
        return adv


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


def move_from_game_action(act):
    if act == "up":
        return Move.UP
    if act == "down":
        return Move.DOWN
    if act == "left":
        return Move.LEFT
    if act == "right":
        return Move.RIGHT
    if act == "stay":
        return Move.IDLE
