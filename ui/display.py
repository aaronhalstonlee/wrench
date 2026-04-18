from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.rule import Rule
from rich import box
from engine.state import GameState, Job

console = Console()


def render_boot_screen():
    console.clear()
    console.print()
    console.print(Panel.fit(
        "[bold green]WRENCH[/] [dim]v0.1[/]\n"
        "[dim]Automotive Diagnostic Simulator[/]",
        border_style="green",
        padding=(1, 4),
    ))
    console.print()
    console.print("[dim]Type [bold]help[/bold] for a list of commands. Type [bold]quit[/bold] to exit.[/]")
    console.print()


def render_header(state: GameState):
    v = state.active_job.vehicle if state.active_job else None
    vehicle_str = (
        f"{v['year']} {v['make']} {v['model']}  [dim]{v['engine']}  {v['mileage']:,} mi[/]"
        if v else "[dim]No active job[/]"
    )

    rep_color = "green" if state.reputation >= 60 else "yellow" if state.reputation >= 35 else "red"

    header = (
        f"[bold]{state.clock_str()}[/]  "
        f"[green]${state.money}[/]  "
        f"Rep: [{rep_color}]{state.reputation}/100[/]"
        f"  |  {vehicle_str}"
    )
    console.rule(header, style="dim")


def render_job_ticket(job: Job):
    v = job["vehicle"] if isinstance(job, dict) else job.vehicle
    c = job["customer"] if isinstance(job, dict) else job.customer
    payout = job["payout"] if isinstance(job, dict) else job.payout

    # use the Job object
    if isinstance(job, Job):
        v = job.vehicle
        c = job.customer
        payout = job.payout

    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    table.add_column(style="dim", width=12)
    table.add_column()

    table.add_row("Vehicle", f"[bold]{v['year']} {v['make']} {v['model']}[/]  {v['engine']}")
    table.add_row("Mileage", f"{v['mileage']:,} mi")
    table.add_row("Customer", c["name"])
    table.add_row("Complaint", f"[italic]\"{c['complaint']}\"[/]")
    table.add_row("Payout", f"[green]${payout}[/]")

    console.print(Panel(table, title=f"[bold]JOB #{job.id.split('_')[1]}[/]", border_style="cyan"))


def render_result(text: str, time_cost: int = 0):
    if time_cost:
        console.print(f"[dim]  [+{time_cost} min][/]")
    console.print()
    # render line by line to support inline markup
    for line in text.split("\n"):
        console.print(f"  {line}")
    console.print()


def render_error(msg: str):
    console.print(f"\n  [red]✗[/]  {msg}\n")


def render_info(msg: str):
    console.print(f"\n  [cyan]→[/]  {msg}\n")


def render_help():
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column(style="bold cyan", width=28)
    table.add_column(style="dim")

    sections = [
        ("— OBSERVATION —", ""),
        ("inspect <target>", "Look at engine bay, undercar, etc."),
        ("listen <target>", "Listen to idle, cranking, etc."),
        ("smell <target>", "Smell exhaust, engine bay"),
        ("check <target>", "Check fluids, battery, spark plugs"),
        ("", ""),
        ("— DIAGNOSTICS —", ""),
        ("scan obd2", "Pull fault codes from ECU"),
        ("test <test>", "fuel-pressure, compression, injector-balance"),
        ("scope <target>", "Oscilloscope a component"),
        ("call customer", "Ask follow-up questions"),
        ("", ""),
        ("— RESEARCH —", ""),
        ("manual <system>", "Look up specs (fuel-system, ignition, etc.)"),
        ("tsb <symptom>", "Search technical service bulletins"),
        ("forums <query>", "Search online forums (caveat emptor)"),
        ("", ""),
        ("— REPAIR —", ""),
        ("replace <part>", "Replace a component"),
        ("flush <system>", "Flush a fluid system"),
        ("", ""),
        ("— SHOP —", ""),
        ("job", "Show current job ticket"),
        ("status", "Show your stats"),
        ("done", "Submit repair as complete"),
        ("quit", "Exit the game"),
    ]

    for cmd, desc in sections:
        if cmd.startswith("—"):
            table.add_row(f"[bold white]{cmd}[/]", "")
        else:
            table.add_row(cmd, desc)

    console.print(Panel(table, title="[bold]COMMANDS[/]", border_style="dim"))


def render_status(state: GameState):
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column(style="dim", width=18)
    table.add_column()

    rep_color = "green" if state.reputation >= 60 else "yellow" if state.reputation >= 35 else "red"

    table.add_row("Time", state.clock_str())
    table.add_row("Money", f"[green]${state.money}[/]")
    table.add_row("Reputation", f"[{rep_color}]{state.reputation}/100[/]")
    table.add_row("Jobs completed", str(len(state.completed_jobs)))
    if state.parts_cannon_total:
        table.add_row("Parts cannon", f"[red]{state.parts_cannon_total} unnecessary parts[/]")

    console.print(Panel(table, title="[bold]SHOP STATUS[/]", border_style="dim"))


def render_findings(job: Job):
    if not job.findings and not job.tests_run:
        render_info("No findings logged yet.")
        return
    console.print()
    console.print("  [bold]Findings so far:[/]")
    for key, val in job.findings.items():
        console.print(f"  [cyan]✓[/] {key}: {val}")
    console.print()
