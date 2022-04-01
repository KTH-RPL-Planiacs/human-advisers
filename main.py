import sys
from copy import deepcopy
from prism_bridge.prism_bridge import PrismBridge
from py4j.protocol import Py4JNetworkError
from models.corridor import corridor_mdp
from ltlf2dfa_nx.mona2nx import to_nxgraph
from ltlf2dfa_nx.parse_ltlf import to_mona
# from game_synth.modelless_human_game import create_game
from game_synth.modelled_human_game import create_game
from game_synth.helpers import remove_edges, remove_other_edges
from game_synth.strategy import get_min_strategy_bounded, has_winning_strategy
from advisers.safety import minimal_safety_edges
from advisers.fairness import minimal_fairness_edges

if __name__ == "__main__":
    try:
        prism_handler = PrismBridge()
        print("Successfully connected to PRISM java gateway!")

        robot_model = corridor_mdp("_r", "end_bot")
        human_model = corridor_mdp("_h", "end_top")
        spec = "F(end_top_r) && G(!(crit_r && crit_h))"
        dfa = to_nxgraph(to_mona(spec))
        # we keep the original game for later
        orig_synth = create_game(robot_model, human_model, dfa)
        synth = deepcopy(orig_synth)

        print("Game has winning strategy before assumptions:", has_winning_strategy(synth, prism_handler))
        safety_edges = minimal_safety_edges(synth, prism_handler)
        remove_edges(synth, safety_edges)           # necessary
        fairness_edges = minimal_fairness_edges(synth, prism_handler)
        assert fairness_edges is not None, "game unwinnable after safety assumptions"
        remove_other_edges(synth, fairness_edges)   # not necessary, only for bounded game purposes

        print("SAFETY ASSUM", safety_edges)
        print("FAIRNESS ASSUM", fairness_edges)

        strategy = get_min_strategy_bounded(synth, prism_handler)
        # print("STRATEGY", *strategy.items(), sep="\n")

    except Py4JNetworkError as err:
        print('Py4JNetworkError:', err)
        print("It is most likely that you forgot to start the PRISM java gateway. "
              "Compile and launch PrismEntryPoint.java!")
        sys.exit()
