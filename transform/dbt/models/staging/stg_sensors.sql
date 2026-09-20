{{ config(alias="stg_sensors") }}

select
    event_id,
    event_ts::timestamptz as event_ts,
    date_trunc('minute', event_ts::timestamptz) as event_minute,
    device_id,
    device_type,
    vehicle_id,
    origin_cd,
    metric,
    lat,
    lon,
    speed_kmh,
    temperature_c,
    humidity_pct
from {{ source('bronze', 'sensors') }}
