CREATE TABLE IF NOT EXISTS analytics.pipeline_runs (
    run_id SERIAL PRIMARY KEY,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    rows_extracted INT,
    rows_loaded INT,
    status TEXT,
    error_message TEXT
);