import yaml
from pathlib import Path
from engine.state import Job

CASES_DIR = Path(__file__).resolve().parent.parent / "data" / "cases"


def load_case(case_id: str) -> Job:
    path = CASES_DIR / f"{case_id}.yaml"
    with open(path) as f:
        raw = yaml.safe_load(f)

    return Job(
        id=raw["id"],
        vehicle=raw["vehicle"],
        customer=raw["customer"],
        payout=raw["payout"],
        time_limit=raw["time_limit"],
        fault_tree=raw["fault_tree"],
        red_herrings=raw.get("red_herrings", []),
        solution=raw["solution"],
        raw=raw,
    )


def load_all_cases() -> list[Job]:
    cases = []
    for path in sorted(CASES_DIR.glob("case_*.yaml")):
        cases.append(load_case(path.stem))
    return cases