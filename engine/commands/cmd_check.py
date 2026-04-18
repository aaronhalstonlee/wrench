from .shared import Result, no_job, get_cmd_data, normalize_arg

def cmd_check(args, state):
    if not state.active_job:
        return no_job()
    target = normalize_arg(args[0]) if args else "fluids"
    text = get_cmd_data(state.active_job, "check", target)
    if not text:
        return Result(f"Nothing to check for '{' '.join(args)}'.", time_cost=3)
    return Result(text, time_cost=8)
