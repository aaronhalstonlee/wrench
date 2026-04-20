import sys
import os
from pathlib import Path
import traceback

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

from engine.state import GameState
from engine import parser, clock
from systems.loader import load_all_cases
from ui import display
from engine.constants import ResultAction

def _handle_action(result, state):
    """Return True to continue loop, False to break."""
    text = getattr(result, "text", None)
    time_cost = getattr(result, "time_cost", None)

    # Map special tokens to actions (support both strings and enums)
    if text in (ResultAction.SHOW_JOB_TICKET, "__SHOW_JOB_TICKET__"):
        if state.active_job:
            display.render_job_ticket(state.active_job)
        else:
            display.render_info("No active job.")
        return True

    if text in (ResultAction.SHOW_STATUS, "__SHOW_STATUS__"):
        display.render_status(state)
        return True

    if text in (ResultAction.SHOW_HELP, "__SHOW_HELP__"):
        display.render_help()
        return True

    if text in (ResultAction.SHOW_FINDINGS, "__SHOW_FINDINGS__"):
        if state.active_job:
            display.render_findings(state.active_job)
        else:
            display.render_info("No active job.")
        return True

    # Default: render result text
    display.render_result(text or "[dim]No output from command[/]", time_cost or 0)

    # Advance clock if time_cost is explicitly provided and > 0
    if time_cost is not None and time_cost > 0:
        try:
            clock.advance(state, time_cost)
        except Exception:
            display.render_error("Error advancing clock.")
            traceback.print_exc()

    return True

def main():
    state = GameState()
    cases = load_all_cases() or []
    state.job_queue.extend(cases)

    display.render_boot_screen()

    if state.job_queue:
        state.active_job = state.job_queue.pop(0)
        vehicle = state.active_job.vehicle
        display.render_info(
            f"New job assigned: [bold]{vehicle.get('year','?')} "
            f"{vehicle.get('make','?')} {vehicle.get('model','?')}[/]"
        )
        display.render_job_ticket(state.active_job)

    while True:
        display.render_header(state)
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            display.console.print("\n[dim]Locking up the shop...[/]")
            # optionally persist state here
            break

        if not raw:
            continue

        if raw.lower() in ("quit", "exit", "q"):
            display.console.print("[dim]Locking up the shop. See you tomorrow.[/]")
            # optionally persist state here
            break

        try:
            verb, args = parser.parse(raw)
        except Exception:
            display.render_error("Failed to parse command.")
            traceback.print_exc()
            continue

        handler = parser.COMMANDS.get(verb)
        if not handler:
            display.render_error(
                f"Unknown command: '[bold]{verb}[/]'  —  type [bold]help[/bold] to see available commands."
            )
            continue

        try:
            result = handler(args, state)
            
            if result.text == "__LOAD_STATE__":
                state = result.finding
                continue
        except Exception:
            display.render_error("Command raised an exception.")
            traceback.print_exc()
            continue

        # Validate result object shape
        if result is None:
            display.render_error("Command returned no result object.")
            continue

        try:
            _handle_action(result, state)
        except Exception:
            display.render_error("Error handling command result.")
            traceback.print_exc()
            continue

        # Job queue handling
        if state.active_job is None and state.job_queue:
            display.render_info("Next job is ready.")
            state.active_job = state.job_queue.pop(0)
            display.render_job_ticket(state.active_job)
        elif state.active_job is None and not state.job_queue:
            display.render_info("[green]All jobs complete for today![/] Final stats below.")
            display.render_status(state)
            break

if __name__ == "__main__":
    main()
