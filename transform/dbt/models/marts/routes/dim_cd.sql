{{ config(alias="dim_cd") }}

select
    row_number() over (order by origin_cd) as sk_cd,
    origin_cd
from {{ ref('stg_orders') }}
group by origin_cd
