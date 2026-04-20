from .shared import (
    Result, no_job, normalize_arg,
    PART_ALIASES, PART_COSTS, PART_TIMES
)

def cmd_replace(args, state):
    print("loaded parts aliases:", PART_ALIASES)
    if not state.active_job:
        return no_job()
    if not args:
        return Result("Usage: replace <part>  (e.g. replace injector-3, replace oxygen-sensor)")

    raw_part = normalize_arg("_".join(args))
    part = PART_ALIASES.get(raw_part)

    if not part:
        for alias, canonical in PART_ALIASES.items():
            if raw_part in alias or alias in raw_part:
                part = canonical
                break

    if not part:
        return Result(
            f"Don't recognize part '{' '.join(args)}'.\n"
            f"Try: injector-3, fuel-injectors-all, oxygen-sensor, battery, spark-plugs"
        )

    job = state.active_job
    cost = PART_COSTS.get(part, 50)
    time_cost = PART_TIMES.get(part, 30)

    if state.money < cost:
        return Result(f"Not enough money. Part costs ${cost}, you have ${state.money}.")

    state.money -= cost
    job.parts_replaced.append(part)

    solution = job.solution
    wrong = solution.get("wrong_repairs", [])
    acceptable = solution.get("acceptable_repairs", [])
    correct = solution.get("required_repair", "")
    part_display = part.replace("_", " ")

    if part == correct or part in acceptable:
        return Result(
            f"[green]✓[/] Replaced {part_display}. Part cost: ${cost}.\n\n"
            f"  Type [bold]done[/bold] when you're satisfied with the repair.",
            time_cost=time_cost,
        )
    elif part in wrong:
        state.parts_cannon_total += 1
        return Result(
            f"[yellow]~[/] Replaced {part_display}. Part cost: ${cost}.\n\n"
            f"  The part is in. But something feels off — the root symptom doesn't seem addressed.",
            time_cost=time_cost,
        )
    else:
        return Result(
            f"Replaced {part_display}. Part cost: ${cost}.",
            time_cost=time_cost,
        )
