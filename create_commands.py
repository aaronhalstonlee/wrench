import os

# Folder where new command files will live
BASE = "engine/commands"

# Ensure directory exists
os.makedirs(BASE, exist_ok=True)

# Shared file content
shared_content = """from dataclasses import dataclass
from typing import Any
from engine.state import GameState, Job

@dataclass
class Result:
    text: str
    time_cost: int = 0
    finding: str | None = None

PART_ALIASES = {
    "injector_3": "fuel_injector_3",
    "fuel_injector_3": "fuel_injector_3",
    "injectors_all": "fuel_injectors_all",
    "fuel_injectors_all": "fuel_injectors_all",
    "all_injectors": "fuel_injectors_all",
    "oxygen_sensor": "oxygen_sensor_upstream",
    "o2_sensor": "oxygen_sensor_upstream",
    "upstream_o2": "oxygen_sensor_upstream",
    "oxygen_sensor_upstream": "oxygen_sensor_upstream",
    "fuel_pressure_regulator": "fuel_pressure_regulator",
    "battery": "battery",
    "spark_plugs": "spark_plugs",
    "spark_plug": "spark_plugs",
    "ckp":                        "crankshaft_position_sensor",
    "ckp_sensor":                 "crankshaft_position_sensor",
    "crank_sensor":               "crankshaft_position_sensor",
    "crankshaft_sensor":          "crankshaft_position_sensor",
    "crankshaft_position_sensor": "crankshaft_position_sensor",
    "idle_air_control":           "idle_air_control_valve",
    "iac":                        "idle_air_control_valve",
    "iac_valve":                  "idle_air_control_valve",
    "maf":                        "mass_airflow_sensor",
    "maf_sensor":                 "mass_airflow_sensor",
    "mass_airflow_sensor":        "mass_airflow_sensor",
    "fuel_pump":                  "fuel_pump",
    "throttle_body":              "throttle_body",
}

POST_REPAIR_TEST_OVERRIDES = {
    "fuel_injector_3": {
        "injector_balance": (
            "Running injector balance test...\n\n"
            "  Injector 1: -2.1%  [OK]\n"
            "  Injector 2: -1.8%  [OK]\n"
            "  Injector 3: -2.3%  [OK]  (repaired)\n"
            "  Injector 4: -1.5%  [OK]\n\n"
            "  All injectors within spec."
        ),
        "fuel_pressure": (
            "Running fuel pressure test...\n\n"
            "  Key-on pressure  : 49 psi   [OK] spec: 47-53 psi\n"
            "  Running pressure : 50 psi   [OK]\n"
            "  Key-off, 8hr sim : 47 psi   [OK] pressure holding\n\n"
            "  Fuel system holding pressure normally."
        ),
    },
    "fuel_injectors_all": {
        "injector_balance": (
            "Running injector balance test...\n\n"
            "  Injector 1: -1.9%  [OK]\n"
            "  Injector 2: -2.1%  [OK]\n"
            "  Injector 3: -2.0%  [OK]  (repaired)\n"
            "  Injector 4: -1.8%  [OK]\n\n"
            "  All injectors within spec."
        ),
        "fuel_pressure": (
            "Running fuel pressure test...\n\n"
            "  Key-on pressure  : 48 psi   [OK] spec: 47-53 psi\n"
            "  Key-off, 8hr sim : 46 psi   [OK] pressure holding\n\n"
            "  Fuel system holding pressure normally."
        ),
    },
    "crankshaft_position_sensor": {
        "ckp_sensor": (
            "Testing crankshaft position sensor resistance...\n\n"
            "  Cold resistance : 860 ohms  [OK]  spec: 750-900\n"
            "  Hot resistance  : 880 ohms  [OK]  spec: 750-900\n\n"
            "  New sensor holding spec at temperature. PCM\n"
            "  signal clean across the full heat range."
        ),
    },
}

PART_COSTS = {
    "crankshaft_position_sensor": 45,
    "idle_air_control_valve":     65,
    "mass_airflow_sensor":        120,
    "fuel_pump":                  280,
    "throttle_body":              210,
    "fuel_injector_3":          85,
    "fuel_injectors_all":       280,
    "oxygen_sensor_upstream":   45,
    "battery":                  120,
    "fuel_pressure_regulator":  65,
    "spark_plugs":              40,
}

PART_TIMES = {
    "fuel_injector_3":          60,
    "fuel_injectors_all":       90,
    "oxygen_sensor_upstream":   20,
    "battery":                  15,
    "fuel_pressure_regulator":  45,
    "spark_plugs":              30,
    "crankshaft_position_sensor": 25,
    "idle_air_control_valve":     30,
    "mass_airflow_sensor":        20,
    "fuel_pump":                  90,
    "throttle_body":              60,
}

def no_job() -> Result:
    return Result("No active job. Type [bold]job[/bold] to see your queue.")

def get_cmd_data(job: Job, *keys: str) -> Any:
    node = job.raw.get("commands", {})
    for k in keys:
        if not isinstance(node, dict):
            return None
        node = node.get(k)
    return node

def normalize_arg(arg: str) -> str:
    return arg.replace("-", "_").lower()
"""

