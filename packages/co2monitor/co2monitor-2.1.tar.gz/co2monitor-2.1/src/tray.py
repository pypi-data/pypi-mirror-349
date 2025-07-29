import signal
import sys
import tempfile

from loguru import logger

try:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont, QFontMetrics, QIcon, QPainter, QPixmap
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
        self._font_family = font
        self.image_file = tempfile.NamedTemporaryFile(suffix=".png")

        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.icon = QSystemTrayIcon()
        self.icon.setIcon(self.create_icon("..."))
        self.icon.show()

    def __exit__(self, exc_type, exc_value, traceback):
        logger.debug("Exiting")
        self.image_file.close()
        self.app.exit()

    def handle(self, data: EnergyData):
        co2: float = data.co2_amount * 1000

        self.icon.setIcon(self.create_icon(str(round(co2))))
        self.icon.setToolTip(
            f"{data.datetime_ams.strftime('%H:%M')}: {co2:.2f}g CO₂/kWh"
        )

    def create_icon(self, text: str) -> QIcon:
        pixmap_size = 128
        pixmap = QPixmap(pixmap_size, pixmap_size)
        pixmap.fill(Qt.white)

        font_size, x, y = self.find_font_parameters(
            text, self._font_family, pixmap_size, padding=3
        )
        font = QFont(self._font_family, font_size)

        painter = QPainter()
        painter.begin(pixmap)
        painter.setFont(font)
        painter.setPen(Qt.black)
        painter.drawText(x, y, text)
        painter.end()

        return QIcon(pixmap)

    @staticmethod
    def find_font_parameters(
        text: str, family: str, pixmap_size: int, padding: int
    ) -> tuple[int, int, int]:
        """Takes as input a text, font family, pixmap size and desired
        padding, and computes a tuple with (font_size, x, y) so as to
        perfectly fill the text within the pixmap, with the minimum
        amount of padding below `padding`.

        """
        max_font_size = pixmap_size
        min_font_size = 1

        while min_font_size < max_font_size - 1:
            mid_font_size = (min_font_size + max_font_size) // 2
            font = QFont(family, mid_font_size)
            metrics = QFontMetrics(font)

            width = metrics.horizontalAdvance(text)
            height = metrics.height()

            if (
                width <= pixmap_size - 2 * padding
                and height <= pixmap_size - 2 * padding
            ):
                # This size fits, try larger
                min_font_size = mid_font_size
            else:
                # Too big, try smaller
                max_font_size = mid_font_size

        x = (pixmap_size - width) / 2
        y = (pixmap_size + height) / 2 - metrics.descent()
        return mid_font_size, x, y
