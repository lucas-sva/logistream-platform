{{ config(alias="fato_entrega") }}

select
    l.delivery_id,
    l.order_id,
    d.sk_data as sk_data_saida,
    v.sk_veiculo,
    r.sk_rota,
    loc.sk_localidade as sk_localidade_destino,
    cd.sk_cd,
    l.promised_hours,
    l.actual_hours,
    l.delay_hours,
    l.transport_cost,
    l.distance_km,
    l.weight_occupancy_pct,
    l.volume_occupancy_pct,
    l.is_late,
    l.occurrence_flag,
    l.status
from {{ ref('stg_logistics') }} l
inner join {{ ref('dim_data') }} d
    on d.calendar_date = l.departed_ts::date
inner join {{ ref('dim_veiculo') }} v
    on v.vehicle_id = l.vehicle_id
inner join {{ ref('dim_rota') }} r
    on r.route_id = l.route_id
inner join {{ ref('dim_localidade') }} loc
    on loc.city = l.destination_city
    and loc.state = l.destination_state
inner join {{ ref('dim_cd') }} cd
    on cd.origin_cd = l.origin_cd
