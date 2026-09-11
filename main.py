from extract import extract
from load import load

def run_pipeline():
    print("=== ELT PIPELINE START ===")
    df = extract()
    load(df)
    print("=== EXTRACT + LOAD DONE — now run sql/03_transform_raw_to_staging.sql in pgAdmin4 ===")

if __name__ == "__main__":
    run_pipeline()