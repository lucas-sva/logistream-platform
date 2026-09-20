{{ config(alias="stg_orders") }}

select
    order_id,
    order_item_id,
    order_ts::timestamptz as order_ts,
    channel,
    customer_id,
    sku,
    quantity,
    unit_price,
    discount_amount,
    (unit_price * quantity) - discount_amount as net_amount,
    status,
    processing_minutes,
    destination_city,
    destination_state,
    destination_zip,
    origin_cd,
    status = 'cancelled' as is_cancelled
from {{ source('bronze', 'orders') }}
