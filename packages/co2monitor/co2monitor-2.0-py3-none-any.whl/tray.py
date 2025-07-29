import signal
import sys
import tempfile

from loguru import logger

try:
    from PIL import Image, ImageDraw, ImageFont
    from PySide6.QtGui import QIcon
    from PySide6.QtWidgets import QApplication, QSystemTrayIcon
except ModuleNotFoundError:
    if "tray" in sys.argv:
        logger.error(
            "The required dependencies were not installed - "
            + "a system tray icon cannot be created. "
            + "Install them via `pip install co2monitor[tray]'."
        )
        raise

from api import EnergyData
from handler import Handler

signal.signal(signal.SIGINT, signal.SIG_DFL)


class SystrayCreator(Handler):
    def __init__(self, font):
        super().__init__()
        self._font = font
        self.image_file = tempfile.NamedTemporaryFile(suffix=".png")

        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.icon = QSystemTrayIcon()
        self.icon.show()

    def __exit__(self, exc_type, exc_value, traceback):
        logger.debug("Exiting")
        self.image_file.close()
        self.app.exit()

    def handle(self, data: EnergyData):
        co2: float = data.co2_amount * 1000

        image = self.image(str(round(co2)), self.font)
        filename = self.image_file.name
        image.save(filename)

        self.icon.setIcon(QIcon(filename))
        self.icon.setToolTip(
            f"{data.datetime_ams.strftime('%H:%M')}: {co2:.2f}g CO₂/kWh"
        )

    @staticmethod
    def image(text, font):
        image = Image.new("RGB", (64, 64), "white")
        draw = ImageDraw.Draw(image)
        draw.text((1, 10), text, fill="black", font=font)
        return image

    @property
    def font(self):
        return ImageFont.truetype(self._font, size=36)
