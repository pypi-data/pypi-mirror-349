#!/home/rens/.virtualenvs/monitor/bin/python
import locale
import os
import sys
import threading
from typing import Type

import click
from dotenv import load_dotenv
from loguru import logger

from api import API
from cliprinter import CliPrinter
from handler import Handler
from poller import Poller
from screenupdater import ScreenUpdater
from tray import SystrayCreator

load_dotenv()

API_KEY = os.getenv("API_KEY")
USER_AGENT = os.getenv("USER_AGENT")

locale.setlocale(locale.LC_ALL, "")


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--debug/--no-debug", default=False)
@click.option(
    "--api-key",
    default=API_KEY,
    help="Override API_KEY environment variable.",
)
@click.option(
    "--api-url",
    default="https://api.ned.nl/v1",
    show_default=True,
)
@click.option(
    "--user-agent",
    default=USER_AGENT,
    help="Override USER_AGENT environment varaible.",
)
@click.option(
    "--polltime",
    default=60,
    show_default=True,
)
@click.version_option(package_name="co2monitor")
@click.pass_context
def app(ctx, debug, api_key, api_url, user_agent, polltime):
    "Shows the current CO2 emissions per kWh of electricity in the Netherlands."
    logger.remove()
    logger.add(sys.stdout, level="DEBUG" if debug else "INFO")
    ctx.ensure_object(dict)
    ctx.obj["api_url"] = api_url
    ctx.obj["api_key"] = api_key
    ctx.obj["user_agent"] = user_agent
    ctx.obj["polltime"] = polltime


@app.command(name="cli", help="Print emissions to the commandline.")
@click.pass_context
def cli(ctx):
    run(ctx.obj, CliPrinter())


@app.command(name="screen", help="Show emissions on an EPD screen connected via GPIO.")
@click.pass_context
@click.option("--font", default="Font.ttc", show_default=True)
def screen(ctx, font):
    if not os.path.exists(font):
        raise ValueError(f"File {font} does not exist. Pass a valid truetype font with --font.")
    handler = ScreenUpdater(font)
    run(ctx.obj, handler)


@app.command(name="tray", help="Add a system tray icon with emissions.")
@click.pass_context
@click.option("--font", default="Font.ttc", show_default=True)
def tray(ctx, font):
    if not os.path.exists(font):
        raise ValueError(f"File {font} does not exist. Pass a valid truetype font with --font.")
    with SystrayCreator(font) as handler:
        t = threading.Thread(target=lambda: run(ctx.obj, handler))
        t.start()
        handler.app.exec()


def run(opts: dict, handler: Handler):
    api = API(opts["api_url"], opts["api_key"], opts["user_agent"])
    poller = Poller(api, handler, int(opts["polltime"]))
    poller.start()
