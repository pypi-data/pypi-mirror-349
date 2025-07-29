import os
import time

from loguru import logger
from PIL import Image, ImageDraw, ImageFont

from api import EnergyData

from .epd2in9b_V3 import EPD

MARGIN = 10
HEIGHT = 128
WIDTH = 296


class TextDoesNotFitError(Exception):
    pass


class ScreenWriter:
    """
    Class that allows you to write text to the EPD display with high-level functions.
    """

    def __init__(self):
        self._epd = EPD()
        self._epd.init()
        time.sleep(0.5)

        self._image = Image.new("1", (self._epd.height, self._epd.width), 255)
        self._draw = ImageDraw.Draw(self._image)

    def draw_left(self, height: int, text: str, font: ImageFont.FreeTypeFont) -> None:
        """Draws some text left-aligned at a certain height."""
        self._raise_if_text_does_not_fit(text, font)
        self._draw.text((MARGIN, height), text, font=font)

    def draw_right(self, height: int, text: str, font: ImageFont.FreeTypeFont) -> None:
        """Draws some text right-aligned at a certain height."""
        self._raise_if_text_does_not_fit(text, font)
        length = self._draw.textlength(text, font=font)
        self._draw.text((WIDTH - MARGIN - length, height), text, font=font)

    def write(self) -> None:
        logger.debug("Drawing at {}", time.strftime("%H:%M"))
        empty = Image.new("1", (self._epd.height, self._epd.width), 255)
        self._epd.display(self._epd.getbuffer(self._image), self._epd.getbuffer(empty))
        self._epd.sleep()
        logger.debug("Finished drawing")

    def _raise_if_text_does_not_fit(
        self, text: str, font: ImageFont.FreeTypeFont
    ) -> None:
        length = self._draw.textlength(text, font=font)
        if length > WIDTH - MARGIN:
            raise TextDoesNotFitError(
                f"Text has length {length}, but can be max {WIDTH - MARGIN}"
            )


def show_info(data: EnergyData, font: str):
    screen_writer = ScreenWriter()

    co2 = f"{data.co2_amount * 1000:.2f}g CO₂/kWh"
    screen_writer.draw_left(0, co2, get_font(font, 36))
    screen_writer.draw_right(95, data.date_str, get_font(font, 24))

    screen_writer.write()


def get_font(filename: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(filename, size)
