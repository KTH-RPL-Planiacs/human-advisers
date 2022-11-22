import json
import networkx as nx
from game_synth.helpers import reduce_set_of_guards


def write_game(game, file_name):
    mapping = dict()
    for node in game.nodes:
        if len(node) == 3:
            new_node = (node[0], node[1], str(node[2]))
        else:
            new_node = node
        mapping[node] = new_node
    mapped_game = nx.relabel_nodes(game, mapping)

    with open(file_name, "w") as file:
        json.dump(mapped_game, file, default=nx.node_link_data)


def write_strategy(game, strat, safe_edges, fair_edges, file_name, modelled=False):
    json_dict = {}
    str_strat = {str(key): value for key, value in strat.items()}

    assert "safe_edges" not in str_strat.keys()
    assert "fair_edges" not in str_strat.keys()

    json_dict["strat"] = str_strat
    json_dict["safe_edges"] = []
    json_dict["fair_edges"] = []

    if modelled:
        # safety advisers
        for e in safe_edges:
            state_from = e[0]
            action = game.edges[e]["act"]
            adv_tuple = (state_from, action)
            json_dict["safe_edges"].append(adv_tuple)

        # fairness advisers
        for e in fair_edges:
            state_from = e[0]
            action = game.edges[e]["act"]
            adv_tuple = (state_from, action)
            json_dict["fair_edges"].append(adv_tuple)
    else:
        # ap order
        json_dict["guard_ap"] = game.graph["human_ap"]

        # safety advisers
        for e in safe_edges:
            state_from = e[0]
            action = reduce_set_of_guards(game.edges[e]["guards"])
            adv_tuple = (state_from, list(action))
            json_dict["safe_edges"].append(adv_tuple)

        # fairness advisers
        for e in fair_edges:
            state_from = e[0]
            action = reduce_set_of_guards(game.edges[e]["guards"])
            adv_tuple = (state_from, list(action))
            json_dict["fair_edges"].append(adv_tuple)

    with open(file_name, "w") as file:
        json.dump(json_dict, file)
