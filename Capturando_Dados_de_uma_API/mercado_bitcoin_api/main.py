import datetime
import time

from schedule import repeat, every, run_pending
from ingestors import day_summary_ingestor
from writes import data_writer

if __name__ == "__main__":
    day_summary_ingestor = day_summary_ingestor(
        writer=data_writer, 
        coins=["BTC", "ETH", "LTC"], 
        default_start_date=datetime.date(2023, 8, 11)
        )
    
    @repeat(every(1).seconds)
    def job():
        day_summary_ingestor.ingest() 

    while True:
        run_pending()
        time.sleep(0.5)

