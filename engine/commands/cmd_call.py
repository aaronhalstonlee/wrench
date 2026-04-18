from .shared import Result, no_job

def cmd_call(args, state):
    if not state.active_job:
        return no_job()
    job = state.active_job
    follow_ups = job.customer.get("follow_up", [])
    trigger = " ".join(["call"] + args).lower()

    for entry in follow_ups:
        if entry["trigger"].lower() in trigger or trigger in entry["trigger"].lower():
            return Result(entry["response"].strip(), time_cost=5)

    return Result(
        f"You call {job.customer['name']}. No answer — goes to voicemail. You leave a message.",
        time_cost=3,
    )
