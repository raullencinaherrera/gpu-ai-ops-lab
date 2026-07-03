import time
import yaml
from pathlib import Path
from simulator.state import save_state
from simulator.event_sender import send_event


def run_scenario(path: str, delay: int = 3) -> None:
    scenario = yaml.safe_load(Path(path).read_text())

    for index, step in enumerate(scenario["steps"], start=1):
        state = {
            "scenario": scenario["name"],
            "description": scenario["description"],
            "severity": scenario["severity"],
            "node": scenario["node"],
            "gpu": scenario["gpu"],
            "step": index,
            "metrics": step,
            "expected_decision": scenario.get("expected_decision")
        }

        save_state(state)

        event = {
            "source": "gpu-ai-ops-lab",
            "event_type": "gpu_incident",
            "scenario": scenario["name"],
            "severity": scenario["severity"],
            "node": scenario["node"],
            "gpu": scenario["gpu"],
            "message": f"{scenario['name']} detected on {scenario['node']} {scenario['gpu']}",
            "metrics": step,
            "labels": {
                "platform": "nvidia",
                "environment": "lab",
                "cluster": "dgx-lab-01"
            }
        }

        send_event(event)
        print(event)
        time.sleep(delay)
