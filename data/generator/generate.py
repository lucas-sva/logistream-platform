"""Generate synthetic LogiStream source files that obey the JSON contracts."""

from __future__ import annotations

import argparse
import json
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reference import CDS, CHANNELS, CITIES, COMMENTS, PRODUCTS, VEHICLE_TYPES

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "data" / "contracts"
DEFAULT_OUT = ROOT / "data" / "output"


def _ts(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _event_id(rng: random.Random) -> str:
    return "EVT-" + "".join(rng.choice("0123456789ABCDEF") for _ in range(16))


def build_orders(rng: random.Random, days: int, orders_per_day: int) -> list[dict]:
    records: list[dict] = []
    start = datetime(2026, 8, 1, tzinfo=timezone.utc)
    item_seq = 1
    for day in range(days):
        for n in range(orders_per_day):
            cd = rng.choice(CDS)
            product = rng.choice(PRODUCTS)
            city, state, zip_code = rng.choice(CITIES)
            order_id = f"ORD-{(day * orders_per_day + n + 1):08d}"
            placed = start + timedelta(days=day, minutes=rng.randint(0, 24 * 60 - 1))
            qty = rng.choice([1, 1, 1, 2, 3])
            status = rng.choices(
                ["placed", "processed", "shipped", "cancelled"],
                weights=[8, 20, 65, 7],
            )[0]
            records.append(
                {
                    "order_id": order_id,
                    "order_item_id": f"ITM-{item_seq:010d}",
                    "order_ts": _ts(placed),
                    "channel": rng.choice(CHANNELS),
                    "customer_id": f"CUS-{rng.randint(1, 8000):08d}",
                    "customer_email": f"cliente{rng.randint(1, 8000)}@mail.example",
                    "sku": product["sku"],
                    "quantity": qty,
                    "unit_price": product["price"],
                    "discount_amount": round(product["price"] * qty * rng.choice([0, 0, 0, 0.05, 0.1]), 2),
                    "status": status,
                    "processing_minutes": rng.randint(12, 180),
                    "destination_city": city,
                    "destination_state": state,
                    "destination_zip": zip_code,
                    "origin_cd": cd["origin_cd"],
                }
            )
            item_seq += 1
    return records


def build_logistics(rng: random.Random, orders: list[dict]) -> list[dict]:
    records: list[dict] = []
    shipped = [o for o in orders if o["status"] in {"processed", "shipped"}]
    for i, order in enumerate(shipped, start=1):
        vehicle_kind = rng.choice(VEHICLE_TYPES)
        departed = datetime.fromisoformat(order["order_ts"].replace("Z", "+00:00")) + timedelta(
            minutes=order["processing_minutes"]
        )
        promised = rng.choice([24, 48, 72, 96])
        delay = rng.choices([0, 2, 6, 18, 30], weights=[55, 20, 12, 8, 5])[0]
        actual = promised + delay
        delivered = departed + timedelta(hours=actual)
        status = "delivered" if delay < 30 else rng.choice(["delivered", "failed"])
        records.append(
            {
                "delivery_id": f"DLV-{i:08d}",
                "order_id": order["order_id"],
                "vehicle_id": f"VEH-{vehicle_kind['prefix']}{rng.randint(0, 49):04d}",
                "route_id": f"RTE-{rng.randint(1, 120):06d}",
                "origin_cd": order["origin_cd"],
                "destination_city": order["destination_city"],
                "destination_state": order["destination_state"],
                "promised_hours": promised,
                "actual_hours": actual if status == "delivered" else None,
                "transport_cost": round(18 + actual * rng.uniform(0.8, 1.6), 2),
                "distance_km": round(rng.uniform(8, 420), 1),
                "weight_occupancy_pct": round(rng.uniform(35, 98), 1),
                "volume_occupancy_pct": round(rng.uniform(30, 95), 1),
                "departed_ts": _ts(departed),
                "delivered_ts": _ts(delivered) if status == "delivered" else None,
                "status": status,
                "occurrence_flag": delay >= 18 or status == "failed",
            }
        )
    return records


def build_feedback(rng: random.Random, orders: list[dict]) -> list[dict]:
    records: list[dict] = []
    candidates = [o for o in orders if o["status"] != "cancelled"]
    sample = rng.sample(candidates, k=max(1, len(candidates) // 3))
    for i, order in enumerate(sample, start=1):
        product_score = rng.choices([1, 2, 3, 4, 5], weights=[4, 6, 15, 35, 40])[0]
        delivery_score = rng.choices([1, 2, 3, 4, 5], weights=[8, 10, 18, 32, 32])[0]
        nps = "promoter" if delivery_score >= 5 else "passive" if delivery_score >= 4 else "detractor"
        submitted = datetime.fromisoformat(order["order_ts"].replace("Z", "+00:00")) + timedelta(
            days=rng.randint(2, 10)
        )
        records.append(
            {
                "feedback_id": f"FBK-{i:08d}",
                "order_id": order["order_id"],
                "customer_id": order["customer_id"],
                "submitted_ts": _ts(submitted),
                "product_score": product_score,
                "delivery_score": delivery_score,
                "nps_group": nps,
                "comment": rng.choice(COMMENTS),
                "contains_pii": False,
            }
        )
    return records


def build_sensors(rng: random.Random, logistics: list[dict], per_vehicle: int) -> list[dict]:
    records: list[dict] = []
    vehicles = sorted({row["vehicle_id"] for row in logistics})
    for vehicle_id in vehicles:
        cd = rng.choice(CDS)
        base_lat, base_lon = cd["lat"], cd["lon"]
        start = datetime(2026, 8, 20, 12, 0, tzinfo=timezone.utc)
        for i in range(per_vehicle):
            ts = start + timedelta(seconds=30 * i)
            records.append(
                {
                    "event_id": _event_id(rng),
                    "event_ts": _ts(ts),
                    "device_id": f"GPS-{vehicle_id}",
                    "device_type": "fleet_gps",
                    "vehicle_id": vehicle_id,
                    "origin_cd": None,
                    "metric": "gps",
                    "lat": round(base_lat + rng.uniform(-0.4, 0.4), 6),
                    "lon": round(base_lon + rng.uniform(-0.4, 0.4), 6),
                    "speed_kmh": round(rng.uniform(0, 92), 1),
                    "temperature_c": None,
                    "humidity_pct": None,
                }
            )
            if i % 2 == 0:
                records.append(
                    {
                        "event_id": _event_id(rng),
                        "event_ts": _ts(ts),
                        "device_id": f"ENV-{vehicle_id}",
                        "device_type": "fleet_environment",
                        "vehicle_id": vehicle_id,
                        "origin_cd": None,
                        "metric": "temperature",
                        "lat": None,
                        "lon": None,
                        "speed_kmh": None,
                        "temperature_c": round(rng.uniform(2.0, 8.5) if "3" in vehicle_id[4:5] else rng.uniform(18, 34), 1),
                        "humidity_pct": round(rng.uniform(35, 80), 1),
                    }
                )
    for cd in CDS:
        start = datetime(2026, 8, 20, 12, 0, tzinfo=timezone.utc)
        for i in range(20):
            ts = start + timedelta(minutes=i)
            records.append(
                {
                    "event_id": _event_id(rng),
                    "event_ts": _ts(ts),
                    "device_id": f"WH-{cd['origin_cd']}",
                    "device_type": "warehouse_environment",
                    "vehicle_id": None,
                    "origin_cd": cd["origin_cd"],
                    "metric": "temperature",
                    "lat": None,
                    "lon": None,
                    "speed_kmh": None,
                    "temperature_c": round(rng.uniform(3, 6) if cd["cold"] else rng.uniform(20, 28), 1),
                    "humidity_pct": round(rng.uniform(40, 70), 1),
                }
            )
    return records


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic LogiStream source data.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--orders-per-day", type=int, default=40)
    parser.add_argument("--sensor-points", type=int, default=12)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    orders = build_orders(rng, args.days, args.orders_per_day)
    logistics = build_logistics(rng, orders)
    feedback = build_feedback(rng, orders)
    sensors = build_sensors(rng, logistics, args.sensor_points)

    write_jsonl(args.out / "orders.jsonl", orders)
    write_jsonl(args.out / "logistics.jsonl", logistics)
    write_jsonl(args.out / "feedback.jsonl", feedback)
    write_jsonl(args.out / "sensors.jsonl", sensors)

    summary = {
        "orders": len(orders),
        "logistics": len(logistics),
        "feedback": len(feedback),
        "sensors": len(sensors),
        "output": str(args.out),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
