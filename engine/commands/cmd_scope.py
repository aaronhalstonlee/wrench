from .shared import Result, no_job, get_cmd_data, normalize_arg

def cmd_scope(args, state):
    if not state.active_job:
        return no_job()
    if not args:
        return Result("Usage: scope <component>  (e.g. scope injector-3, scope oxygen-sensor)")
    target = normalize_arg("_".join(args))
    text = get_cmd_data(state.active_job, "scope", target)
    if not text:
        return Result(f"No scope data available for '{' '.join(args)}'.", time_cost=5)
    return Result(text, time_cost=20)
