import subprocess
import time
import logging
import sys
import os

from config import log_config_vars

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Lista plików do uruchomienia w kolejności
scripts = [
    "world.py",
    "npc-generator.py",
    "hero-generator.py",
    "quests-generator.py",
    "epic-generator.py",
    "visualisator.py"
]

def run_script(script_name):
    logging.info(f"🔹 Uruchamiam: {script_name}")
    start_time = time.time()

    try:
        result = subprocess.run(
            ["python3", script_name],
            capture_output=False,
            text=True,
            env=os.environ  # użycie ustawionych zmiennych środowiskowych
        )
        elapsed = time.time() - start_time

        if result.returncode == 0:
            logging.info(f"✅ {script_name} zakończony poprawnie w {elapsed:.2f}s")
        else:
            logging.error(f"❌ {script_name} zakończony z błędem ({result.returncode}) w {elapsed:.2f}s")
            logging.error(f"STDOUT:\n{result.stdout}")
            logging.error(f"STDERR:\n{result.stderr}")

        return result.returncode == 0

    except Exception as e:
        elapsed = time.time() - start_time
        logging.exception(f"❌ Wystąpił wyjątek przy uruchamianiu {script_name} po {elapsed:.2f}s: {e}")
        return False


def main():
    log_config_vars()
    total_start = time.time()
    for script in scripts:
        success = run_script(script)
        if not success:
            logging.warning(f"⚠️ Przerywam pipeline z powodu błędu w {script}")
            break
    total_elapsed = time.time() - total_start
    logging.info(f"⏱️ Całkowity czas wykonania pipeline: {total_elapsed:.2f}s")

if __name__ == "__main__":
    main()
