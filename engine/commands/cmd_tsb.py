from .shared import Result, no_job, get_cmd_data, normalize_arg

def cmd_tsb(args, state):
    if not state.active_job:
        return no_job()
    if not args:
        return Result("Usage: tsb <symptom>  (e.g. tsb hard-start)")
    target = normalize_arg("_".join(args))
    text = get_cmd_data(state.active_job, "tsb", target)
    if not text:
        return Result(f"No TSBs found matching '{' '.join(args)}'.", time_cost=5)
    return Result(text, time_cost=8)
