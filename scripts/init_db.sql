"""
PostgreSQL initialization SQL — runs automatically on first docker-compose up.
"""

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ── Plants ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS plants (
    plant_id     VARCHAR(10)  PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    location     VARCHAR(100),
    country      VARCHAR(50),
    established  DATE,
    capacity     INTEGER,
    created_at   TIMESTAMPTZ  DEFAULT NOW()
);

-- ── Production Lines ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS production_lines (
    line_id      VARCHAR(10)  PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    plant_id     VARCHAR(10)  REFERENCES plants(plant_id),
    line_type    VARCHAR(50),
    capacity_per_hour INTEGER,
    status       VARCHAR(20)  DEFAULT 'active',
    created_at   TIMESTAMPTZ  DEFAULT NOW()
);

-- ── Suppliers ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id  VARCHAR(10)  PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    country      VARCHAR(50),
    contact_name VARCHAR(100),
    email        VARCHAR(150),
    rating       NUMERIC(3,1),
    tier         INTEGER      DEFAULT 1,
    created_at   TIMESTAMPTZ  DEFAULT NOW()
);

-- ── Materials ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS materials (
    material_id   VARCHAR(10)  PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    category      VARCHAR(50),
    unit          VARCHAR(20),
    unit_cost     NUMERIC(10,2),
    lead_time_days INTEGER,
    supplier_id   VARCHAR(10)  REFERENCES suppliers(supplier_id),
    created_at    TIMESTAMPTZ  DEFAULT NOW()
);

-- ── Machines ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS machines (
    machine_id        VARCHAR(10)  PRIMARY KEY,
    name              VARCHAR(100) NOT NULL,
    machine_type      VARCHAR(50),
    plant_id          VARCHAR(10)  REFERENCES plants(plant_id),
    line_id           VARCHAR(10)  REFERENCES production_lines(line_id),
    supplier_id       VARCHAR(10)  REFERENCES suppliers(supplier_id),
    manufacturer      VARCHAR(100),
    model_number      VARCHAR(50),
    installation_date DATE,
    status            VARCHAR(20)  DEFAULT 'operational',
    created_at        TIMESTAMPTZ  DEFAULT NOW()
);

-- ── Sensors ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sensors (
    sensor_id     VARCHAR(10)  PRIMARY KEY,
    machine_id    VARCHAR(10)  REFERENCES machines(machine_id),
    sensor_type   VARCHAR(50),  -- temperature, vibration, pressure, etc.
    unit          VARCHAR(20),
    min_threshold NUMERIC(10,3),
    max_threshold NUMERIC(10,3),
    location_tag  VARCHAR(50),
    status        VARCHAR(20)  DEFAULT 'active',
    created_at    TIMESTAMPTZ  DEFAULT NOW()
);

-- ── Employees ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS employees (
    employee_id  VARCHAR(10)  PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    role         VARCHAR(50),
    department   VARCHAR(50),
    plant_id     VARCHAR(10)  REFERENCES plants(plant_id),
    email        VARCHAR(150),
    hire_date    DATE,
    created_at   TIMESTAMPTZ  DEFAULT NOW()
);

-- ── Production Orders ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS production_orders (
    order_id       VARCHAR(15)  PRIMARY KEY,
    product_name   VARCHAR(100) NOT NULL,
    line_id        VARCHAR(10)  REFERENCES production_lines(line_id),
    plant_id       VARCHAR(10)  REFERENCES plants(plant_id),
    quantity       INTEGER,
    start_date     DATE,
    end_date       DATE,
    status         VARCHAR(20)  DEFAULT 'planned',
    priority       VARCHAR(10)  DEFAULT 'normal',
    created_at     TIMESTAMPTZ  DEFAULT NOW()
);

-- ── Maintenance Events ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS maintenance_events (
    event_id        VARCHAR(15)  PRIMARY KEY,
    machine_id      VARCHAR(10)  REFERENCES machines(machine_id),
    event_type      VARCHAR(30),  -- preventive, corrective, emergency
    description     TEXT,
    technician_id   VARCHAR(10)  REFERENCES employees(employee_id),
    start_time      TIMESTAMPTZ,
    end_time        TIMESTAMPTZ,
    duration_hours  NUMERIC(5,2),
    root_cause      VARCHAR(200),
    parts_replaced  VARCHAR(200),
    cost            NUMERIC(10,2),
    created_at      TIMESTAMPTZ  DEFAULT NOW()
);

-- ── Quality Events ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS quality_events (
    quality_id     VARCHAR(15)  PRIMARY KEY,
    order_id       VARCHAR(15)  REFERENCES production_orders(order_id),
    machine_id     VARCHAR(10)  REFERENCES machines(machine_id),
    inspector_id   VARCHAR(10)  REFERENCES employees(employee_id),
    inspection_type VARCHAR(30),
    result         VARCHAR(20),  -- pass, fail, conditional
    defect_type    VARCHAR(100),
    defect_count   INTEGER       DEFAULT 0,
    notes          TEXT,
    inspection_time TIMESTAMPTZ,
    created_at     TIMESTAMPTZ  DEFAULT NOW()
);

-- ── Telemetry ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS telemetry (
    id             BIGSERIAL    PRIMARY KEY,
    sensor_id      VARCHAR(10)  REFERENCES sensors(sensor_id),
    machine_id     VARCHAR(10)  REFERENCES machines(machine_id),
    value          NUMERIC(12,4) NOT NULL,
    unit           VARCHAR(20),
    is_anomaly     BOOLEAN      DEFAULT FALSE,
    threshold_exceeded BOOLEAN  DEFAULT FALSE,
    recorded_at    TIMESTAMPTZ  NOT NULL,
    created_at     TIMESTAMPTZ  DEFAULT NOW()
);

-- ── Indexes ───────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_machines_plant     ON machines(plant_id);
CREATE INDEX IF NOT EXISTS idx_machines_line      ON machines(line_id);
CREATE INDEX IF NOT EXISTS idx_sensors_machine    ON sensors(machine_id);
CREATE INDEX IF NOT EXISTS idx_telemetry_sensor   ON telemetry(sensor_id);
CREATE INDEX IF NOT EXISTS idx_telemetry_time     ON telemetry(recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_maintenance_machine ON maintenance_events(machine_id);
CREATE INDEX IF NOT EXISTS idx_quality_machine    ON quality_events(machine_id);

COMMENT ON TABLE machines IS 'Enterprise assets: CNC, Robot, Conveyor, Compressor, etc.';
COMMENT ON TABLE telemetry IS 'Time-series sensor readings — 10k+ records per day';
