import psycopg2
from config import DB_CONFIG
from logger import get_logger

log = get_logger("transform")

def transform(sql_file="sql/04_transform_raw_to_staging.sql"):
    with open(sql_file, "r") as f:
        sql = f.read()

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    log.info(f"Transform complete: {sql_file}")
    cur.close()
    conn.close()

if __name__ == "__main__":
    transform()