DROP TABLE IF EXISTS staging.clean_data;

CREATE TABLE staging.clean_data AS
SELECT
    id::INT AS id,
    INITCAP(TRIM(name)) AS name,
    NULLIF(NULLIF(signup_date, ''), 'NaN')::DATE AS signup_date,
    COALESCE(NULLIF(NULLIF(amount, ''), 'NaN')::NUMERIC, 0) AS amount
FROM raw.source_data
WHERE id IS NOT NULL;