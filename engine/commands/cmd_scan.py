from .shared import Result, no_job, get_cmd_data, normalize_arg

def cmd_scan(args, state):
    if not state.active_job:
        return no_job()
    target = normalize_arg(args[0]) if args else "obd2"
    text = get_cmd_data(state.active_job, "scan", target)
    if not text:
        return Result(f"Can't scan '{' '.join(args)}'.", time_cost=2)
    return Result(text, time_cost=10)
