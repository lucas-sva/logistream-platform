create schema if not exists bronze;
create schema if not exists silver;
create schema if not exists gold;

create table if not exists bronze.orders (
    order_id text not null,
    order_item_id text primary key,
    order_ts timestamptz not null,
    channel text not null,
    customer_id text not null,
    customer_email text,
    sku text not null,
    quantity integer not null,
    unit_price numeric not null,
    discount_amount numeric not null,
    status text not null,
    processing_minutes integer not null,
    destination_city text not null,
    destination_state text not null,
    destination_zip text not null,
    origin_cd text not null
);

create table if not exists bronze.logistics (
    delivery_id text primary key,
    order_id text not null,
    vehicle_id text not null,
    route_id text not null,
    origin_cd text not null,
    destination_city text,
    destination_state text,
    promised_hours numeric not null,
    actual_hours numeric,
    transport_cost numeric not null,
    distance_km numeric not null,
    weight_occupancy_pct numeric,
    volume_occupancy_pct numeric,
    departed_ts timestamptz not null,
    delivered_ts timestamptz,
    status text not null,
    occurrence_flag boolean
);

create table if not exists bronze.feedback (
    feedback_id text primary key,
    order_id text not null,
    customer_id text not null,
    submitted_ts timestamptz not null,
    product_score integer not null,
    delivery_score integer not null,
    nps_group text,
    comment text,
    contains_pii boolean
);

create table if not exists bronze.sensors (
    event_id text primary key,
    event_ts timestamptz not null,
    device_id text not null,
    device_type text not null,
    vehicle_id text,
    origin_cd text,
    metric text not null,
    lat double precision,
    lon double precision,
    speed_kmh double precision,
    temperature_c double precision,
    humidity_pct double precision
);
