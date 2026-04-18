from .shared import Result, no_job, get_cmd_data, normalize_arg

def cmd_forums(args, state):
    if not state.active_job:
        return no_job()
    if not args:
        return Result("Usage: forums <query>  (e.g. forums hard-start-accord)")
    target = normalize_arg("_".join(args))
    text = get_cmd_data(state.active_job, "forums", target)
    if not text:
        return Result(
            f"Search: '{' '.join(args)}'\n\n"
            "  No relevant threads found. Try different search terms.",
            time_cost=5,
        )
    return Result(text, time_cost=5)
