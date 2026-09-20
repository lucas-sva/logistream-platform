{{ config(alias="dim_produto") }}

select
    row_number() over (order by sku) as sk_produto,
    sku,
    max(unit_price) as reference_price
from {{ ref('stg_orders') }}
group by sku
