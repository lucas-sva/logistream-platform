"""Structured Streaming sink from Kafka sensor topics into Bronze."""

from __future__ import annotations

import argparse

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, StringType, StructField, StructType


SENSOR_SCHEMA = StructType(
    [
        StructField("event_id", StringType()),
        StructField("event_ts", StringType()),
        StructField("device_id", StringType()),
        StructField("device_type", StringType()),
        StructField("vehicle_id", StringType()),
        StructField("origin_cd", StringType()),
        StructField("metric", StringType()),
        StructField("lat", DoubleType()),
        StructField("lon", DoubleType()),
        StructField("speed_kmh", DoubleType()),
        StructField("temperature_c", DoubleType()),
        StructField("humidity_pct", DoubleType()),
    ]
)

TOPICS = ",".join(
    [
        "sensors.fleet.gps",
        "sensors.fleet.environment",
        "sensors.warehouse.environment",
    ]
)


def spark_session() -> SparkSession:
    return (
        SparkSession.builder.appName("logistream-sensors-stream")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap", default="localhost:9092")
    parser.add_argument("--checkpoint", default="data/output/checkpoints/sensors")
    parser.add_argument("--output", default="data/output/lake/bronze/sensors_stream")
    args = parser.parse_args()

    spark = spark_session()
    raw = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", args.bootstrap)
        .option("subscribe", TOPICS)
        .option("startingOffsets", "latest")
        .load()
    )

    parsed = (
        raw.select(F.from_json(F.col("value").cast("string"), SENSOR_SCHEMA).alias("event"))
        .select("event.*")
        .withColumn("event_ts_parsed", F.to_timestamp("event_ts"))
        .withWatermark("event_ts_parsed", "2 minutes")
        .withColumn("ingested_at", F.current_timestamp())
    )

    query = (
        parsed.writeStream.format("parquet")
        .option("path", args.output)
        .option("checkpointLocation", args.checkpoint)
        .outputMode("append")
        .start()
    )
    query.awaitTermination()


if __name__ == "__main__":
    main()
