import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from config import DB_CONFIG
from logger import get_logger

log = get_logger("load")

def load(df, table="raw.live_users"):
    df = df.where(pd.notnull(df), None)  # NaN -> real NULL

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    columns = list(df.columns)
    values = [tuple(row) for row in df.itertuples(index=False)]

    update_clause = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns if col != "id"])

    insert_query = f"""
        INSERT INTO {table} ({', '.join(columns)}, extracted_at)
        VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            {update_clause},
            extracted_at = NOW()
    """

    # append NOW() for extracted_at on each row
    template = "(" + ", ".join(["%s"] * len(columns)) + ", NOW())"

    execute_values(cur, insert_query, values, template=template)

    conn.commit()
    log.info(f"Upserted {len(values)} rows into {table}")

    cur.close()
    conn.close()
    return len(values)

if __name__ == "__main__":
    from extract import extract
    df = extract()
    load(df)