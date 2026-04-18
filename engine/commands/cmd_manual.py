from .shared import Result, no_job, get_cmd_data, normalize_arg

def cmd_manual(args, state):
    if not state.active_job:
        return no_job()
    if not args:
        return Result("Usage: manual <section>  (e.g. manual fuel-system, manual ignition)")
    target = normalize_arg("_".join(args))
    text = get_cmd_data(state.active_job, "manual", target)
    if not text:
        return Result(f"No manual section found for '{' '.join(args)}'.", time_cost=2)
    return Result(text, time_cost=5)
