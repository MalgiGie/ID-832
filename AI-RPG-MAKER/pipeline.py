import argparse
import subprocess
import time
import logging
import sys
import os
from pathlib import Path

from config import log_config_vars, LANGUAGE, ROOT_DIRECTORY

LOG_PATH = Path(__file__).parent / "pipeline.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

SCRIPTS = [
    "world.py",
    "npc.py",
    "hero.py",
    "missions.py",
    "epic-generator.py",
    "visualisator.py"
]

STEPS = [s.removesuffix(".py") for s in SCRIPTS]

def run_script(script_name: str) -> bool:
    script_path = Path(__file__).parent / script_name

    if not script_path.exists():
        logging.warning(f"Skipping {script_name} - file not found")
        return True

    start_time = time.time()

    try:
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True,
            env=os.environ
        )

        process.wait()
        elapsed = time.time() - start_time

        if process.returncode == 0:
            logging.info(f"Stage {script_name} completed ({elapsed:.2f}s)")
            return True
        else:
            logging.error(f"Stage {script_name} ended with error ({process.returncode}) ({elapsed:.2f}s)")
            return False

    except Exception as e:
        elapsed = time.time() - start_time
        logging.exception(f"Exception during running stage {script_name} after {elapsed:.2f}s: {e}")
        return False


def run_pipeline(selected_scripts=None):
    log_config_vars()
    logging.info(f"Selected language: {LANGUAGE}")
    total_start = time.time()

    stage_times = {}
    scripts_to_run = selected_scripts or SCRIPTS

    for script in scripts_to_run:
        stage_start = time.time()
        logging.info(f"Running stage: {script}")

        success = run_script(script)

        stage_elapsed = time.time() - stage_start
        stage_times[script] = stage_elapsed
        if not success:
            logging.warning(f"Pipeline disconnected after error inside {script}")
            break
        else:
            logging.info(f"Stage {script} ended successfully [{stage_elapsed:.2f}s]")

    total_elapsed = time.time() - total_start
    logging.info("\n Summary:")
    for name, secs in stage_times.items():
        logging.info(f"{name:<25} {secs:>6.2f}s")

    logging.info(f"\nTotal elapsed time: {total_elapsed:.2f}s")

def main():

    parser = argparse.ArgumentParser(
        description="Pipeline runner",
        epilog="Available steps:\n  " + "\n  ".join(STEPS)
    )

    parser.add_argument(
        "steps",
        nargs="*",
        choices=STEPS,
        help="Pipeline steps to run (default: all)"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List available pipeline steps"
    )

    args = parser.parse_args()

    if args.list:
        print("Available steps:")
        for step in STEPS:
            print(f"  - {step}")
        exit(0)

    selected = [f"{arg}.py" for arg in args] if args.steps else None

    print(f"Starting {ROOT_DIRECTORY}")

    if selected:
        logging.info(
            "Running selected pipeline: "
            + " → ".join(s.removesuffix(".py") for s in selected)
        )
    else:
        logging.info(
            "Running full pipeline: "
            + " → ".join(s.removesuffix(".py") for s in STEPS)
        )

    run_pipeline(selected)

if __name__ == "__main__":
    main()
