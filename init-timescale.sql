CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE sensor_data (
    id SERIAL,
    server_ulid TEXT NOT NULL,
    sensor_type TEXT NOT NULL,
    value FLOAT NOT NULL,
    server_time TIMESTAMPTZ NOT NULL
);

ALTER TABLE sensor_data ALTER COLUMN server_time TYPE TIMESTAMP;

SELECT create_hypertable('sensor_data', 'server_time', partitioning_column => 'server_ulid', number_partitions => 1000);