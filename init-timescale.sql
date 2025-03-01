CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE sensor_data (
    id SERIAL,
    server_ulid TEXT NOT NULL,
    sensor_type TEXT NOT NULL,
    value FLOAT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL
);

SELECT create_hypertable('sensor_data', 'timestamp', partitioning_column => 'server_ulid', number_partitions => 1000);