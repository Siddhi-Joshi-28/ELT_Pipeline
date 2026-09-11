import schedule
import time
from main import run_pipeline
from logger import get_logger

log = get_logger("scheduler")

def job():
    try:
        run_pipeline()
    except Exception:
        log.error("Scheduled run failed — will retry on next interval")

schedule.every(10).minutes.do(job)

if __name__ == "__main__":
    log.info("Scheduler started — running every 10 minutes")
    job()  # run once immediately on startup
    while True:
        schedule.run_pending()
        time.sleep(1)