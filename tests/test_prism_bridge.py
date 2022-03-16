import unittest
from prism_bridge.prism_bridge import PrismBridge
from py4j.protocol import Py4JNetworkError


class PrismHandlerTest(unittest.TestCase):

    def setUp(self):
        try:
            self.prism_handler = PrismBridge()
            print("Successfully connected to PRISM java gateway!")
        except Py4JNetworkError as err:
            print('Py4JNetworkError:', err)
            print("It is most likely that you forgot to start the PRISM java gateway. "
                  "Compile and launch PrismEntryPoint.java!")
    
    def test_load_model_file(self):
        self.prism_handler.load_model_file("../tests/resources/die.prism")

    def test_check_property(self):
        self.prism_handler.load_model_file("../tests/resources/die.prism")
        result = self.prism_handler.check_property("P=? [ F s=7 & d=3 ]")
        self.assertAlmostEqual(result[0], 0.166666666, places=4)

    def test_check_smg(self):
        self.prism_handler.load_model_file("../tests/resources/reward-game.prism")
        result = self.prism_handler.check_property("<<p1>> Rmax=? [ F0 \"acc\" ]")
        self.assertAlmostEqual(result[0], 2.0, places=4)

    def test_strategy_smg(self):
        self.prism_handler.load_model_file("../tests/resources/simple-game.prism")
        result = self.prism_handler.synthesize_strategy("<<p1>> Pmax=? [ F \"acc\" ]", test=True)
        self.assertEqual(result["0"], "p1_0_1")
        self.assertEqual(result["3"], "-")

    def test_strategy_reward(self):
        self.prism_handler.load_model_file("../tests/resources/reward-game.prism")
        result = self.prism_handler.synthesize_strategy("<<p1>> Rmax=? [ F0 \"acc\" ]", test=True)
        self.assertEqual(result["0"], "p1_0_2")
        self.assertEqual(result["3"], "-")

 
if __name__ == '__main__':
    unittest.main()