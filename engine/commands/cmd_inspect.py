from .shared import Result, no_job, get_cmd_data, normalize_arg

def cmd_inspect(args, state):
    if not state.active_job:
        return no_job()
    target = normalize_arg(args[0]) if args else "engine_bay"
    text = get_cmd_data(state.active_job, "inspect", target)
    if not text:
        return Result(f"Nothing notable to inspect about '{' '.join(args)}'.", time_cost=2)
    return Result(text, time_cost=5)
