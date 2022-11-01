import sys
from copy import deepcopy
from prism_bridge.prism_bridge import PrismBridge
from py4j.protocol import Py4JNetworkError
from models.burgers import burger_robot_study, burger_human_study
from ltlf2dfa_nx.mona2nx import to_nxgraph
from ltlf2dfa_nx.parse_ltlf import to_mona
from game_synth.modelled_human_game import create_game
from game_synth.helpers import remove_edges, remove_other_edges
from game_synth.strategy import has_winning_strategy, get_winning_strategy, has_coop_strategy, get_min_strategy_bounded
from advisers.safety import minimal_safety_edges
from advisers.fairness import minimal_fairness_edges, construct_fair_game, union_minimal_fairness_egdes
from visualization.interactive_viz import InteractiveViz
from visualization.robot_controller import AdviserRobotController
from models.io import write_game, write_strategy

if __name__ == "__main__":
    try:
        prism_handler = PrismBridge()
        print("Successfully connected to PRISM java gateway!")

        robot_model = burger_robot_study()
        human_model = burger_human_study()
        spec = "F(delivery_r)"
        dfa = to_nxgraph(to_mona(spec))
        # we keep the original game for later
        orig_synth = create_game(robot_model, human_model, dfa)
        synth = deepcopy(orig_synth)

        assert has_coop_strategy(synth, prism_handler), "From the start, game is unwinnable no matter what"
        print("Safety necessary:", not has_winning_strategy(synth, prism_handler))
        safety_edges = minimal_safety_edges(synth, prism_handler)
        print("SAFETY ASSUM", *safety_edges, sep="\n")
        remove_edges(synth, safety_edges, prune_unreachable=True)

        assert has_coop_strategy(synth, prism_handler), "After safety assumptions, game is unwinnable no matter what"
        print("Fairness necessary:", not has_winning_strategy(synth, prism_handler))
        # fairness_edges = union_minimal_fairness_egdes(synth, prism_handler)
        fairness_edges = minimal_fairness_edges(synth, prism_handler)
        print("FAIRNESS ASSUM", *fairness_edges, sep="\n")
        safe_and_fair_game = construct_fair_game(synth, fairness_edges)

        assert has_coop_strategy(safe_and_fair_game, prism_handler), "After fairness assumptions, game is unwinnable " \
                                                                     "no matter what "
        assert has_winning_strategy(safe_and_fair_game, prism_handler), "After fairness assumptions, player 1 has no " \
                                                                        "winning strategy "

        remove_other_edges(synth, fairness_edges)
        strategy = get_winning_strategy(safe_and_fair_game, prism_handler)
        # strategy = get_min_strategy_bounded(synth, prism_handler, safety=safety_edges, fairness=fairness_edges)
        controller = AdviserRobotController(orig_synth, strategy, safety_edges, fairness_edges)
        write_game(orig_synth, "game.json")
        write_strategy(orig_synth, strategy, safety_edges, fairness_edges, "strat.json")

        """
        # state to coord mapping
        corridor_mdp_coords = {
            'end_top': (0, 0),
            'corridor_top': (0, 1),
            'crit': (0, 2),
            'corridor_bot': (0, 3),
            'end_bot': (0, 4),
        }

        ex_grid = [[0 for col in range(1)] for row in range(5)]
        viz = InteractiveViz(controller, grid=ex_grid, state_coord_map=corridor_mdp_coords, grid_size_x=200, grid_size_y=1000)
        viz.run_loop()
        """

    except Py4JNetworkError as err:
        print('Py4JNetworkError:', err)
        print("It is most likely that you forgot to start the PRISM java gateway. "
              "Compile and launch PrismEntryPoint.java!")
        sys.exit()
