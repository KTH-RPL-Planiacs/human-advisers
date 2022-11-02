import json
import networkx as nx


def write_game(game, file_name):
    with open(file_name, "w") as file:
        json.dump(game, file, default=nx.node_link_data)


def write_strategy(game, strat, safe_edges, fair_edges, file_name):
    json_dict = {}
    str_strat = {str(key): value for key, value in strat.items()}

    assert "safe_edges" not in str_strat.keys()
    assert "fair_edges" not in str_strat.keys()

    json_dict["strat"] = str_strat

    # safety advisers
    json_dict["safe_edges"] = []
    for e in safe_edges:
        state_from = e[0]
        action = game.edges[e]["act"]
        adv_tuple = (state_from, action)
        json_dict["safe_edges"].append(adv_tuple)

    # fairness advisers
    json_dict["fair_edges"] = []
    for e in safe_edges:
        state_from = e[0]
        action = game.edges[e]["act"]
        adv_tuple = (state_from, action)
        json_dict["fair_edges"].append(adv_tuple)

    with open(file_name, "w") as file:
        json.dump(json_dict, file)
