from prism_bridge.prism_io import write_prism_model


def minimal_safety_edges(synth, prism_handler):
    safass_prop = '<< p1,p2 >> Pmax=? [F \"accept\"]'

    # PRISM translations
    prism_model, state_ids = write_prism_model(synth, "safety")
    prism_handler.load_model_file(prism_model)
    coop_reach = prism_handler.check_property(safass_prop)
    # create list of all doomed states that can never reach the accepting states
    doomed_states = []
    for state, state_id in state_ids.items():
        if coop_reach[state_id] < 1.0:
            doomed_states.append(state)

    safety_edges = []
    # search for all player 2 edges that could lead to a doomed state from a safe state
    for node, data in synth.nodes(data=True):
        if data['player'] != 2:
            continue
        if node in doomed_states:
            continue
        for succ in synth.successors(node):
            unsafe = any(elem in doomed_states for elem in synth.successors(succ))
            if unsafe:
                safety_edges.append((node, succ))

    return safety_edges
