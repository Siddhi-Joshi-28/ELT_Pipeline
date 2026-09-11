CREATE TABLE IF NOT EXISTS raw.live_users (
    id INT PRIMARY KEY,
    name TEXT,
    username TEXT,
    email TEXT,
    phone TEXT,
    website TEXT,
    city TEXT,
    company_name TEXT,
    extracted_at TIMESTAMP DEFAULT NOW()
);