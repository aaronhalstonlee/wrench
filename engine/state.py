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
    
    def to_dict(self):
        return {
            "id": self.id,
            "vehicle": self.vehicle,
            "customer": self.customer,
            "payout": self.payout,
            "time_limit": self.time_limit,
            "fault_tree": self.fault_tree,
            "red_herrings": self.red_herrings,
            "raw": self.raw,
            "solution": self.solution,
            "parts_replaced": self.parts_replaced,
            "findings": self.findings,
            "tests_run": self.tests_run,
        }
    
    @classmethod
    def from_dict(cls, data):
        job = cls(
            id=data["id"],
            vehicle=data["vehicle"],
            customer=data["customer"],
            payout=data["payout"],
            time_limit=data["time_limit"],
            fault_tree=data["fault_tree"],
            red_herrings=data["red_herrings"],
            raw=data["raw"],
            solution=data["solution"],
        )
        job.parts_replaced = data["parts_replaced"]
        job.findings = data["findings"]
        job.tests_run = data["tests_run"]
        
        return job


@dataclass
class GameState:
    money: int = 500
    reputation: int = 50        # 0–100
    time: int = 480     # 8:00am in minutes from midnight
    active_job: Job | None = None
    job_queue: list[Job] = field(default_factory=list)
    completed_jobs: list[str] = field(default_factory=list)
    parts_cannon_total: int = 0

    def clock_str(self) -> str:
        h = (self.time // 60) % 24
        m = self.time % 60
        period = "am" if h < 12 else "pm"
        h12 = h % 12 or 12
        return f"{h12}:{m:02d}{period}"
    
    def to_dict(self):
        return {
            "money": self.money,
            "reputation": self.reputation,
            "time": self.time,
            "active_job": self.active_job.to_dict() if self.active_job else None,
            "job_queue": [job.to_dict() for job in self.job_queue],
            "completed_jobs": self.completed_jobs,
            "parts_cannon_total": self.parts_cannon_total,
        }
        
    @classmethod
    def from_dict(cls, data):
        state = cls()
        state.money = data["money"]
        state.reputation = data["reputation"]
        state.time = data["time"]
        state.completed_jobs = data["completed_jobs"]
        state.parts_cannon_total = data["parts_cannon_total"]
        
        #rebuild jobs
        from engine.state import Job
        state.job_queue = [Job.from_dict(j) for j in data["job_queue"]]
        state.active_job = Job.from_dict(data["active_job"]) if data["active_job"] else None
        
        return state
