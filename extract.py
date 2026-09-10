import pandas as pd

def extract(file_path="data/source_data.csv"):
    df = pd.read_csv(file_path)
    print(f"[EXTRACT] Read {len(df)} rows, {len(df.columns)} columns from {file_path}")
    return df

if __name__ == "__main__":
    df = extract()
    print(df.head())