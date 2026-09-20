{{ config(alias="dim_data") }}

with bounds as (
    select
        date_trunc('day', min(order_ts))::date as start_date,
        date_trunc('day', max(order_ts))::date + 30 as end_date
    from {{ ref('stg_orders') }}
),
series as (
    select generate_series(start_date, end_date, interval '1 day')::date as calendar_date
    from bounds
)
select
    to_char(calendar_date, 'YYYYMMDD')::int as sk_data,
    calendar_date,
    extract(year from calendar_date)::int as year,
    extract(quarter from calendar_date)::int as quarter,
    extract(month from calendar_date)::int as month,
    extract(week from calendar_date)::int as iso_week,
    extract(dow from calendar_date)::int as day_of_week,
    extract(dow from calendar_date) in (0, 6) as is_weekend
from series
