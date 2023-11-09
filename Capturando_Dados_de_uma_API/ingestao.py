from abc import ABC, abstractmethod
from typing import List

import requests
import logging
import datetime
import json
import os



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class mercado_bitcoin_api(ABC):

    def __init__(self, coin: str) -> None:
        self.coin = coin
        self.base_endpoint = "https://www.mercadobitcoin.net/api"

    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass

    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
class day_summary_api(mercado_bitcoin_api):
    type = "day-summary"

    def _get_endpoint(self, date: datetime.date) -> str:
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"
    
class trades_api(mercado_bitcoin_api):
    type = "trades"

    def _get_unix_epoch(self, date: datetime.datetime) -> int:
        return int(date.timestamp())

    def _get_endpoint(self, date_from: datetime.datetime = None, date_to: datetime.datetime = None) -> str:
        if date_from and not date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}"
        elif date_from and date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            unix_date_to = self._get_unix_epoch(date_to)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}"
        else:
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"

        return endpoint
    
#print(trades_api(coin="BTC").get_date())
#print(trades_api(coin="BTC").get_date(date_from=datetime.datetime(2023, 8, 11)))
#print(trades_api(coin="BTC").get_date(date_from=datetime.datetime(2023, 8, 11), date_to=datetime.datetime(2023, 8, 11)))

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
  

#data = day_summary_api(coin="BTC").get_data(date=datetime.date(2023, 8, 11))
#writer = data_writer("day-summary.json")
#writer.write(data)

#data = trades_api("BTC").get_data()
#writer = data_writer("trades.json")
#writer.write(data)

class data_ingestor(ABC):

    def __init__(self, writer, coins: List[str], default_start_date: datetime.datetime) -> None:
        self.coins = coins
        self.default_start_date = default_start_date
        self.writer = writer

    @abstractmethod
    def ingest(self) -> None:
        pass

class day_summary_ingestor(data_ingestor):

    def ingest(self) -> None:
        date = self.default_start_date
        if date < datetime.date.today():
            for coin in self.coins:
                api = day_summary_api(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
                # atualizar a data

ingestor = day_summary_ingestor(writer=data_writer, coins=["BTC", "ETH", "LTC"], default_start_date=datetime.date(2023, 8, 11))
ingestor.ingest()     

