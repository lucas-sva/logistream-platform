{{ config(alias="feat_rota_veiculo") }}

select
    vehicle_id,
    departed_ts::date as calendar_date,
    count(*) as deliveries,
    avg(delay_hours) as avg_delay_hours,
    sum(case when is_late then 1 else 0 end)::float / count(*) as late_pct,
    avg(distance_km) as avg_distance_km,
    avg(weight_occupancy_pct) as avg_weight_occupancy_pct
from {{ ref('stg_logistics') }}
group by 1, 2
