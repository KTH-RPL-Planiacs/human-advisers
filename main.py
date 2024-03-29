import sys
from copy import deepcopy
from prism_bridge.prism_bridge import PrismBridge
from py4j.protocol import Py4JNetworkError
from models.burgers import burger_robot_study, burger_human_study
from ltlf2dfa_nx.mona2nx import to_nxgraph
from ltlf2dfa_nx.parse_ltlf import to_mona
# from game_synth.modelled_human_game import create_game
from game_synth.modelless_human_game import create_game
from game_synth.helpers import remove_edges, remove_other_edges
from game_synth.strategy import has_winning_strategy, get_winning_strategy, has_coop_strategy, get_min_strategy_bounded
from advisers.safety import minimal_safety_edges
from advisers.fairness import minimal_fairness_edges, construct_fair_game
from models.io import write_game, write_strategy

if __name__ == "__main__":
    try:
        prism_handler = PrismBridge()
        print("Successfully connected to PRISM java gateway!")

        robot_model = burger_robot_study()
        human_model = burger_human_study()
        goals = "F buns_r && F patty_r && F lettuce_r && F (ketchup_r && ketchup_h) && F tomato_r"
        constraints = "G(!(buns_r && buns_h)) && G(!(patty_r && patty_h)) && G(!(lettuce_r && lettuce_h)) && G(!(tomato_r && tomato_h))"
        spec = goals + " && " + constraints
        #spec = "F (buns_r && buns_h) && G! lettuce_h"
        dfa = to_nxgraph(to_mona(spec))
        # we keep the original game for later
        orig_synth = create_game(robot_model, dfa)
        synth = deepcopy(orig_synth)
        print("Product created:", orig_synth)

        assert has_coop_strategy(synth, prism_handler), "From the start, game is unwinnable no matter what"
        print("Safety necessary:", not has_winning_strategy(synth, prism_handler))
        safety_edges = minimal_safety_edges(synth, prism_handler)
        print("Minimal safety assumptions:", len(safety_edges), "edges.")
        remove_edges(synth, safety_edges, prune_unreachable=True)

        assert has_coop_strategy(synth, prism_handler), "After safety assumptions, game is unwinnable no matter what"
        print("Fairness necessary:", not has_winning_strategy(synth, prism_handler))
        fairness_edges = minimal_fairness_edges(synth, prism_handler)
        print("Minimal fairness assumptions:", len(fairness_edges), "edges.")
        safe_and_fair_game = construct_fair_game(synth, fairness_edges)

        assert has_coop_strategy(safe_and_fair_game, prism_handler), "After fairness assumptions, game is unwinnable no matter what "
        assert has_winning_strategy(safe_and_fair_game, prism_handler), "After fairness assumptions, player 1 has no winning strategy "

        remove_other_edges(synth, fairness_edges)
        strategy = get_winning_strategy(safe_and_fair_game, prism_handler)
        # strategy = get_min_strategy_bounded(synth, prism_handler, safety=safety_edges, fairness=fairness_edges)
        print("Strategy computed.")

        # write results to files
        write_game(orig_synth, "game.json")
        write_strategy(orig_synth, strategy, safety_edges, fairness_edges, "strat.json")
        print("Strategy written to file.")

    except Py4JNetworkError as err:
        print('Py4JNetworkError:', err)
        print("It is most likely that you forgot to start the PRISM java gateway. "
              "Compile and launch PrismEntryPoint.java!")
        sys.exit()