# Write shared.py
with open(os.path.join(BASE, "shared.py"), "w", encoding="utf-8") as f:
    f.write(shared_content)

# Command file templates
commands = {
    "cmd_inspect.py": """from .shared import Result, no_job, get_cmd_data, normalize_arg

def cmd_inspect(args, state):
    if not state.active_job:
        return no_job()
    target = normalize_arg(args[0]) if args else "engine_bay"
    text = get_cmd_data(state.active_job, "inspect", target)
    if not text:
        return Result(f"Nothing notable to inspect about '{' '.join(args)}'.", time_cost=2)
    return Result(text, time_cost=5)
""",

    "cmd_listen.py": """from .shared import Result, no_job, get_cmd_data, normalize_arg

def cmd_listen(args, state):
    if not state.active_job:
        return no_job()
    target = normalize_arg(args[0]) if args else "idle"
    text = get_cmd_data(state.active_job, "listen", target)
    if not text:
        return Result(f"Nothing notable when listening to '{' '.join(args)}'.", time_cost=2)
    return Result(text, time_cost=5)
""",

    "cmd_smell.py": """from .shared import Result, no_job, get_cmd_data, normalize_arg

def cmd_smell(args, state):
    if not state.active_job:
        return no_job()
    target = normalize_arg(args[0]) if args else "engine_bay"
    text = get_cmd_data(state.active_job, "smell", target)
    if not text:
        return Result(f"Nothing notable smelling '{' '.join(args)}'.", time_cost=1)
    return Result(text, time_cost=2)
""",

    "cmd_check.py": """from .shared import Result, no_job, get_cmd_data, normalize_arg

def cmd_check(args, state):
    if not state.active_job:
        return no_job()
    target = normalize_arg(args[0]) if args else "fluids"
    text = get_cmd_data(state.active_job, "check", target)
    if not text:
        return Result(f"Nothing to check for '{' '.join(args)}'.", time_cost=3)
    return Result(text, time_cost=8)
""",

    "cmd_scan.py": """from .shared import Result, no_job, get_cmd_data, normalize_arg

def cmd_scan(args, state):
    if not state.active_job:
        return no_job()
    target = normalize_arg(args[0]) if args else "obd2"
    text = get_cmd_data(state.active_job, "scan", target)
    if not text:
        return Result(f"Can't scan '{' '.join(args)}'.", time_cost=2)
    return Result(text, time_cost=10)
""",

    "cmd_test.py": """from .shared import Result, no_job, get_cmd_data, normalize_arg, POST_REPAIR_TEST_OVERRIDES

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
            f"Don't know how to test '{' '.join(args)}'.\\n"
            f"Try: fuel-pressure, compression, injector-balance"
        )

    finding_key = None
    if "FINDING LOGGED:" in text:
        parts = text.split("FINDING LOGGED:", 1)
        finding_key = parts[1].split("\\n")[0].strip()
        text = text.replace(f"FINDING LOGGED: {finding_key}\\n\\n", "")
        job.findings[finding_key] = True

    job.tests_run.append(target)
    return Result(text, time_cost=15, finding=finding_key)
""",

    "cmd_scope.py": """from .shared import Result, no_job, get_cmd_data, normalize_arg

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
""",

    "cmd_call.py": """from .shared import Result, no_job

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
""",

    "cmd_manual.py": """from .shared import Result, no_job, get_cmd_data, normalize_arg

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
""",

    "cmd_tsb.py": """from .shared import Result, no_job, get_cmd_data, normalize_arg

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
""",

    "cmd_forums.py": """from .shared import Result, no_job, get_cmd_data, normalize_arg

def cmd_forums(args, state):
    if not state.active_job:
        return no_job()
    if not args:
        return Result("Usage: forums <query>  (e.g. forums hard-start-accord)")
    target = normalize_arg("_".join(args))
    text = get_cmd_data(state.active_job, "forums", target)
    if not text:
        return Result(
            f"Search: '{' '.join(args)}'\\n\\n"
            "  No relevant threads found. Try different search terms.",
            time_cost=5,
        )
    return Result(text, time_cost=5)
""",

    "cmd_replace.py": """from .shared import (
    Result, no_job, normalize_arg,
    PART_ALIASES, PART_COSTS, PART_TIMES
)

def cmd_replace(args, state):
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
            f"Don't recognize part '{' '.join(args)}'.\\n"
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
            f"[green]✓[/] Replaced {part_display}. Part cost: ${cost}.\\n\\n"
            f"  Type [bold]done[/bold] when you're satisfied with the repair.",
            time_cost=time_cost,
        )
    elif part in wrong:
        state.parts_cannon_total += 1
        return Result(
            f"[yellow]~[/] Replaced {part_display}. Part cost: ${cost}.\\n\\n"
            f"  The part is in. But something feels off — the root symptom doesn't seem addressed.",
            time_cost=time_cost,
        )
    else:
        return Result(
            f"Replaced {part_display}. Part cost: ${cost}.",
            time_cost=time_cost,
        )
""",

    "cmd_flush.py": """from .shared import Result, no_job

def cmd_flush(args, state):
    if not state.active_job:
        return no_job()
    target = " ".join(args) if args else "unknown"
    return Result(f"Flushed {target}. Fresh fluid in. [dim](No notable findings.)[/]", time_cost=20)
""",

    "cmd_done.py": """from .shared import Result, no_job

def cmd_done(args, state):
    if not state.active_job:
        return no_job()

    job = state.active_job
    solution = job.solution
    required_repair = solution["required_repair"]
    acceptable = solution.get("acceptable_repairs", [])
    wrong = solution.get("wrong_repairs", [])
    required_findings = solution.get("required_findings", [])

    parts = job.parts_replaced
    correct_repair_done = required_repair in parts or any(p in acceptable for p in parts)
    wrong_repairs_done = [p for p in parts if p in wrong]
    findings_met = all(f in job.findings for f in required_findings)

    lines = []

    if correct_repair_done and findings_met:
        bonus = 50 if not wrong_repairs_done else 0
        payout = job.payout + bonus
        rep_delta = +8 if not wrong_repairs_done else +4
        state.money += payout
        state.reputation = min(100, state.reputation + rep_delta)
        state.completed_jobs.append(job.id)
        state.active_job = None

        lines.append("[green bold]✓ JOB COMPLETE[/]\\n")
        lines.append("  Root cause correctly identified and repaired.")
        if wrong_repairs_done:
            lines.append(f"  [yellow]Note: {len(wrong_repairs_done)} unnecessary part(s) replaced.[/]")
        else:
            lines.append(f"  [green]+${bonus} accuracy bonus — clean diagnosis.[/]")
        lines.append(f"\\n  Payout: [green]+${payout}[/]  |  Rep: [green]+{rep_delta}[/]")

    elif correct_repair_done and not findings_met:
        payout = job.payout
        state.money += payout
        state.reputation = min(100, state.reputation + 3)
        state.completed_jobs.append(job.id)
        state.active_job = None

        lines.append("[yellow]~ JOB CLOSED[/]\\n")
        lines.append("  The repair seems to have worked, but your diagnostic trail")
        lines.append("  was incomplete. Customer is happy for now.")
        lines.append(f"\\n  Payout: [green]+${payout}[/]  |  Rep: [yellow]+3[/]")

    elif not correct_repair_done and parts:
        rep_delta = -10
        state.reputation = max(0, state.reputation + rep_delta)

        lines.append("[red]✗ COMEBACK LIKELY[/]\\n")
        lines.append("  None of the repairs addressed the root cause.")
        lines.append("  The customer will be back. That's going to hurt your reputation.")
        lines.append(f"\\n  Payout: [red]$0[/]  |  Rep: [red]{rep_delta}[/]")
        lines.append("\\n  [dim]Hint: Keep diagnosing. The root cause hasn't been found yet.[/]")

    else:
        lines.append("[dim]Nothing repaired yet. Keep diagnosing before closing the job.[/]")

    return Result("\\n".join(lines), time_cost=5)
""",

    "cmd_job.py": """from .shared import Result

def cmd_job(args, state):
    return Result("__SHOW_JOB_TICKET__")
""",

    "cmd_status.py": """from .shared import Result

def cmd_status(args, state):
    return Result("__SHOW_STATUS__")
""",

    "cmd_help.py": """from .shared import Result

def cmd_help(args, state):
    return Result("__SHOW_HELP__")
""",

    "cmd_findings.py": """from .shared import Result, no_job

def cmd_findings(args, state):
    if not state.active_job:
        return no_job()
    return Result("__SHOW_FINDINGS__")
""",
}

# Write each command file
for filename, content in commands.items():
    with open(os.path.join(BASE, filename), "w", encoding="utf-8") as f:
        f.write(content)

# Generate __init__.py
init_lines = [f"from .{name[:-3]} import {name[:-3]}" for name in commands]
with open(os.path.join(BASE, "__init__.py"), "w", encoding="utf-8") as f:
    f.write("\n".join(init_lines))

print("Command folder generated successfully!")
