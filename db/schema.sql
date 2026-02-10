-- DIMENSION TABLES

CREATE TABLE dim_users (
    user_id        INT PRIMARY KEY,
    name           VARCHAR(100),
    username       VARCHAR(100),
    email          VARCHAR(150),
    phone          VARCHAR(50),
    website        VARCHAR(100),
    city           VARCHAR(100),
    company        VARCHAR(150),
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE dim_grounds (
    ground_id       INT PRIMARY KEY,
    ground_name     VARCHAR(150),
    location        VARCHAR(150),
    ground_type     VARCHAR(100),
    price_per_hour  NUMERIC(10,2),
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE dim_date (
    date_id     SERIAL PRIMARY KEY,
    full_date   DATE UNIQUE,
    day         INT,
    month       INT,
    year        INT,
    quarter     INT,
    weekday     INT,
    weekday_name VARCHAR(20)
);


-- FACT TABLE

CREATE TABLE fact_bookings (
    booking_id     INT PRIMARY KEY,

    user_id        INT,
    ground_id      INT,
    date_id        INT,

    booking_date   DATE,
    slot_time      VARCHAR(50),
    duration_hours NUMERIC(5,2),
    total_price    NUMERIC(10,2),
    booking_status VARCHAR(50),

    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign Keys
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES dim_users(user_id),

    CONSTRAINT fk_ground
        FOREIGN KEY (ground_id)
        REFERENCES dim_grounds(ground_id),

    CONSTRAINT fk_date
        FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);
