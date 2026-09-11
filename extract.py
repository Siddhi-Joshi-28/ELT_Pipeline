import requests
import pandas as pd
import time
from config import API_URL
from logger import get_logger

log = get_logger("extract")

def extract(retries=3, delay=5):
    for attempt in range(1, retries + 1):
        try:
            log.info(f"Extracting from {API_URL} (attempt {attempt})")
            response = requests.get(API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()

            df = pd.json_normalize(data)
            df = df.rename(columns={
                "address.city": "city",
                "company.name": "company_name"
            })
            df = df[["id", "name", "username", "email", "phone", "website", "city", "company_name"]]

            log.info(f"Extracted {len(df)} rows")
            return df

        except requests.exceptions.RequestException as e:
            log.warning(f"Extract failed on attempt {attempt}: {e}")
            if attempt == retries:
                log.error("All retry attempts failed")
                raise
            time.sleep(delay)

if __name__ == "__main__":
    df = extract()
    print(df.head())