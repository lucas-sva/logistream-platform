{{ config(alias="fato_leitura_sensor") }}

select
    device_id,
    device_type,
    vehicle_id,
    origin_cd,
    event_minute,
    avg(lat) as lat,
    avg(lon) as lon,
    avg(speed_kmh) as speed_kmh,
    avg(temperature_c) as temperature_c,
    avg(humidity_pct) as humidity_pct,
    count(*) as event_count
from {{ ref('stg_sensors') }}
group by 1, 2, 3, 4, 5
