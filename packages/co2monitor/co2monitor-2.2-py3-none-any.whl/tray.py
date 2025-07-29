import signal
import sys
import tempfile
import webbrowser
from typing import Optional

from loguru import logger

try:
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
        self.icon.activated.connect(self.open_co2monitor_website)

        # Cached data, set in self.handle() and necessary to repaint
        # if the system pallete changes (user switches dark/light
        # mode).
        self._data = None
        self.app.paletteChanged.connect(lambda: self.handle(self._data))

    def open_co2monitor_website(self):
        webbrowser.open("https://co2monitor.nl")

    def __exit__(self, exc_type, exc_value, traceback):
        logger.debug("Exiting")
        self.image_file.close()
        self.app.exit()

    def handle(self, data: Optional[EnergyData]):
        if data is None:
            logger.warning("No data was given, not updating icon.")
            return

        co2: float = data.co2_amount * 1000
        text = str(round(co2))

        self.icon.setIcon(self.create_icon(text))
        self.icon.setToolTip(
            f"{data.datetime_ams.strftime('%H:%M')}: {co2:.2f}g CO₂/kWh"
        )

        self._data = data

    def create_icon(self, text: str) -> QIcon:
        pixmap_size = 128
        pixmap = QPixmap(pixmap_size, pixmap_size)
        bg_col, text_col = self.system_colors
        pixmap.fill(bg_col)

        font_size, x, y = self.find_font_parameters(
            text, self._font_family, pixmap_size, padding=3
        )
        font = QFont(self._font_family, font_size)

        painter = QPainter()
        painter.begin(pixmap)
        painter.setFont(font)
        painter.setPen(text_col)
        painter.drawText(x, y, text)
        painter.end()

        return QIcon(pixmap)

    @property
    def system_colors(self) -> tuple[int, int]:
        """Returns a tuple of system colors: (bg_col, text_col)."""
        p = self.app.palette()
        window = p.window().color()
        text = p.text().color()

        return window, text

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
