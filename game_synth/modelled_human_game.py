import networkx as nx
import queue

from game_synth.helpers import sog_fits_to_guard


def create_game(mdp_r, mdp_h, dfa):
    synth = nx.DiGraph()
    synth.graph['acc'] = []  # list of accepting states

    # initial state
    dfa_init = dfa.graph['init']
    robot_init = mdp_r.graph['init']
    human_init = mdp_h.graph['init']
    synth_init = (robot_init, human_init, dfa_init, 1)

    if dfa_init in dfa.graph['acc']:
        synth.graph['acc'].append(synth_init)

    init_ap = mdp_r.nodes[robot_init]['ap'] + mdp_h.nodes[human_init]['ap']
    synth.add_node(synth_init, player=1, ap=init_ap)
    synth.graph['init'] = synth_init

    # dfa and mdp atomic propositions
    spec_ap = dfa.graph['ap']
    robot_ap = mdp_r.graph['ap']
    human_ap = mdp_h.graph['ap']
    joined_ap = robot_ap + human_ap
    relevant_human_ap = list(set(human_ap).intersection(set(spec_ap)))
    synth.graph['ap_r'] = robot_ap
    synth.graph['ap_h'] = human_ap
    assert set(spec_ap).issubset(set(joined_ap))

    # queue of open states
    que = queue.Queue()
    que.put(synth_init)  # initialize the queue

    # work the queue
    while not que.empty():
        synth_from = que.get()
        mdp_r_from = synth_from[0]
        mdp_h_from = synth_from[1]
        dfa_from = synth_from[2]
        player = synth_from[3]

        assert synth.nodes[synth_from]['player'] in [1, 2, 0], "Each state need to belong to player 1,2 or 0!"
        assert synth.nodes[synth_from]['player'] == player
        # player 1 states, robot moves
        if player == 1:
            # for all possible robot moves
            for robot_succ in mdp_r.successors(mdp_r_from):
                # this should be a probabilistic state in the robot mdp
                assert mdp_r.nodes[robot_succ]['player'] == 0
                # add the new state to the synthesis product and connect it
                synth_succ = (robot_succ, mdp_h_from, dfa_from, 0)
                if not synth.has_node(synth_succ):
                    synth.add_node(synth_succ, player=0)
                    que.put(synth_succ)  # put new states in queue
                action_lbl = mdp_r.edges[mdp_r_from, robot_succ]['act']
                synth.add_edge(synth_from, synth_succ, act=action_lbl)

        # player 2 states, human moves
        if player == 2:
            # for all possible human moves
            for human_succ in mdp_h.successors(mdp_h_from):
                # this should be a probabilistic state in the human mdp
                assert mdp_h.nodes[human_succ]['player'] == 0
                # add the new state to the synthesis product and connect it
                synth_succ = (mdp_r_from, human_succ, dfa_from, 0)
                if not synth.has_node(synth_succ):
                    synth.add_node(synth_succ, player=0)
                    que.put(synth_succ)  # put new states in queue
                action_lbl = mdp_h.edges[mdp_h_from, human_succ]['act']
                synth.add_edge(synth_from, synth_succ, act=action_lbl)

        # probabilistic states
        if player == 0:
            assert sum(1 for _ in synth.predecessors(synth_from)) == 1
            pred = next(synth.predecessors(synth_from))

            # case 1: after p1 state, just resolve probabilistic event for robot
            if synth.nodes[pred]['player'] == 1:
                for robot_succ in mdp_r.successors(mdp_r_from):
                    # this should be a player1 state in the robot mdp
                    assert mdp_r.nodes[robot_succ]['player'] == 1
                    # get the resulting joined ap
                    cur_ap = mdp_r.nodes[robot_succ]['ap'] + mdp_h.nodes[mdp_h_from]['ap']
                    # based on new observation (cur_ap), update the dfa state
                    for dfa_succ in dfa.successors(dfa_from):
                        # check if config matches at least one dfa guard, skip non-matching
                        dfa_guard = dfa.edges[dfa_from, dfa_succ]['guard']
                        matched_guards = sog_fits_to_guard(cur_ap, dfa_guard, joined_ap, spec_ap)
                        if len(matched_guards) == 0:
                            continue

                        # add the new state to the synthesis product and connect it
                        synth_succ = (robot_succ, mdp_h_from, dfa_succ, 2)
                        if not synth.has_node(synth_succ):
                            synth.add_node(synth_succ, player=2, ap=cur_ap)
                            que.put(synth_succ)  # put new states in queue
                            if dfa_succ in dfa.graph['acc']:
                                synth.graph['acc'].append(synth_succ)
                        prob = mdp_r.edges[mdp_r_from, robot_succ]['prob']
                        synth.add_edge(synth_from, synth_succ, prob=prob)

            # case 2: after p2 state, resolve probabilistic event for human, also update DFA
            elif synth.nodes[pred]['player'] == 2:
                for human_succ in mdp_h.successors(mdp_h_from):
                    # this should be a player1 state in the human mdp
                    assert mdp_h.nodes[human_succ]['player'] == 1
                    # get the resulting joined ap
                    cur_ap = mdp_r.nodes[mdp_r_from]['ap'] + mdp_h.nodes[human_succ]['ap']

                    # based on new observation (cur_ap), update the dfa state
                    for dfa_succ in dfa.successors(dfa_from):
                        # check if config matches at least one dfa guard, skip non-matching
                        dfa_guard = dfa.edges[dfa_from, dfa_succ]['guard']
                        matched_guards = sog_fits_to_guard(cur_ap, dfa_guard, joined_ap, spec_ap)
                        if len(matched_guards) == 0:
                            continue

                        # add the new state to the synthesis product and connect it
                        synth_succ = (mdp_r_from, human_succ, dfa_succ, 1)
                        if not synth.has_node(synth_succ):
                            synth.add_node(synth_succ, player=1, ap=cur_ap)
                            que.put(synth_succ)  # put new states in queue
                            if dfa_succ in dfa.graph['acc']:
                                synth.graph['acc'].append(synth_succ)
                        prob = mdp_h.edges[mdp_h_from, human_succ]['prob']
                        synth.add_edge(synth_from, synth_succ, prob=prob)
            else:
                assert False, "probabilistic state with invalid predecessor"

    return synth
