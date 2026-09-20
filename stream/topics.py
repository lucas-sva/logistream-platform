"""Kafka topic names for LogiStream sensor streams."""

TOPICS = [
    {
        "name": "sensors.fleet.gps",
        "partitions": 6,
        "retention_ms": 172800000,
        "value_schema": "sensors.schema.json",
        "filter": "fleet_gps",
    },
    {
        "name": "sensors.fleet.environment",
        "partitions": 6,
        "retention_ms": 172800000,
        "value_schema": "sensors.schema.json",
        "filter": "fleet_environment",
    },
    {
        "name": "sensors.warehouse.environment",
        "partitions": 3,
        "retention_ms": 172800000,
        "value_schema": "sensors.schema.json",
        "filter": "warehouse_environment",
    },
]
