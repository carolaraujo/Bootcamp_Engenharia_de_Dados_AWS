from abc import ABC, abstractmethod
from typing import List

import datetime

from apis import day_summary_api

class data_ingestor(ABC):

    def __init__(self, writer, coins: List[str], default_start_date: datetime.datetime) -> None:
        self.coins = coins
        self.default_start_date = default_start_date
        self.writer = writer
        self._checkpoint = self._load_checkpoint

    @property
    def _checkpoint_filename(self) -> str:
        return f"{self.__class__.__name__}.checkpoint"

    def _write_checkpoint(self):
        with open(self._checkpoint_filename, "w") as f:
            f.write(f"{self._checkpoint}")

    def _load_checkpoint(self) -> datetime:
        try:
            with open(self._checkpoint_filename, "r") as f:
                return datetime.date.strptime(f.read(), "%Y-%m-%d").date()
        except FileNotFoundError:
            return None

    def _get_checkpoint(self):
        if not self._checkpoint:
            return self.default_start_date
        else:
            return self._checkpoint
        
    def _update_checkpoint(self, value):
        self._checkpoint = value
        self._write_checkpoint()


    @abstractmethod
    def ingest(self) -> None:
        pass

class day_summary_ingestor(data_ingestor):

    def ingest(self) -> None:
        date = self._get_checkpoint()() 
        if date < datetime.date.today():
            for coin in self.coins:
                api = day_summary_api(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
                self._update_checkpoint(date + datetime.timedelta(days=1)) 
