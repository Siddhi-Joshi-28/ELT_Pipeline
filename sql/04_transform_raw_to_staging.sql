CREATE TABLE IF NOT EXISTS staging.clean_users (
    id INT PRIMARY KEY,
    name TEXT,
    username TEXT,
    email TEXT,
    phone TEXT,
    website TEXT,
    city TEXT,
    company_name TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO staging.clean_users (id, name, username, email, phone, website, city, company_name)
SELECT
    id,
    INITCAP(TRIM(name)) AS name,
    LOWER(TRIM(username)) AS username,
    LOWER(TRIM(email)) AS email,
    TRIM(phone) AS phone,
    LOWER(TRIM(website)) AS website,
    INITCAP(TRIM(city)) AS city,
    TRIM(company_name) AS company_name
FROM raw.live_users
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    username = EXCLUDED.username,
    email = EXCLUDED.email,
    phone = EXCLUDED.phone,
    website = EXCLUDED.website,
    city = EXCLUDED.city,
    company_name = EXCLUDED.company_name,
    updated_at = NOW();