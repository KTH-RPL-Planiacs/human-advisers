import json
import networkx as nx
from game_synth.helpers import reduce_set_of_guards


def write_game(game, file_name):
    mapping = dict()
    for node in game.nodes:
        if len(node) == 3:
            new_node = (node[0], node[1], str(node[2]))
        else:
            new_node = (node[0], node[1], "")
        mapping[node] = new_node
    mapped_game = nx.relabel_nodes(game, mapping)

    init_state = mapped_game.graph["init"]
    mapped_game.graph["init"] = (init_state[0], init_state[1], "")

    mapped_acc = []
    for acc_state in mapped_game.graph["acc"]:
        mapped_acc.append((acc_state[0], acc_state[1], ""))
    mapped_game.graph["acc"] = mapped_acc

    with open(file_name, "w") as file:
        json.dump(mapped_game, file, default=nx.node_link_data)


def write_strategy(game, strat, safe_edges, fair_edges, file_name):
    json_dict = {}
    str_strat = {str(key): value for key, value in strat.items()}

    assert "safe_edges" not in str_strat.keys()
    assert "fair_edges" not in str_strat.keys()

    json_dict["strat"] = str_strat
    json_dict["safety_adv"] = []
    json_dict["fairness_adv"] = []

    # ap order
    json_dict["guard_ap"] = game.graph["human_ap"]

    # safety advisers
    for e in safe_edges:
        state_from = e[0]
        action = reduce_set_of_guards(game.edges[e]["guards"])
        mapped_state = (state_from[0], state_from[1], "")
        adv_tuple = (mapped_state, list(action))
        json_dict["safety_adv"].append(adv_tuple)

    # fairness advisers
    for e in fair_edges:
        state_from = e[0]
        action = reduce_set_of_guards(game.edges[e]["guards"])
        mapped_state = (state_from[0], state_from[1], "")
        adv_tuple = (mapped_state, list(action))
        json_dict["fairness_adv"].append(adv_tuple)

    with open(file_name, "w") as file:
        json.dump(json_dict, file)
