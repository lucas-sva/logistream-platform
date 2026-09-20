# dbt project for Gold marts (demand and routes).

Local target: PostgreSQL. Production target: Databricks SQL / Spark, same model names.

```sh
cd transform/dbt
dbt parse --profiles-dir .
dbt run --profiles-dir .
dbt test --profiles-dir .
```
