import networkx as nx
import queue
from game_synth.helpers import powerset, create_guard, group_and_flip, sog_fits_to_guard


def create_game(mdp, dfa):
    synth = nx.DiGraph()
    synth.graph['acc'] = []  # list of accepting states

    # initial state
    dfa_init = dfa.graph['init']
    mdp_init = mdp.graph['init']
    synth_init = (mdp_init, dfa_init)

    if dfa_init in dfa.graph['acc']:
        synth.graph['acc'].append(synth_init)

    synth.add_node(synth_init, player=1, ap=mdp.nodes[mdp_init]['ap'][0])
    synth.graph['init'] = synth_init

    # dfa and mdp atomic propositions
    dfa_ap = dfa.graph['ap']
    mdp_ap = mdp.graph['ap']
    synth.graph['ap'] = mdp_ap  # order sensitive because of the edge guards
    env_ap = list(set(dfa_ap).difference(set(mdp_ap)))  # order sensitive
    synth.graph['env_ap'] = env_ap
    joined_ap = mdp_ap + env_ap

    # queue of open states
    que = queue.Queue()
    que.put(synth_init)  # initialize the queue

    # work the queue
    while not que.empty():
        synth_from = que.get()
        mdp_from = synth_from[0]
        dfa_from = synth_from[1]

        assert synth.nodes[synth_from]['player'] in [1, 2, 0], "Each state need to belong to player 1,2 or 0!"

        # player 1 states, mdp gets to move
        if synth.nodes[synth_from]['player'] == 1:
            # for all possible mdp moves
            for mdp_succ in mdp.successors(mdp_from):
                assert mdp.nodes[mdp_succ]['player'] == 0  # this should be a probabilistic state in the mdp
                # add the new state to the synthesis product and connect it
                synth_succ = (mdp_succ, dfa_from)
                if not synth.has_node(synth_succ):
                    synth.add_node(synth_succ, player=2)
                    que.put(synth_succ)  # put new states in queue
                synth.add_edge(synth_from, synth_succ, act=mdp.edges[mdp_from, mdp_succ]['act'])

        # player 2 states, opponent fills out "missing" propositions
        elif synth.nodes[synth_from]['player'] == 2:
            results = {}  # possible outcomes are stored

            for opt in powerset(env_ap):
                # generate guard for chosen option
                opt_guard = create_guard(opt, env_ap)
                results[opt_guard] = []

                for mdp_succ in mdp.successors(mdp_from):
                    # generate configuration guard for chosen option and potential next mdp state
                    mdp_obs = mdp.nodes[mdp_succ]['ap'][0]
                    config = mdp_obs + opt_guard

                    for dfa_succ in dfa.successors(dfa_from):
                        # check if config matches at least one dfa guard
                        matched_guards = sog_fits_to_guard(config, dfa.edges[dfa_from, dfa_succ]['guard'],
                                                           joined_ap, dfa_ap)
                        if len(matched_guards) > 0:  # this config matches to this dfa successor
                            results[opt_guard].append((mdp_succ, dfa_succ))

            # flip and group the results to see which options lead to the same results
            grouped_results = group_and_flip(results)

            for res, opts in grouped_results.items():
                # TODO: simplify guards for each grouped option

                # create a probabilistic state, add it and connect it
                synth_succ = (mdp_from, dfa_from, frozenset(opts))
                if not synth.has_node(synth_succ):
                    synth.add_node(synth_succ, player=0, res=res)
                    que.put(synth_succ)  # put new states in queue
                synth.add_edge(synth_from, synth_succ, guards=opts)

        # player 3 states, probabilistic function moves and dfa moves accordingly
        elif synth.nodes[synth_from]['player'] == 0:
            for synth_succ in synth.nodes[synth_from]['res']:
                mdp_succ = synth_succ[0]
                dfa_succ = synth_succ[1]

                if not synth.has_node(synth_succ):
                    synth.add_node(synth_succ, player=1, ap=mdp.nodes[mdp_succ]['ap'][0])
                    if dfa_succ in dfa.graph['acc']:
                        synth.graph['acc'].append(synth_succ)
                    que.put(synth_succ)  # put new states in queue
                synth.add_edge(synth_from, synth_succ, prob=mdp.edges[mdp_from, mdp_succ]['prob'])
            # res is only temporarily needed for creation of player 3 state successors, not in the final product
            del synth.nodes[synth_from]['res']

    return synth
