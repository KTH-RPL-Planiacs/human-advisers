from prism_bridge.prism_bridge import PrismBridge
from py4j.protocol import Py4JNetworkError
from models.corridor import corridor_mdp
from ltlf2dfa_nx.mona2nx import to_nxgraph
from ltlf2dfa_nx.parse_ltlf import to_mona
from game_synth.modelless_human_game import create_game
from game_synth.helpers import remove_edges
from advisers.safety import minimal_safety_edges
from advisers.fairness import minimal_fairness_edges

if __name__ == "__main__":
    try:
        prism_handler = PrismBridge()
        print("Successfully connected to PRISM java gateway!")

        mdp = corridor_mdp("_r", "end_top")
        human_model = corridor_mdp("_h", "end_bot")
        spec = "F(end_top_r) && G(!(crit_r && crit_h))"
        dfa = to_nxgraph(to_mona(spec))
        synth = create_game(mdp, dfa)
        safety_edges = minimal_safety_edges(synth, prism_handler)
        remove_edges(synth, safety_edges)
        fairness_edges = minimal_fairness_edges(synth, prism_handler)
        print("SAFETY ASSUM", safety_edges)
        print("FAIRNESS ASSUM", fairness_edges)

    except Py4JNetworkError as err:
        print('Py4JNetworkError:', err)
        print("It is most likely that you forgot to start the PRISM java gateway. "
              "Compile and launch PrismEntryPoint.java!")

