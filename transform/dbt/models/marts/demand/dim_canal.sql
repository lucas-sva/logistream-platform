{{ config(alias="dim_canal") }}

select
    row_number() over (order by channel) as sk_canal,
    channel
from {{ ref('stg_orders') }}
group by channel
