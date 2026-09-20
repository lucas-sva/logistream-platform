{{ config(alias="fato_pedido") }}

select
    o.order_item_id,
    o.order_id,
    d.sk_data as sk_data_pedido,
    p.sk_produto,
    l.sk_localidade,
    c.sk_canal,
    o.origin_cd,
    o.quantity,
    o.unit_price,
    o.discount_amount,
    o.net_amount,
    o.processing_minutes,
    o.is_cancelled
from {{ ref('stg_orders') }} o
inner join {{ ref('dim_data') }} d
    on d.calendar_date = o.order_ts::date
inner join {{ ref('dim_produto') }} p
    on p.sku = o.sku
inner join {{ ref('dim_localidade') }} l
    on l.city = o.destination_city
    and l.state = o.destination_state
inner join {{ ref('dim_canal') }} c
    on c.channel = o.channel
