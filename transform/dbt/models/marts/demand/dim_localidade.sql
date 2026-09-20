{{ config(alias="dim_localidade") }}

select
    row_number() over (order by destination_state, destination_city) as sk_localidade,
    destination_city as city,
    destination_state as state
from {{ ref('stg_orders') }}
group by destination_city, destination_state
