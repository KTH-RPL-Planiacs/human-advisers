import networkx as nx
import queue


def create_game(mdp_r, dfa, mdp_h):
    synth = nx.DiGraph()
    synth.graph['acc'] = []  # list of accepting states

    # initial state
    dfa_init = dfa.graph['init']
    robot_init = mdp_r.graph['init']
    human_init = mdp_h.graph['init']
    synth_init = (robot_init, human_init, dfa_init)

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

    return synth
