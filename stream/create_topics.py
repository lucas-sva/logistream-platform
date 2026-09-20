"""Create Kafka topics for the local demo."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from topics import TOPICS


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap", default="localhost:9092")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        for topic in TOPICS:
            print(topic["name"])
        return 0

    from kafka.admin import KafkaAdminClient, NewTopic

    admin = KafkaAdminClient(bootstrap_servers=args.bootstrap, client_id="logistream-admin")
    new_topics = [
        NewTopic(name=t["name"], num_partitions=t["partitions"], replication_factor=1)
        for t in TOPICS
    ]
    try:
        admin.create_topics(new_topics=new_topics, validate_only=False)
    except Exception as exc:
        print(exc)
    finally:
        admin.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
