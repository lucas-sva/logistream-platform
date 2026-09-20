"""Load generated JSONL into the local PostgreSQL Bronze schema."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import psycopg2

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "data" / "output"

TABLES = {
    "orders": (
        "orders.jsonl",
        [
            "order_id",
            "order_item_id",
            "order_ts",
            "channel",
            "customer_id",
            "customer_email",
            "sku",
            "quantity",
            "unit_price",
            "discount_amount",
            "status",
            "processing_minutes",
            "destination_city",
            "destination_state",
            "destination_zip",
            "origin_cd",
        ],
    ),
    "logistics": (
        "logistics.jsonl",
        [
            "delivery_id",
            "order_id",
            "vehicle_id",
            "route_id",
            "origin_cd",
            "destination_city",
            "destination_state",
            "promised_hours",
            "actual_hours",
            "transport_cost",
            "distance_km",
            "weight_occupancy_pct",
            "volume_occupancy_pct",
            "departed_ts",
            "delivered_ts",
            "status",
            "occurrence_flag",
        ],
    ),
    "feedback": (
        "feedback.jsonl",
        [
            "feedback_id",
            "order_id",
            "customer_id",
            "submitted_ts",
            "product_score",
            "delivery_score",
            "nps_group",
            "comment",
            "contains_pii",
        ],
    ),
    "sensors": (
        "sensors.jsonl",
        [
            "event_id",
            "event_ts",
            "device_id",
            "device_type",
            "vehicle_id",
            "origin_cd",
            "metric",
            "lat",
            "lon",
            "speed_kmh",
            "temperature_c",
            "humidity_pct",
        ],
    ),
}


def connect():
    return psycopg2.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=os.environ.get("PGPORT", "5432"),
        user=os.environ.get("PGUSER", "logistream"),
        password=os.environ.get("PGPASSWORD", "logistream"),
        dbname=os.environ.get("PGDATABASE", "logistream"),
    )


def load_table(cur, table: str, filename: str, columns: list[str]) -> int:
    path = OUTPUT / filename
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            payload = json.loads(line)
            rows.append(tuple(payload.get(col) for col in columns))
    cur.execute(f"truncate table bronze.{table}")
    placeholders = ",".join(["%s"] * len(columns))
    col_sql = ",".join(columns)
    cur.executemany(
        f"insert into bronze.{table} ({col_sql}) values ({placeholders})",
        rows,
    )
    return len(rows)


def main() -> int:
    conn = connect()
    conn.autocommit = False
    cur = conn.cursor()
    total = {}
    for table, (filename, columns) in TABLES.items():
        total[table] = load_table(cur, table, filename, columns)
    conn.commit()
    cur.close()
    conn.close()
    print(json.dumps(total, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
