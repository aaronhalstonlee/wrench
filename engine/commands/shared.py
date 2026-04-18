from dataclasses import dataclass
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
}

POST_REPAIR_TEST_OVERRIDES = {
    # paste your dict here manually after generation
}

PART_COSTS = {
    # paste your dict here manually after generation
}

PART_TIMES = {
    # paste your dict here manually after generation
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
