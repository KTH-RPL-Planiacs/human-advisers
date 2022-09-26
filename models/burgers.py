import networkx as nx
from models.validation import is_valid


def burger_robot_study():
    m = nx.DiGraph()

    # graph information
    m.graph['name'] = 'burger_robot'
    m.graph['init'] = 'del'
    # order sensitive
    m.graph['ap'] = ['buns_r', 'patty_r', 'lettuce_r', 'ketchup_r', 'tomato_r', 'delivery_r']

    # player 1 states
    # ingredients
    m.add_node('01', player=1, ap='000000')
    m.add_node('11', player=1, ap='000000')
    m.add_node('21', player=1, ap='000000')
    m.add_node('31', player=1, ap='000000')
    m.add_node('41', player=1, ap='000000')
    # ingredients interact
    m.add_node('01i', player=1, ap='100000')
    m.add_node('11i', player=1, ap='010000')
    m.add_node('21i', player=1, ap='001000')
    m.add_node('31i', player=1, ap='000100')
    m.add_node('41i', player=1, ap='000010')
    # delivery
    m.add_node('20', player=1, ap='000000')
    m.add_node('20i', player=1, ap='000001')

    # probabilistic states
    m.add_node('20_idle', player=0)
    m.add_node('20_up', player=0)
    m.add_node('20_interact', player=0)

    m.add_node('01_idle', player=0)
    m.add_node('01_right', player=0)
    m.add_node('01_interact', player=0)

    m.add_node('11_idle', player=0)
    m.add_node('11_left', player=0)
    m.add_node('11_right', player=0)
    m.add_node('11_interact', player=0)

    m.add_node('21_idle', player=0)
    m.add_node('21_down', player=0)
    m.add_node('21_left', player=0)
    m.add_node('21_right', player=0)
    m.add_node('21_interact', player=0)

    m.add_node('31_idle', player=0)
    m.add_node('31_left', player=0)
    m.add_node('31_right', player=0)
    m.add_node('31_interact', player=0)

    m.add_node('41_idle', player=0)
    m.add_node('41_left', player=0)
    m.add_node('41_interact', player=0)

    m.add_node('01i_interact', player=0)
    m.add_node('11i_interact', player=0)
    m.add_node('21i_interact', player=0)
    m.add_node('31i_interact', player=0)
    m.add_node('41i_interact', player=0)
    m.add_node('20i_interact', player=0)

    # player 1 edges
    m.add_edge('20', '20_idle', act='idle')
    m.add_edge('20', '20_up', act='up')
    m.add_edge('20', '20_interact', act='interact')

    m.add_edge('01', '01_idle', act='idle')
    m.add_edge('01', '01_right', act='right')
    m.add_edge('01', '01_interact', act='interact')

    m.add_edge('11', '11_idle', act='idle')
    m.add_edge('11', '11_left', act='left')
    m.add_edge('11', '11_right', act='right')
    m.add_edge('11', '11_interact', act='interact')

    m.add_edge('21', '21_idle', act='idle')
    m.add_edge('21', '21_down', act='down')
    m.add_edge('21', '21_left', act='left')
    m.add_edge('21', '21_right', act='right')
    m.add_edge('21', '21_interact', act='interact')

    m.add_edge('31', '31_idle', act='idle')
    m.add_edge('31', '31_left', act='left')
    m.add_edge('31', '31_right', act='right')
    m.add_edge('31', '31_interact', act='interact')

    m.add_edge('41', '41_idle', act='idle')
    m.add_edge('41', '41_left', act='left')
    m.add_edge('41', '41_interact', act='interact')

    m.add_edge('01i', '01i_interact', act='interact')
    m.add_edge('11i', '11i_interact', act='interact')
    m.add_edge('21i', '21i_interact', act='interact')
    m.add_edge('31i', '31i_interact', act='interact')
    m.add_edge('41i', '41i_interact', act='interact')
    m.add_edge('20i', '20i_interact', act='interact')

    # probabilistic edges
    m.add_edge('20_idle', '20', prob=1.0)
    m.add_edge('20_up', '21', prob=1.0)
    m.add_edge('20_interact', '20i', prob=1.0)

    m.add_edge('01_idle', '01', prob=1.0)
    m.add_edge('01_right', '11', prob=1.0)
    m.add_edge('01_interact', '01i', prob=1.0)

    m.add_edge('11_idle', '11', prob=1.0)
    m.add_edge('11_left', '01', prob=1.0)
    m.add_edge('11_right', '21', prob=1.0)
    m.add_edge('11_interact', '11i', prob=1.0)

    m.add_edge('21_idle', '21', prob=1.0)
    m.add_edge('21_down', '20', prob=1.0)
    m.add_edge('21_left', '11', prob=1.0)
    m.add_edge('21_right', '31', prob=1.0)
    m.add_edge('21_interact', '21i', prob=1.0)

    m.add_edge('31_idle', '31', prob=1.0)
    m.add_edge('31_left', '21', prob=1.0)
    m.add_edge('31_right', '41', prob=1.0)
    m.add_edge('31_interact', '31i', prob=1.0)

    m.add_edge('41_idle', '41', prob=1.0)
    m.add_edge('41_left', '31', prob=1.0)
    m.add_edge('41_interact', '41i', prob=1.0)

    m.add_edge('01i_interact', '01', prob=1.0)
    m.add_edge('11i_interact', '01', prob=1.0)
    m.add_edge('21i_interact', '01', prob=1.0)
    m.add_edge('31i_interact', '01', prob=1.0)
    m.add_edge('41i_interact', '01', prob=1.0)
    m.add_edge('20i_interact', '01', prob=1.0)

    is_valid(m)
    return m


