import sys
import threading

from loguru import logger

from api import EnergyData
from handler import Handler

try:
    from screen import show_info
except (ModuleNotFoundError, RuntimeError):
    # A RuntimeError is thrown if the EPD library cannot find the required
    # files to write to the screen.
    if "screen" in sys.argv:
        logger.error(
            "We cannot communicate with the screen. "
            + "Verify that the requirements are installed with `pip install co2monitor[screen]'. "
            + "If that is not sufficient, verify that you are running on a raspberry pi. "
            + "Check waveshare docs."
        )
        raise


class ScreenUpdater(Handler):
    def __init__(self, font: str):
        super().__init__()
        self.lock = threading.Lock()
        self.font = font

    def handle(self, data: EnergyData):
        t = threading.Thread(target=lambda: self._update_screen(data))
        t.start()

    def _update_screen(self, data: EnergyData):
        with self.lock:
            show_info(data, self.font)
