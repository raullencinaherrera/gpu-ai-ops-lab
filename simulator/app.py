import argparse
from simulator.scenario_runner import run_scenario


def main():
    parser = argparse.ArgumentParser(description="GPU AI Ops Lab Simulator")
    parser.add_argument(
        "--scenario",
        default="scenarios/overheating.yaml",
        help="Path to scenario YAML file"
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=3,
        help="Delay between scenario steps"
    )

    args = parser.parse_args()
    run_scenario(args.scenario, args.delay)


if __name__ == "__main__":
    main()
