from .shared import Result, no_job, get_cmd_data, normalize_arg

def cmd_listen(args, state):
    if not state.active_job:
        return no_job()
    target = normalize_arg(args[0]) if args else "idle"
    text = get_cmd_data(state.active_job, "listen", target)
    if not text:
        return Result(f"Nothing notable when listening to '{' '.join(args)}'.", time_cost=2)
    return Result(text, time_cost=5)
