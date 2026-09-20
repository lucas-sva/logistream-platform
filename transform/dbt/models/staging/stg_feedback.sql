{{ config(alias="stg_feedback") }}

select
    feedback_id,
    order_id,
    customer_id,
    submitted_ts::timestamptz as submitted_ts,
    product_score,
    delivery_score,
    nps_group,
    contains_pii
from {{ source('bronze', 'feedback') }}
