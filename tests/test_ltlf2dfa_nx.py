import unittest
import networkx
from ltlf2dfa_nx.mona2nx import to_nxgraph, MonaFormatError
from ltlf2dfa_nx.parse_ltlf import to_mona


class TestMona2Nx(unittest.TestCase):

    def test_unsatisfiable(self):
        with self.assertRaises(MonaFormatError) as context:
            to_nxgraph("Formula is unsatisfiable")

        self.assertTrue("Formula is unsatisfiable, DFA not constructed!" in str(context.exception))

    def test_invalid(self):
        with self.assertRaises(MonaFormatError) as context:
            to_nxgraph("This is super wrong input 2315453jnasfjaj5")

        self.assertTrue("Input is no valid MONA output!" in str(context.exception))

    def test_valid(self):
        mona = to_mona("F b")
        ba = to_nxgraph(mona)
        self.assertIsInstance(ba, networkx.classes.digraph.DiGraph)
        self.assertEqual(len(ba.nodes), 2)


if __name__ == '__main__':
    unittest.main()
