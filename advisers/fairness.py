from prism_bridge.prism_io import write_prism_model

import copy
import random


def construct_fair_game(synth, fairness_edges):
    if len(fairness_edges) == 0:
        return synth

    fairness_synth = copy.deepcopy(synth)
    fairness_dict = {}
    for edge in fairness_edges:
        if edge[0] not in fairness_dict.keys():
            fairness_dict[edge[0]] = [edge]
        else:
            fairness_dict[edge[0]].append(edge)

    for node, data in synth.nodes(data=True):
        # skip the nodes that don't have any fairness edges
        if node not in fairness_dict.keys():
            continue
        # create a probabilistic node between player-1 and player-2 node
        prob_node = node + ('fair',)
        # add the probabilistic node
        fairness_synth.add_node(prob_node, player=0)
        # re-route incoming edges
        for pred in synth.predecessors(node):
            fairness_synth.remove_edge(pred, node)
            assert 'prob' in synth.edges[pred, node], 'EDGE (' + str(pred) + ',' + str(node) + ') does not have prob, but should'
            fairness_synth.add_edge(pred, prob_node, prob=synth.edges[pred, node]['prob'])
        # add edge representing the player being free to chose
        fairness_synth.add_edge(prob_node, node, prob=(1/(1+len(fairness_dict[node]))))
        # add edges representing player-2 being forced to be fair
        for fair_edge in fairness_dict[node]:
            action = synth.edges[fair_edge]["act"]
            fairness_node_label = "force_" + action
            promise_node = node + (fairness_node_label,)

            fairness_synth.add_node(promise_node, player=2)
            fairness_synth.add_edge(prob_node, promise_node, prob=(1 / (1 + len(fairness_dict[node]))))
            fairness_synth.add_edge(promise_node, fair_edge[1], act=action)

    return fairness_synth


def minimal_fairness_edges(synth, prism_handler):
    # check if fairness is necessary
    win_prop = '<< p1 >> Pmax=? [F \"accept\"]'
    # PRISM translations
    prism_model, state_ids = write_prism_model(synth, "fairness")
    prism_handler.load_model_file(prism_model)
    result = prism_handler.check_property(win_prop)

    winnable = result[state_ids[synth.graph['init']]] >= 0.999
    if winnable:
        # fairness is not necessary
        return []

    # fairness is necessary
    # start by assuming all player-2 edges are necessary
    fairness_edges = []
    for node in synth.nodes:
        if synth.nodes[node]["player"] != 2:
            continue
        for succ in synth.successors(node):
            fairness_edges.append((node, succ))

    # TODO: remove all edges from nodes where player 2 has only a single choice (will never need fairness)
    assume_fair_synth = construct_fair_game(synth, fairness_edges)

    # PRISM translations
    prism_model, state_ids = write_prism_model(assume_fair_synth, "fairness")
    prism_handler.load_model_file(prism_model)
    result = prism_handler.check_property(win_prop)

    init_win_prob = result[state_ids[assume_fair_synth.graph['init']]]
    assert init_win_prob >= 0.999, "no fairness edges will work"

    # minimize the set of fairness edges
    minimal = False
    while not minimal:

        # greedy chopping time
        guess = int(len(fairness_edges) / 2)
        while guess >= 1:
            selection = random.sample(fairness_edges, guess)
            assume_fair_synth = construct_fair_game(synth, selection)

            # PRISM translations
            prism_model, state_ids = write_prism_model(assume_fair_synth, "fairness")
            prism_handler.load_model_file(prism_model)
            result = prism_handler.check_property(win_prop)

            # check if the chosen edge is removable
            if result[state_ids[assume_fair_synth.graph['init']]] > 0.999:
                fairness_edges = selection
                guess = int(len(fairness_edges) / 2)
            else:
                guess = int(guess / 2)

        # thorough search
        removable_edge = None
        for fair_edge in fairness_edges:
            index = fairness_edges.index(fair_edge)
            try_fair_edges = fairness_edges[:index] + fairness_edges[(index + 1):]
            assume_fair_synth = construct_fair_game(synth, try_fair_edges)

            # PRISM translations
            prism_model, state_ids = write_prism_model(assume_fair_synth, "fairness")
            prism_handler.load_model_file(prism_model)
            result = prism_handler.check_property(win_prop)

            # check if the chosen edge is removable
            if result[state_ids[assume_fair_synth.graph['init']]] >= 0.999:
                removable_edge = fair_edge
                break

        if removable_edge is None:
            # the set has to be minimal
            minimal = True
        else:
            fairness_edges.remove(removable_edge)

    return fairness_edges
