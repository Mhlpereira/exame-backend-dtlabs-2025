CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS sensor_data (
    time TIMESTAMP NOT NULL,
    sensor_id INT,
    value FLOAT
);

SELECT create_hypertable('sensor_data', 'time');