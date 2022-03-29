import unittest

import networkx as nx

from game_synth.helpers import powerset, group_and_flip, create_guard, sog_fits_to_guard, remove_edges


class GameSynthHelpersTest(unittest.TestCase):

    def test_powerset(self):
        result = list(powerset([1, 2, 3]))
        expected = [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
        self.assertEqual(result, expected)

    def test_group_and_flip(self):
        inp = {'a': [1, 2], 'b': [2, 1], 'c': [1, 3, 5]}
        result = group_and_flip(inp)
        expected = {frozenset({1, 2}): ['a', 'b'], frozenset({1, 3, 5}): ['c']}
        self.assertEqual(result, expected)

    def test_create_guard(self):
        ap = ["a", "b", "c"]
        self.assertEqual(create_guard((), ap), "000")
        self.assertEqual(create_guard(("a", "b", "c"), ap), "111")
        self.assertEqual(create_guard(("a", "c"), ap), "101")

    def test_sog_fits_to_guard(self):
        guard = "110"
        sog = ["XXX", "000", "010", "011"]
        guard_ap = ["a", "b", "c"]
        sog_ap = ["c", "b", "a"]
        result = sog_fits_to_guard(guard, sog, guard_ap, sog_ap)
        expected = ["XXX", "011"]
        self.assertEqual(result, expected)

    def test_remove_edges(self):
        game = nx.DiGraph()
        game.add_edge(1, 2)
        game.add_edge(2, 3)
        self.assertEqual(len(game.edges), 2)
        edges_to_remove = [(1, 2)]
        remove_edges(game, edges_to_remove)
        self.assertEqual(len(game.edges), 1)

