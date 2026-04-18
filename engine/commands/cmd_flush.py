from .shared import Result, no_job

def cmd_flush(args, state):
    if not state.active_job:
        return no_job()
    target = " ".join(args) if args else "unknown"
    return Result(f"Flushed {target}. Fresh fluid in. [dim](No notable findings.)[/]", time_cost=20)
