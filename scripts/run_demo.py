"""Run the local demo path: generate data, land Bronze, load Postgres."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> None:
    print("+", " ".join(args))
    subprocess.check_call(args, cwd=ROOT)


def main() -> int:
    py = sys.executable
    run([py, "data/generator/generate.py"])
    run([py, "data/generator/validate.py"])
    run([py, "ingest/local/load_bronze.py"])
    if "--postgres" in sys.argv:
        run([py, "ingest/local/load_postgres.py"])
    if "--dry-run-stream" in sys.argv:
        run([py, "stream/create_topics.py", "--dry-run"])
        run([py, "stream/sensor_producer.py", "--dry-run"])
    print("demo local concluida")
    return 0


if __name__ == "__main__":
    sys.exit(main())
