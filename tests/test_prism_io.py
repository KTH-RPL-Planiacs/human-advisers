import unittest
import os
import networkx as nx
from prism_bridge.prism_io import write_prism_model


class PrismIOTest(unittest.TestCase):

    def setUp(self):
        self.test_game = nx.DiGraph()
        self.test_game.graph['init'] = 'A'
        self.test_game.graph['acc'] = ['A']
        self.test_game.add_node('A', player=1)
        self.test_game.add_node('B', player=2)
        self.test_game.add_node('C', player=2)
        self.test_game.add_node('C_p', player=0)
        self.test_game.add_node('C_pp', player=0)
        self.test_game.add_edge('A', 'B', act='stay')
        self.test_game.add_edge('A', 'C', act='move')
        self.test_game.add_edge('B', 'A')
        self.test_game.add_edge('C', 'C_p')
        self.test_game.add_edge('C_p', 'A', prob=0.5)
        self.test_game.add_edge('C_p', 'C_pp', prob=0.5)
        self.test_game.add_edge('C_pp', 'B', prob=1)
        os.mkdir(os.path.join(os.getcwd(), 'generated'))

    def test_write_prism_model(self):
        file_name, state_ids = write_prism_model(self.test_game, 'test')
        self.assertTrue(os.path.exists(file_name))
        self.assertEqual(state_ids, {'A': 0, 'B': 1, 'C': 2})
