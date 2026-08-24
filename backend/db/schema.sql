-- Pravaha Setu database schema.
-- Adapted from the team's execution-plan doc; one deviation: reservoirs.lat/lon
-- are plain FLOAT columns, not a PostGIS GEOGRAPHY(POINT) -- no spatial-query
-- work is in v1 scope (no river-network geometry), so pulling in PostGIS +
-- GeoAlchemy2 now would be dependency weight with no use. Swap back if that
-- changes (see CLAUDE.md > Tech stack, PostGIS is listed as optional).
--
-- Applied directly via psql for now (see SETUP.md); Alembic migrations
-- are a follow-up once this schema stabilizes.

CREATE TABLE IF NOT EXISTS reservoirs (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    lat FLOAT,
    lon FLOAT,
    max_storage_mcm FLOAT,
    catchment_area_sqkm FLOAT
);

CREATE TABLE IF NOT EXISTS reservoir_observations (
    id SERIAL PRIMARY KEY,
    reservoir_id INT NOT NULL REFERENCES reservoirs(id),
    obs_date DATE NOT NULL,
    storage_mcm FLOAT,
    inflow_cumecs FLOAT,
    outflow_cumecs FLOAT,
    source TEXT NOT NULL,
    UNIQUE (reservoir_id, obs_date, source)
);

CREATE TABLE IF NOT EXISTS rainfall_grid (
    id SERIAL PRIMARY KEY,
    reservoir_id INT NOT NULL REFERENCES reservoirs(id),
    obs_date DATE NOT NULL,
    rainfall_mm FLOAT,
    source TEXT NOT NULL,
    UNIQUE (reservoir_id, obs_date, source)
);

CREATE TABLE IF NOT EXISTS gauge_observations (
    id SERIAL PRIMARY KEY,
    gauge_name TEXT NOT NULL,      -- 'Rajaram Weir', 'Sangli', etc.
    obs_date DATE NOT NULL,
    obs_time TIME,
    stage_m FLOAT,
    discharge_cumecs FLOAT,
    source TEXT
);

CREATE TABLE IF NOT EXISTS forecast_runs (
    id SERIAL PRIMARY KEY,
    reservoir_id INT NOT NULL REFERENCES reservoirs(id),
    run_timestamp TIMESTAMP NOT NULL,
    forecast_horizon_hrs INT,
    predicted_inflow_cumecs FLOAT[],
    model_version TEXT
);

CREATE TABLE IF NOT EXISTS advisory_runs (
    id SERIAL PRIMARY KEY,
    run_timestamp TIMESTAMP NOT NULL,
    recommended_schedule JSONB,   -- {reservoir_id: [release_cumecs per hour]}
    baseline_schedule JSONB,
    projected_peak_kolhapur FLOAT,
    projected_peak_sangli FLOAT
);

INSERT INTO reservoirs (name, max_storage_mcm, catchment_area_sqkm) VALUES
    ('Koyna', 2797, 891.78),
    ('Warna', 776, 776),
    ('Radhanagari', 250.6, 500)
ON CONFLICT (name) DO NOTHING;
