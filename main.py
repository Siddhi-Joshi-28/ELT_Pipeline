import psycopg2
from datetime import datetime
from config import DB_CONFIG
from extract import extract
from load import load
from transform import transform
from logger import get_logger

log = get_logger("main")

def log_run(started_at, ended_at, rows_extracted, rows_loaded, status, error_message=None):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO analytics.pipeline_runs
        (started_at, ended_at, rows_extracted, rows_loaded, status, error_message)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (started_at, ended_at, rows_extracted, rows_loaded, status, error_message))
    conn.commit()
    cur.close()
    conn.close()

def run_pipeline():
    started_at = datetime.now()
    rows_extracted = 0
    rows_loaded = 0

    try:
        log.info("=== ELT PIPELINE START ===")

        df = extract()
        rows_extracted = len(df)

        rows_loaded = load(df)

        transform()

        ended_at = datetime.now()
        log_run(started_at, ended_at, rows_extracted, rows_loaded, "SUCCESS")
        log.info(f"=== PIPELINE COMPLETE in {(ended_at - started_at).total_seconds():.2f}s ===")

    except Exception as e:
        ended_at = datetime.now()
        log.error(f"Pipeline failed: {e}")
        log_run(started_at, ended_at, rows_extracted, rows_loaded, "FAILED", str(e))
        raise

if __name__ == "__main__":
    run_pipeline()