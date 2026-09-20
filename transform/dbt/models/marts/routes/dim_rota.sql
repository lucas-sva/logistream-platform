{{ config(alias="dim_rota") }}

select
    row_number() over (order by route_id) as sk_rota,
    route_id,
    max(origin_cd) as origin_cd
from {{ ref('stg_logistics') }}
group by route_id
