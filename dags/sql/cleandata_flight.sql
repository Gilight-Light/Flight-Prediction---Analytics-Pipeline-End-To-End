CREATE TABLE IF NOT EXISTS cleandata_flight (
    date VARCHAR(50),
    airline VARCHAR(50),
    flight VARCHAR(50),
    source_city VARCHAR(100),
    departure_time VARCHAR(50),
    stops VARCHAR(50),
    arrival_time VARCHAR(50),
    destination_city VARCHAR(100),
    class VARCHAR(50),
    duration FLOAT,
    days_left INT,
    price INT
);