"""Clean Bronze entities into Silver business tables."""

from __future__ import annotations

import argparse

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def spark_session() -> SparkSession:
    return (
        SparkSession.builder.appName("logistream-silver-batch")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def token(col):
    return F.sha2(col.cast("string"), 256)


def silver_orders(spark: SparkSession, root: str) -> None:
    df = spark.read.parquet(f"{root}/bronze/orders")
    window = Window.partitionBy("order_item_id").orderBy(F.col("order_ts").desc())
    silver = (
        df.withColumn("rn", F.row_number().over(window))
        .where("rn = 1")
        .drop("rn")
        .withColumn("customer_token", token(F.col("customer_id")))
        .drop("customer_email")
        .withColumn("net_amount", F.col("unit_price") * F.col("quantity") - F.col("discount_amount"))
        .withColumn("is_cancelled", F.col("status") == "cancelled")
    )
    silver.write.mode("overwrite").parquet(f"{root}/silver/orders")


def silver_logistics(spark: SparkSession, root: str) -> None:
    df = spark.read.parquet(f"{root}/bronze/logistics")
    window = Window.partitionBy("delivery_id").orderBy(F.col("departed_ts").desc())
    silver = (
        df.withColumn("rn", F.row_number().over(window))
        .where("rn = 1")
        .drop("rn")
        .withColumn("is_late", F.col("actual_hours") > F.col("promised_hours"))
        .withColumn("delay_hours", F.col("actual_hours") - F.col("promised_hours"))
    )
    silver.write.mode("overwrite").parquet(f"{root}/silver/logistics")


def silver_feedback(spark: SparkSession, root: str) -> None:
    df = spark.read.parquet(f"{root}/bronze/feedback")
    silver = (
        df.withColumn("customer_token", token(F.col("customer_id")))
        .withColumn("comment_hash", token(F.col("comment")))
        .drop("comment")
    )
    silver.write.mode("overwrite").parquet(f"{root}/silver/feedback")


def silver_sensors(spark: SparkSession, root: str) -> None:
    df = spark.read.parquet(f"{root}/bronze/sensors")
    silver = df.withColumn(
        "event_minute",
        F.date_trunc("minute", F.to_timestamp("event_ts")),
    )
    silver.write.mode("overwrite").parquet(f"{root}/silver/sensors")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lake-root", default="data/output/lake")
    args = parser.parse_args()
    spark = spark_session()
    silver_orders(spark, args.lake_root)
    silver_logistics(spark, args.lake_root)
    silver_feedback(spark, args.lake_root)
    silver_sensors(spark, args.lake_root)
    spark.stop()


if __name__ == "__main__":
    main()
