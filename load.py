import psycopg2
from psycopg2.extras import execute_values
from config import DB_CONFIG
from extract import extract

def load(df, table="raw.source_data"):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(f"TRUNCATE TABLE {table};")  # wipe old raw data before reloading

    columns = list(df.columns)
    df = df.where(pd.notnull(df), None)   # convert NaN -> Python None -> real SQL NULL
    values = [tuple(row) for row in df.itertuples(index=False)]

    insert_query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES %s"
    execute_values(cur, insert_query, values)

    conn.commit()
    print(f"[LOAD] Inserted {len(values)} rows into {table}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    df = extract()
    load(df)