import shlex
from typing import Tuple, List, Callable, Dict

from engine.commands import (
    cmd_inspect, cmd_listen, cmd_smell, cmd_check,
    cmd_scan, cmd_test, cmd_scope, cmd_call,
    cmd_manual, cmd_tsb, cmd_forums,
    cmd_replace, cmd_flush,
    cmd_done, cmd_job, cmd_status, cmd_help, cmd_findings,
    cmd_save, cmd_load,
)

# Primary command -> handler
COMMANDS: Dict[str, Callable] = {
    "inspect":  cmd_inspect,
    "listen":   cmd_listen,
    "smell":    cmd_smell,
    "check":    cmd_check,
    "scan":     cmd_scan,
    "test":     cmd_test,
    "scope":    cmd_scope,
    "call":     cmd_call,
    "manual":   cmd_manual,
    "tsb":      cmd_tsb,
    "forums":   cmd_forums,
    "replace":  cmd_replace,
    "flush":    cmd_flush,
    "done":     cmd_done,
    "job":      cmd_job,
    "status":   cmd_status,
    "help":     cmd_help,
    "findings": cmd_findings,
    "save": cmd_save,
    "load": cmd_load,
}

# Centralized alias mapping (alias -> canonical)
ALIASES: Dict[str, str] = {
    "look": "inspect",
    "sniff": "smell",
    # add more aliases here
}

# Build a lookup that resolves aliases to handlers
def _build_lookup(commands: Dict[str, Callable], aliases: Dict[str, str]) -> Dict[str, Callable]:
    lookup = dict(commands)
    for alias, target in aliases.items():
        if target in commands:
            lookup[alias] = commands[target]
    return lookup

LOOKUP = _build_lookup(COMMANDS, ALIASES)

def parse(raw: str) -> Tuple[str, List[str]]:
    """
    Parse a raw command line into (verb, args).
    Supports quoted arguments and escaping via shlex.
    Returns empty verb for blank input.
    """
    raw = (raw or "").strip()
    if not raw:
        return "", []

    try:
        tokens = shlex.split(raw)
    except ValueError:
        # fallback to simple split if quotes are malformed
        tokens = raw.split()

    verb = tokens[0].lower()
    args = [t for t in tokens[1:]]
    return verb, args

def get_handler(verb: str):
    """Return the handler callable for a verb or None if unknown."""
    if not verb:
        return None
    return LOOKUP.get(verb.lower())

def list_commands() -> List[str]:
    """Return sorted list of available verbs (including aliases)."""
    return sorted(LOOKUP.keys())
