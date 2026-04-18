from .shared import Result, no_job

def cmd_findings(args, state):
    if not state.active_job:
        return no_job()
    return Result("__SHOW_FINDINGS__")
