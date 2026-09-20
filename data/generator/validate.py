"""Validate generated JSONL files against the source contracts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "data" / "contracts"
OUTPUT = ROOT / "data" / "output"

MAPPING = {
    "orders.jsonl": "orders.schema.json",
    "logistics.jsonl": "logistics.schema.json",
    "feedback.jsonl": "feedback.schema.json",
    "sensors.jsonl": "sensors.schema.json",
}


def load_schema(name: str) -> Draft202012Validator:
    with (CONTRACTS / name).open(encoding="utf-8") as handle:
        return Draft202012Validator(json.load(handle))


def main() -> int:
    if not OUTPUT.exists():
        print("no output directory; run generate.py first", file=sys.stderr)
        return 1

    errors = 0
    for filename, schema_name in MAPPING.items():
        path = OUTPUT / filename
        validator = load_schema(schema_name)
        with path.open(encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                row = json.loads(line)
                for err in validator.iter_errors(row):
                    errors += 1
                    print(f"{filename}:{line_no} {err.message}")
                    if errors >= 20:
                        print("stopping after 20 errors")
                        return 1
    if errors:
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
