import networkx as nx
import re


class MonaFormatError(Exception):
    """Custom Error that is thrown when the provided string does not match MONA output"""
    pass


def get_value(text, regex, value_type=str):
    """Searches the provided text for values matching the provided regular expression and returns matches
    :param text: provided string to be searched
    :param regex: regular expression used for matching
    :param value_type: desired type of the return value
    :return: matches in text from the regex
    """

    pattern = re.compile(regex, re.MULTILINE)
    results = pattern.search(text)
    if results:
        return value_type(results.group(1))
    else:
        print("Could not find the value {}, in the text provided".format(regex))
        return value_type(0.0)


def to_nxgraph(mona_output, name="MONA_DFA"):
    """
    Creates a networkx.DiGraph from a MONA string
    :param mona_output: the MONA output
    :param name: a desired name for the DiGraph, "MONA_DFA" by default
    :return: the DFA as a networkx.DiGraph
    """
    dfa = nx.DiGraph()
    dfa.graph["name"] = name

    # if formula is unsatisfiable
    if "Formula is unsatisfiable" in mona_output:
        raise MonaFormatError("Formula is unsatisfiable, DFA not constructed!")

    if "DFA for formula with free variables:" not in mona_output:
        raise MonaFormatError("Input is no valid MONA output!")

    # atomic propositions
    variables = get_value(mona_output, r'.*DFA for formula with free variables:[\s]*(.*?)\n.*', str)
    dfa.graph['ap'] = variables.lower().split()

    # accepting states
    accepting_states = get_value(mona_output, r".*Accepting states:[\s]*(.*?)\n.*", str)
    accepting_states = [
        str(x.strip()) for x in accepting_states.split() if len(x.strip()) > 0
    ]

    dfa.graph['acc'] = accepting_states

    # transitions and states
    for line in mona_output.splitlines():
        if line.startswith("State "):

            orig_state = get_value(line, r".*State[\s]*(\d+):\s.*", str)
            dest_state = get_value(line, r".*state[\s]*(\d+)[\s]*.*", str)
            guard = get_value(line, r".*:[\s](.*?)[\s]->.*", str)
            if dfa.has_edge(orig_state, dest_state):
                dfa.edges[orig_state, dest_state]['guard'].append(guard)
            else:
                dfa.add_edge(orig_state, dest_state, guard=[guard])

    # remove the don't care state 0
    assert dfa.has_edge('0', '1')
    assert len(list(dfa.successors('0'))) == 1
    assert len(dfa.edges['0', '1']['guard']) == 1
    assert all(c == 'X' for c in dfa.edges['0', '1']['guard'][0])
    dfa.remove_node('0')

    # initial state
    dfa.graph['init'] = '1'

    return dfa


if __name__ == "__main__":
    from parse_ltlf import to_mona
    mona = to_mona("G a && F b")
    print(mona)
    dfa = to_nxgraph(mona)
    print(dfa.edges(data=True))