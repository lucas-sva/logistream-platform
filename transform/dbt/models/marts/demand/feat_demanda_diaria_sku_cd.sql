{{ config(alias="feat_demanda_diaria_sku_cd") }}

select
    origin_cd,
    sku,
    order_ts::date as calendar_date,
    sum(quantity) as quantity,
    sum(net_amount) as net_amount,
    sum(case when is_cancelled then 1 else 0 end) as cancelled_items
from {{ ref('stg_orders') }}
group by 1, 2, 3
