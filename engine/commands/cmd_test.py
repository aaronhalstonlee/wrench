from .shared import Result, no_job, get_cmd_data, normalize_arg, POST_REPAIR_TEST_OVERRIDES

def cmd_test(args, state):
    if not state.active_job:
        return no_job()
    if not args:
        return Result("Usage: test <what>  (e.g. test fuel-pressure, test compression)")

    target = normalize_arg("_".join(args))
    job = state.active_job

    for part in job.parts_replaced:
        overrides = POST_REPAIR_TEST_OVERRIDES.get(part, {})
        if target in overrides:
            return Result(overrides[target], time_cost=15)

    text = get_cmd_data(job, "test", target)
    if not text:
        return Result(
            f"Don't know how to test '{' '.join(args)}'.\n"
            f"Try: fuel-pressure, compression, injector-balance"
        )

    finding_key = None
    if "FINDING LOGGED:" in text:
        parts = text.split("FINDING LOGGED:", 1)
        finding_key = parts[1].split("\n")[0].strip()
        text = text.replace(f"FINDING LOGGED: {finding_key}\n\n", "")
        job.findings[finding_key] = True

    job.tests_run.append(target)
    return Result(text, time_cost=15, finding=finding_key)
