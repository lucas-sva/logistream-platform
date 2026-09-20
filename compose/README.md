# Demo local: Kafka, MinIO (lake) e PostgreSQL (alvo dbt).

```sh
docker compose -f compose/docker-compose.yml up -d
python scripts/run_demo.py --postgres --dry-run-stream
```

Airbyte OSS nao sobe neste compose. As conexoes de producao estao em `ingest/airbyte/connections.yaml`.
