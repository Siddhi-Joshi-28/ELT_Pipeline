# ELT Pipeline — Live Data (Practice Project)

A practice ELT (Extract, Load, Transform) pipeline that pulls live data from a
public API, loads it untouched into PostgreSQL, then transforms it **inside**
the database using SQL. Built to understand how ELT differs from ETL and to
practice a pattern used in real data engineering projects.

## What is ELT (vs ETL)?

- **ETL**: Extract → Transform (in Python/app code) → Load clean data into the DB
- **ELT**: Extract → **Load raw data into the DB first** → Transform **inside
  the database** using SQL

This project loads raw, messy data as-is into a `raw` schema, then uses SQL to
clean and reshape it into a `staging` schema. The database does the
transformation work, not Python.

## Project Structure

```
elt_pipeline/
├── .env                        # DB credentials + API URL (not committed)
├── requirements.txt
├── config.py                   # loads settings from .env
├── logger.py                   # logging setup (console + logs/pipeline.log)
├── extract.py                  # pulls live data from the API, with retries
├── load.py                     # upserts raw data into Postgres
├── transform.py                # runs the SQL transform file
├── main.py                     # orchestrates extract -> load -> transform
├── scheduler.py                # runs main.py automatically every 10 minutes
├── data/
│   └── source_data.csv         # optional static sample data (early version)
└── sql/
    ├── 01_create_schemas.sql
    ├── 02_create_raw_table.sql
    ├── 03_create_audit_table.sql
    └── 04_transform_raw_to_staging.sql
```

## Database Schemas

| Schema      | Purpose                                                   |
|-------------|------------------------------------------------------------|
| `raw`       | Untouched data, exactly as extracted from the source       |
| `staging`   | Cleaned, typed, deduplicated data — produced by SQL         |
| `analytics` | Pipeline run history / audit log (and future reporting)    |

**Tables:**
- `raw.live_users` — raw upserted rows from the API, one per `id`
- `staging.clean_users` — cleaned version of the same rows
- `analytics.pipeline_runs` — one row per pipeline run: start/end time, rows
  extracted/loaded, status, and error message if it failed

## Setup

1. **Create the database** in pgAdmin4: right-click *Databases* → *Create* →
   name it `elt_practice`.

2. **Run the SQL setup** in the Query Tool, in order:
   - `sql/01_create_schemas.sql`
   - `sql/02_create_raw_table.sql`
   - `sql/03_create_audit_table.sql`

   (`04_transform_raw_to_staging.sql` is run automatically by `transform.py`
   — you don't need to run it manually.)

3. **Configure `.env`** with your DB credentials:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=elt_practice
   DB_USER=postgres
   DB_PASSWORD=your_password_here
   API_URL=https://jsonplaceholder.typicode.com/users
   ```

4. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Running the Pipeline

**One-time run:**
```
python main.py
```
This extracts data from the live API, upserts it into `raw.live_users`, then
transforms it into `staging.clean_users` — all in one command.

**Continuous / scheduled run:**
```
python scheduler.py
```
Runs the pipeline immediately, then automatically every 10 minutes. Leave it
running in a terminal; `Ctrl+C` to stop.

## Checking the Data

In pgAdmin4's Query Tool:

```sql
-- Raw data, untouched
SELECT * FROM raw.live_users ORDER BY id;

-- Cleaned/transformed data
SELECT * FROM staging.clean_users ORDER BY id;

-- Pipeline run history
SELECT * FROM analytics.pipeline_runs ORDER BY run_id DESC;

-- Compare raw vs staging side by side
SELECT
    r.id,
    r.name AS raw_name,
    s.name AS clean_name,
    r.extracted_at,
    s.updated_at
FROM raw.live_users r
JOIN staging.clean_users s ON r.id = s.id
ORDER BY r.id;
```

Or browse visually: **Databases → elt_practice → Schemas → (raw / staging /
analytics) → Tables → right-click a table → View/Edit Data → All Rows.**

## Key Design Choices

- **Upsert, not overwrite** — `load.py` and the transform SQL use
  `ON CONFLICT (id) DO UPDATE`, so re-running the pipeline updates existing
  rows instead of duplicating or wiping data. This is what makes it safe to
  run repeatedly against a live, changing source.
- **Retries on extract** — `extract.py` retries failed API calls (default: 3
  attempts) before giving up, since live sources occasionally time out.
- **Audit logging** — every run writes a row to `analytics.pipeline_runs`,
  recording success/failure and row counts, so pipeline history is queryable
  instead of only living in log files.
- **NULL handling** — missing values (empty strings, pandas `NaN`) are
  converted to real SQL `NULL`s before insert, and the transform SQL
  defensively handles both cases when casting types.

## Extending This Project

- Add data quality checks (duplicate `id`s, invalid values) before promoting
  raw → staging
- Add an `analytics` summary table/view aggregating `staging.clean_users`
- Swap `API_URL` for a different live source — no other file needs to change
  as long as the response can be normalized into the same columns
- Replace the `schedule` library with a proper orchestrator (e.g. Airflow,
  cron, or Windows Task Scheduler) for production-style scheduling