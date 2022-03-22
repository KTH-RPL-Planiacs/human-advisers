from prism_bridge.prism_bridge import PrismBridge
from py4j.protocol import Py4JNetworkError
from models.corridor import corridor_mdp
from ltlf2dfa_nx.mona2nx import to_nxgraph
from ltlf2dfa_nx.parse_ltlf import to_mona
from game_synth.modelless_human_game import create_game

if __name__ == "__main__":
    try:
        prism_handler = PrismBridge()
        print("Successfully connected to PRISM java gateway!")

        mdp = corridor_mdp("R", "end_top")
        spec = "F(end_top_r) && G(!(crit_r && crit_h))"
        dfa = to_nxgraph(to_mona(spec))
        synth = create_game(mdp, dfa)

    except Py4JNetworkError as err:
        print('Py4JNetworkError:', err)
        print("It is most likely that you forgot to start the PRISM java gateway. "
              "Compile and launch PrismEntryPoint.java!")

