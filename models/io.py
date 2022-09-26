import json
import networkx as nx


def write_game(game, file_name):
    with open(file_name, "w") as file:
        json.dump(game, file, default=nx.node_link_data)


def write_strategy(strat, safe_edges, fair_edges, file_name):
    json_dict = {}
    str_strat = {str(key): value for key, value in strat.items()}

    assert "safe_edges" not in str_strat.keys()
    assert "fair_edges" not in str_strat.keys()

    json_dict["strat"] = str_strat
    json_dict["safe_edges"] = [str(e) for e in safe_edges]
    json_dict["fair_edges"] = [str(e) for e in fair_edges]

    with open(file_name, "w") as file:
        json.dump(json_dict, file)
