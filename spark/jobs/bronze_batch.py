"""Promote raw JSONL from the landing zone into Bronze parquet tables."""

from __future__ import annotations

import argparse

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

SOURCES = ("orders", "logistics", "feedback", "sensors")


def spark_session() -> SparkSession:
    return (
        SparkSession.builder.appName("logistream-bronze-batch")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def ingest_source(spark: SparkSession, source: str, input_root: str, output_root: str) -> None:
    src = f"{input_root}/{source}"
    dst = f"{output_root}/bronze/{source}"
    df = spark.read.json(src)
    df = df.withColumn("ingested_at", F.current_timestamp()).withColumn(
        "source_system", F.lit(source)
    )
    (
        df.write.mode("overwrite")
        .partitionBy("source_system")
        .parquet(dst)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", default="data/output/bronze")
    parser.add_argument("--output-root", default="data/output/lake")
    args = parser.parse_args()

    spark = spark_session()
    for source in SOURCES:
        ingest_source(spark, source, args.input_root, args.output_root)
    spark.stop()


if __name__ == "__main__":
    main()
