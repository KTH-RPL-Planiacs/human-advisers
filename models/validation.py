import networkx as nx


def is_valid(mdp):
    return is_probabilites_valid(mdp)


def is_probabilites_valid(mdp):
    for node in mdp.nodes:
        if mdp.nodes[node]["player"] != 0:
            continue

        total_prob = 0.0
        for succ in mdp.successors(node):
            total_prob += mdp.edges[node, succ]["prob"]

        if abs(total_prob - 1.0) > 0.01:
            return False

    return True
