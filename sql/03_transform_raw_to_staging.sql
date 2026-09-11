CREATE TABLE IF NOT EXISTS staging.clean_data AS
SELECT
    id::INT AS id,
    INITCAP(TRIM(name)) AS name,
    NULLIF(signup_date, '')::DATE AS signup_date,
    COALESCE(NULLIF(amount, '')::NUMERIC, 0) AS amount
FROM raw.source_data
WHERE id IS NOT NULL;