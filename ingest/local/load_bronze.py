"""Load generated JSONL into the local Bronze lake (MinIO or filesystem)."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SRC = ROOT / "data" / "output"
DEFAULT_DST = ROOT / "data" / "output" / "bronze"


def copy_jsonl(src: Path, dst: Path) -> int:
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    dst.write_bytes(data)
    return len(data)


def put_minio(src: Path, bucket: str, key: str) -> None:
    import boto3

    client = boto3.client(
        "s3",
        endpoint_url=os.environ.get("MINIO_ENDPOINT", "http://localhost:9000"),
        aws_access_key_id=os.environ.get("MINIO_ROOT_USER", "logistream"),
        aws_secret_access_key=os.environ.get("MINIO_ROOT_PASSWORD", "logistream123"),
        region_name="us-east-1",
    )
    try:
        client.head_bucket(Bucket=bucket)
    except Exception:
        client.create_bucket(Bucket=bucket)
    client.upload_file(str(src), bucket, key)


def main() -> int:
    parser = argparse.ArgumentParser(description="Load Bronze from generated JSONL.")
    parser.add_argument("--src", type=Path, default=DEFAULT_SRC)
    parser.add_argument("--dst", type=Path, default=DEFAULT_DST)
    parser.add_argument("--minio", action="store_true", help="Also upload to MinIO.")
    parser.add_argument("--bucket", default="logistream-bronze")
    args = parser.parse_args()

    dt = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    mapping = {
        "orders.jsonl": f"orders/dt={dt}/orders.jsonl",
        "logistics.jsonl": f"logistics/dt={dt}/logistics.jsonl",
        "feedback.jsonl": f"feedback/dt={dt}/feedback.jsonl",
        "sensors.jsonl": f"sensors/dt={dt}/sensors.jsonl",
    }

    loaded = []
    for filename, key in mapping.items():
        src = args.src / filename
        if not src.exists():
            print(f"missing {src}", file=sys.stderr)
            return 1
        bytes_written = copy_jsonl(src, args.dst / key)
        if args.minio:
            put_minio(src, args.bucket, key)
        loaded.append({"key": key, "bytes": bytes_written})

    for row in loaded:
        print(f"{row['key']} {row['bytes']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
