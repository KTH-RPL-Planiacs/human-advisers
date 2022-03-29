import networkx as nx
from itertools import chain, combinations
from copy import deepcopy


def create_guard(opt, ap):
    guard = ''
    for e in ap:
        if e in opt:
            guard += '1'
        else:
            guard += '0'
    return guard


def sog_fits_to_guard(guard, sog, guard_ap, sog_ap):
    guards = deepcopy(sog)

    # check if this guard fits to one of the guards
    for i, g_value in enumerate(guard):
        if g_value == 'X':
            continue
        if guard_ap[i] in sog_ap:
            j = sog_ap.index(guard_ap[i])
            wrong_guards = []
            for guard in guards:
                if guard[j] != 'X' and guard[j] != g_value:
                    # if a synth guard is not matching to the current config, mark for removal
                    wrong_guards.append(guard)
            # remove marked guards
            for wg in wrong_guards:
                guards.remove(wg)

    return guards


# list(powerset([1,2,3])) --> [(), (1,), (2,), (3,), (1,2), (1,3), (2,3), (1,2,3)]
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


# group_and_flip({'a':[1,2], 'b':[2,1], 'c':[1,3,5]}) --> {{frozenset({1, 2}): ['a', 'b'], frozenset({1, 3, 5}): ['c']}}
def group_and_flip(d):
    grouped_dict = {}
    for k, v in d.items():
        hashable_v = frozenset(v)
        if hashable_v not in grouped_dict:
            grouped_dict[hashable_v] = [k]
        else:
            grouped_dict[hashable_v].append(k)
    return grouped_dict


def prune_unreachable_states(game):
    reach = nx.single_source_shortest_path_length(game, source=game.graph['init'])
    # identify unreachable states
    unreachable_nodes = []
    for node in game.nodes:
        if node not in reach.keys():
            unreachable_nodes.append(node)
    # remove unreachable states
    for urn in unreachable_nodes:
        game.remove_node(urn)
        # remove unreachable accepting state from accepting state list
        if urn in game.graph['acc']:
            game.graph['acc'].remove(urn)


def remove_edges(game, edges):
    for edge in edges:
        game.remove_edge(*edge)
