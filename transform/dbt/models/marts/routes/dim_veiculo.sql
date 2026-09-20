{{ config(alias="dim_veiculo") }}

select
    row_number() over (order by vehicle_id) as sk_veiculo,
    vehicle_id,
    max(origin_cd) as home_cd
from {{ ref('stg_logistics') }}
group by vehicle_id
