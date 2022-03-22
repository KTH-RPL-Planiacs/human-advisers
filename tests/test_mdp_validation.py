import unittest
import networkx as nx
from models.validation import is_probabilites_valid


class GameSynthHelpersTest(unittest.TestCase):

    def test_probabilities_valid(self):
        valid_mdp = nx.DiGraph()
        valid_mdp.graph["init"] = "1"
        valid_mdp.graph["acc"] = "1"
        valid_mdp.graph["ap"] = ["a", "b"]

        valid_mdp.add_node("1", player=1, ap="11")
        valid_mdp.add_node("3", player=1, ap="00")
        valid_mdp.add_node("2", player=0)

        valid_mdp.add_edge("1", "2", act="act")
        valid_mdp.add_edge("2", "1", prob=0.5)
        valid_mdp.add_edge("2", "3", prob=0.5)

        self.assertTrue(is_probabilites_valid(valid_mdp))

    def test_probabilities_invalid(self):
        invalid_mdp = nx.DiGraph()
        invalid_mdp.graph["init"] = "1"
        invalid_mdp.graph["acc"] = "1"
        invalid_mdp.graph["ap"] = ["a", "b"]

        invalid_mdp.add_node("1", player=1, ap="11")
        invalid_mdp.add_node("3", player=1, ap="00")
        invalid_mdp.add_node("2", player=0)

        invalid_mdp.add_edge("1", "2", act="act")
        invalid_mdp.add_edge("2", "1", prob=1.0)
        invalid_mdp.add_edge("2", "3", prob=1.0)

        self.assertFalse(is_probabilites_valid(invalid_mdp))
