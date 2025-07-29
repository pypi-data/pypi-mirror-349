import time
from typing import Optional

from loguru import logger

from api import API, EnergyData
from handler import Handler


class Poller:
    def __init__(self, api: API, handler: Handler, interval: int):
        self.handler = handler
        self.api = api
        self.interval = interval
        self.data: Optional[EnergyData] = None

    def start(self):
        while True:
            self.poll()
            time.sleep(self.interval)

    def poll(self):
        logger.debug("Polling for new data from API")
        try:
            new_data = self.api.get_data()
        except Exception as e:
            logger.exception("Could not reach API! Error: {}", e)
            return

        if new_data == self.data:
            logger.debug("Data wasn't updated, doing nothing.")
        else:
            logger.debug("Data changed, handling new data.")
            self.data = new_data
            self.handler.handle(self.data)
