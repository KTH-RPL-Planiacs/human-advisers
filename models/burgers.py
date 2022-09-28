import networkx as nx
from models.validation import is_valid


def burger_robot_study():
    m = nx.DiGraph()

    # graph information
    m.graph['name'] = 'burger_robot'
    m.graph['init'] = '20'
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
    m.add_edge('11i_interact', '11', prob=1.0)
    m.add_edge('21i_interact', '21', prob=1.0)
    m.add_edge('31i_interact', '31', prob=1.0)
    m.add_edge('41i_interact', '41', prob=1.0)
    m.add_edge('20i_interact', '20', prob=1.0)

    is_valid(m)
    return m


def burger_human_study():
    m = nx.DiGraph()

    # graph information
    m.graph['name'] = 'burger_human'
    m.graph['init'] = '24'
    # order sensitive
    m.graph['ap'] = ['buns_h', 'patty_h', 'lettuce_h', 'ketchup_h', 'tomato_h', 'delivery_h']

    # player 1 states
    # ingredients
    m.add_node('03', player=1, ap='000000')
    m.add_node('13', player=1, ap='000000')
    m.add_node('23', player=1, ap='000000')
    m.add_node('33', player=1, ap='000000')
    m.add_node('43', player=1, ap='000000')
    # ingredients interact
    m.add_node('03i', player=1, ap='100000')
    m.add_node('13i', player=1, ap='010000')
    m.add_node('23i', player=1, ap='001000')
    m.add_node('33i', player=1, ap='000100')
    m.add_node('43i', player=1, ap='000010')
    # delivery
    m.add_node('24', player=1, ap='000000')
    m.add_node('24i', player=1, ap='000001')

    # probabilistic states
    m.add_node('24_idle', player=0)
    m.add_node('24_down', player=0)
    m.add_node('24_interact', player=0)

    m.add_node('03_idle', player=0)
    m.add_node('03_right', player=0)
    m.add_node('03_interact', player=0)

    m.add_node('13_idle', player=0)
    m.add_node('13_left', player=0)
    m.add_node('13_right', player=0)
    m.add_node('13_interact', player=0)

    m.add_node('23_idle', player=0)
    m.add_node('23_up', player=0)
    m.add_node('23_left', player=0)
    m.add_node('23_right', player=0)
    m.add_node('23_interact', player=0)

    m.add_node('33_idle', player=0)
    m.add_node('33_left', player=0)
    m.add_node('33_right', player=0)
    m.add_node('33_interact', player=0)

    m.add_node('43_idle', player=0)
    m.add_node('43_left', player=0)
    m.add_node('43_interact', player=0)

    m.add_node('03i_interact', player=0)
    m.add_node('13i_interact', player=0)
    m.add_node('23i_interact', player=0)
    m.add_node('33i_interact', player=0)
    m.add_node('43i_interact', player=0)
    m.add_node('24i_interact', player=0)

    # player 1 edges
    m.add_edge('24', '24_idle', act='idle')
    m.add_edge('24', '24_down', act='down')
    m.add_edge('24', '24_interact', act='interact')

    m.add_edge('03', '03_idle', act='idle')
    m.add_edge('03', '03_right', act='right')
    m.add_edge('03', '03_interact', act='interact')

    m.add_edge('13', '13_idle', act='idle')
    m.add_edge('13', '13_left', act='left')
    m.add_edge('13', '13_right', act='right')
    m.add_edge('13', '13_interact', act='interact')

    m.add_edge('23', '23_idle', act='idle')
    m.add_edge('23', '23_up', act='up')
    m.add_edge('23', '23_left', act='left')
    m.add_edge('23', '23_right', act='right')
    m.add_edge('23', '23_interact', act='interact')

    m.add_edge('33', '33_idle', act='idle')
    m.add_edge('33', '33_left', act='left')
    m.add_edge('33', '33_right', act='right')
    m.add_edge('33', '33_interact', act='interact')

    m.add_edge('43', '43_idle', act='idle')
    m.add_edge('43', '43_left', act='left')
    m.add_edge('43', '43_interact', act='interact')

    m.add_edge('03i', '03i_interact', act='interact')
    m.add_edge('13i', '13i_interact', act='interact')
    m.add_edge('23i', '23i_interact', act='interact')
    m.add_edge('33i', '33i_interact', act='interact')
    m.add_edge('43i', '43i_interact', act='interact')
    m.add_edge('24i', '24i_interact', act='interact')

    # probabilistic edges
    m.add_edge('24_idle', '24', prob=1.0)
    m.add_edge('24_down', '23', prob=1.0)
    m.add_edge('24_interact', '24i', prob=1.0)

    m.add_edge('03_idle', '03', prob=1.0)
    m.add_edge('03_right', '13', prob=1.0)
    m.add_edge('03_interact', '03i', prob=1.0)

    m.add_edge('13_idle', '13', prob=1.0)
    m.add_edge('13_left', '03', prob=1.0)
    m.add_edge('13_right', '23', prob=1.0)
    m.add_edge('13_interact', '13i', prob=1.0)

    m.add_edge('23_idle', '23', prob=1.0)
    m.add_edge('23_up', '24', prob=1.0)
    m.add_edge('23_left', '13', prob=1.0)
    m.add_edge('23_right', '33', prob=1.0)
    m.add_edge('23_interact', '23i', prob=1.0)

    m.add_edge('33_idle', '33', prob=1.0)
    m.add_edge('33_left', '23', prob=1.0)
    m.add_edge('33_right', '43', prob=1.0)
    m.add_edge('33_interact', '33i', prob=1.0)

    m.add_edge('43_idle', '43', prob=1.0)
    m.add_edge('43_left', '33', prob=1.0)
    m.add_edge('43_interact', '43i', prob=1.0)

    m.add_edge('03i_interact', '03', prob=1.0)
    m.add_edge('13i_interact', '13', prob=1.0)
    m.add_edge('23i_interact', '23', prob=1.0)
    m.add_edge('33i_interact', '33', prob=1.0)
    m.add_edge('43i_interact', '43', prob=1.0)
    m.add_edge('24i_interact', '24', prob=1.0)

    is_valid(m)
    return m


