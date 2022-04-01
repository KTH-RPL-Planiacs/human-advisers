from prism_bridge.prism_io import write_prism_model


def get_winning_strategy(game, prism_handler, test=False):
    # PRISM translations
    win_prop = '<< p1 >> Pmax=? [F \"accept\"]'
    prism_model, state_ids = write_prism_model(game, "safety")
    prism_handler.load_model_file(prism_model)
    prism_strat = prism_handler.synthesize_strategy(win_prop, test)
    strategy = {}
    for state, state_id in state_ids.items():
        if game.nodes[state]["player"] != 1:
            continue
        if str(state_id) not in prism_strat.keys():
            continue
        move = prism_strat[str(state_id)]
        if move == "null" or move == "-":
            continue
        strategy[state] = move.split("_")[2]

    return strategy
