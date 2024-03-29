from prism_bridge.prism_io import write_prism_model, write_prism_model_bounded


def has_winning_strategy(game, prism_handler):
    win_prop = '<< p1 >> Pmax=? [F \"accept\"]'
    prism_model, state_ids = write_prism_model(game, "strategy")
    prism_handler.load_model_file(prism_model)
    result = prism_handler.check_property(win_prop)
    init_id = state_ids[game.graph["init"]]
    return result[init_id] > 0.999


def has_coop_strategy(game, prism_handler):
    win_prop = '<< p1,p2 >> Pmax=? [F \"accept\"]'
    prism_model, state_ids = write_prism_model(game, "strategy")
    prism_handler.load_model_file(prism_model)
    result = prism_handler.check_property(win_prop)
    init_id = state_ids[game.graph["init"]]
    return result[init_id] > 0.999


def get_winning_strategy(game, prism_handler, test=False):
    win_prop = '<< p1 >> Pmax=? [F \"accept\"]'
    prism_model, state_ids = write_prism_model(game, "strategy")
    prism_handler.load_model_file(prism_model)
    prism_strat = prism_handler.synthesize_strategy(win_prop, test)
    id_strat = {}

    # gather all moves for the same state id
    for _, move in prism_strat.items():
        if move == "null" or move == "-":
            continue
        move_arr = move.split("_")
        if move_arr[0] != "p1":
            continue

        state_id = int(move_arr[1])
        strat_move = move_arr[2]
        id_strat[state_id] = strat_move

    # translate state_id to actual state
    strategy = {}
    for state, state_id in state_ids.items():
        if state_id in id_strat.keys():
            strategy[state] = id_strat[state_id]

    return strategy


def get_min_strategy_bounded(game, prism_handler, safety=None, fairness=None, test=False):
    if safety is None:
        safety = []
    if fairness is None:
        fairness = []
    win_prop = '<< p1 >> Rmin=? [F \"accept\"]'
    # TODO: better bounds?
    step_bound = game.number_of_nodes()
    # costs
    costs = {}
    for edge in safety:
        node_from = edge[0]
        if node_from not in costs.keys():
            costs[node_from] = 0
        costs[node_from] += 1
    for edge in fairness:
        node_from = edge[0]
        if node_from not in costs.keys():
            costs[node_from] = 0
        costs[node_from] += 1

    # prism translations
    prism_model, state_ids = write_prism_model_bounded(game, step_bound, costs, "min_bounded")
    prism_handler.load_model_file(prism_model)
    prism_strat = prism_handler.synthesize_strategy(win_prop, test)
    id_strat = {}

    # gather all moves for the same state id
    for _, move in prism_strat.items():
        if move == "null" or move == "-":
            continue
        move_arr = move.split("_")
        if move_arr[0] != "p1":
            continue

        state_id = int(move_arr[1])
        strat_move = move_arr[2]
        if state_id not in id_strat.keys():
            id_strat[state_id] = set()
        id_strat[state_id].add(strat_move)

    # translate state_id to actual state
    strategy = {}
    for state, state_id in state_ids.items():
        if state_id in id_strat.keys():
            strategy[state] = id_strat[state_id]

    for state, moves in strategy.items():
        if len(moves) > 1:
            moves.remove("stay")
        assert len(moves) == 1
        strategy[state] = list(moves)[0]
    return strategy
