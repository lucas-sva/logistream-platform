"""Publish synthetic sensor events to Kafka using the source contract."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from topics import TOPICS

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SRC = ROOT / "data" / "output" / "sensors.jsonl"


def topic_for(device_type: str) -> str:
    for item in TOPICS:
        if item["filter"] == device_type:
            return item["name"]
    raise KeyError(device_type)


def main() -> int:
    parser = argparse.ArgumentParser(description="Produce LogiStream sensor events.")
    parser.add_argument("--bootstrap", default="localhost:9092")
    parser.add_argument("--src", type=Path, default=DEFAULT_SRC)
    parser.add_argument("--sleep-ms", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.src.exists():
        print(f"missing {args.src}", file=sys.stderr)
        return 1

    producer = None
    if not args.dry_run:
        from kafka import KafkaProducer

        producer = KafkaProducer(
            bootstrap_servers=args.bootstrap,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda v: v.encode("utf-8") if v else None,
        )

    count = 0
    with args.src.open(encoding="utf-8") as handle:
        for line in handle:
            event = json.loads(line)
            topic = topic_for(event["device_type"])
            key = event.get("vehicle_id") or event.get("origin_cd") or event["device_id"]
            if args.dry_run:
                print(f"{topic} {key} {event['event_id']}")
            else:
                producer.send(topic, key=key, value=event)
            count += 1
            if args.sleep_ms:
                time.sleep(args.sleep_ms / 1000)

    if producer is not None:
        producer.flush()
    print(f"published {count} events")
    return 0


if __name__ == "__main__":
    sys.exit(main())
