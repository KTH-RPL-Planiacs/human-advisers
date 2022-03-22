import networkx as nx


def corridor_mdp(r_id, init_state):
    m = nx.DiGraph()

    # graph information
    m.graph['name'] = 'robot' + r_id
    m.graph['init'] = init_state
    # order sensitive
    m.graph['ap'] = ['end_top' + r_id, 'corr_top' + r_id, 'crit' + r_id, 'corr_bot' + r_id, 'end_bot' + r_id]

    # player 1 states
    m.add_node('end_top', player=1, ap='10000')
    m.add_node('corridor_top', player=1, ap='01000')
    m.add_node('crit', player=1, ap='00100')
    m.add_node('corridor_bot', player=1, ap='00010')
    m.add_node('end_bot', player=1, ap='00001')

    # probabilistic states
    m.add_node('end_top_s', player=0)
    m.add_node('end_top_d', player=0)

    m.add_node('corridor_top_s', player=0)
    m.add_node('corridor_top_u', player=0)
    m.add_node('corridor_top_d', player=0)

    m.add_node('crit_u', player=0)
    m.add_node('crit_d', player=0)

    m.add_node('corridor_bot_s', player=0)
    m.add_node('corridor_bot_u', player=0)
    m.add_node('corridor_bot_d', player=0)

    m.add_node('end_bot_s', player=0)
    m.add_node('end_bot_u', player=0)

    # player 1 edges
    m.add_edge('end_top', 'end_top_s', act='stay')
    m.add_edge('end_top', 'end_top_d', act='down')

    m.add_edge('corridor_top', 'corridor_top_s', act='stay')
    m.add_edge('corridor_top', 'corridor_top_u', act='up')
    m.add_edge('corridor_top', 'corridor_top_d', act='down')

    m.add_edge('crit', 'crit_u', act='up')
    m.add_edge('crit', 'crit_d', act='down')

    m.add_edge('corridor_bot', 'corridor_bot_s', act='stay')
    m.add_edge('corridor_bot', 'corridor_bot_u', act='up')
    m.add_edge('corridor_bot', 'corridor_bot_d', act='down')

    m.add_edge('end_bot', 'end_bot_s', act='stay')
    m.add_edge('end_bot', 'end_bot_u', act='up')

    # probabilistic edges - deterministic here
    m.add_edge('end_top_s', 'end_top', prob=1.0)
    m.add_edge('end_top_d', 'corridor_top', prob=1.0)

    m.add_edge('corridor_top_s', 'corridor_top', prob=1.0)
    m.add_edge('corridor_top_u', 'end_top', prob=1.0)
    m.add_edge('corridor_top_d', 'crit', prob=1.0)

    m.add_edge('crit_u', 'corridor_top', prob=1.0)
    m.add_edge('crit_d', 'corridor_bot', prob=1.0)

    m.add_edge('corridor_bot_s', 'corridor_bot', prob=1.0)
    m.add_edge('corridor_bot_u', 'crit', prob=1.0)
    m.add_edge('corridor_bot_d', 'end_bot', prob=1.0)

    m.add_edge('end_bot_s', 'end_bot', prob=1.0)
    m.add_edge('end_bot_u', 'corridor_bot', prob=1.0)
    return m
