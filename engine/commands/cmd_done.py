from .shared import Result, no_job

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

        lines.append("[green bold]✓ JOB COMPLETE[/]\n")
        lines.append("  Root cause correctly identified and repaired.")
        if wrong_repairs_done:
            lines.append(f"  [yellow]Note: {len(wrong_repairs_done)} unnecessary part(s) replaced.[/]")
        else:
            lines.append(f"  [green]+${bonus} accuracy bonus — clean diagnosis.[/]")
        lines.append(f"\n  Payout: [green]+${payout}[/]  |  Rep: [green]+{rep_delta}[/]")

    elif correct_repair_done and not findings_met:
        payout = job.payout
        state.money += payout
        state.reputation = min(100, state.reputation + 3)
        state.completed_jobs.append(job.id)
        state.active_job = None

        lines.append("[yellow]~ JOB CLOSED[/]\n")
        lines.append("  The repair seems to have worked, but your diagnostic trail")
        lines.append("  was incomplete. Customer is happy for now.")
        lines.append(f"\n  Payout: [green]+${payout}[/]  |  Rep: [yellow]+3[/]")

    elif not correct_repair_done and parts:
        rep_delta = -10
        state.reputation = max(0, state.reputation + rep_delta)

        lines.append("[red]✗ COMEBACK LIKELY[/]\n")
        lines.append("  None of the repairs addressed the root cause.")
        lines.append("  The customer will be back. That's going to hurt your reputation.")
        lines.append(f"\n  Payout: [red]$0[/]  |  Rep: [red]{rep_delta}[/]")
        lines.append("\n  [dim]Hint: Keep diagnosing. The root cause hasn't been found yet.[/]")

    else:
        lines.append("[dim]Nothing repaired yet. Keep diagnosing before closing the job.[/]")

    return Result("\n".join(lines), time_cost=5)
