{{ config(alias="stg_logistics") }}

select
    delivery_id,
    order_id,
    vehicle_id,
    route_id,
    origin_cd,
    destination_city,
    destination_state,
    promised_hours,
    actual_hours,
    actual_hours - promised_hours as delay_hours,
    actual_hours > promised_hours as is_late,
    transport_cost,
    distance_km,
    weight_occupancy_pct,
    volume_occupancy_pct,
    departed_ts::timestamptz as departed_ts,
    delivered_ts::timestamptz as delivered_ts,
    status,
    occurrence_flag
from {{ source('bronze', 'logistics') }}
