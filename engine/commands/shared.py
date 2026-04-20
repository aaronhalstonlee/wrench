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
