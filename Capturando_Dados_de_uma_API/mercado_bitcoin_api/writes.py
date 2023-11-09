from typing import List

import datetime
import json
import os

from apis import day_summary_api, trades_api


class DataTypeNotSupportedForIngestionException(Exception):

    def __init__(self, data):
        self.data = data
        self.message = f"Data type {type(data)} is not supported for ingestion"
        super().__init__(self.message)

class data_writer:

    def __init__(self, coin: str, api: str) -> None:
        self.coin = coin
        self.api = api
        self.filename = f"{self.api}/{self.coin}/{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.json"

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, "a") as f:
            f.write(row)

    def write(self, data: [List, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, List):
           for element in data:
          
            self.write(element)
        else:
            raise DataTypeNotSupportedForIngestionException(data)
  

data = day_summary_api(coin="BTC").get_data(date=datetime.date(2023, 8, 11))
writer = data_writer("day-summary.json")
writer.write(data)

data = trades_api("BTC").get_data()
writer = data_writer("trades.json")
writer.write(data)