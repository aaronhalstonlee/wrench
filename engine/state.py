from dataclasses import dataclass, field
from typing import Any


@dataclass
class Job:
    id: str
    vehicle: dict
    customer: dict
    payout: int
    time_limit: int
    fault_tree: dict
    red_herrings: list
    solution: dict
    raw: dict  # full yaml data

    # what the player has discovered this session
    tests_run: list[str] = field(default_factory=list)
    parts_replaced: list[str] = field(default_factory=list)
    findings: dict[str, Any] = field(default_factory=dict)


@dataclass
class GameState:
    money: int = 500
    reputation: int = 50        # 0–100
    time_minutes: int = 480     # 8:00am in minutes from midnight
    active_job: Job | None = None
    job_queue: list[Job] = field(default_factory=list)
    completed_jobs: list[str] = field(default_factory=list)
    parts_cannon_total: int = 0

    def clock_str(self) -> str:
        h = (self.time_minutes // 60) % 24
        m = self.time_minutes % 60
        period = "am" if h < 12 else "pm"
        h12 = h % 12 or 12
        return f"{h12}:{m:02d}{period}"
