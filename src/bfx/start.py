import logging
from bfxapi import Client
from bfxapi.models.subscription import Subscription
from bfxapi.models.ticker import Ticker

from . import PUB_WS_HOST, coins

log = logging.getLogger(__name__)
bfx = Client(ws_host=PUB_WS_HOST, logLevel="INFO")


async def start():
    """subscribe to ticker channels"""
    for key in coins.keys():
        sym = f"t{key}USD"
        await bfx.ws.subscribe("ticker", symbol=sym)


@bfx.ws.on("subscribed")  # type: ignore
def show_subscribed(sub: Subscription):
    log.info(f"Ticker channel {sub.symbol} subscribed")


@bfx.ws.on("ticker_update")  # type: ignore
def update_ticker(ticker: Ticker):
    log.debug(f"Ticker {ticker.pair} update")


@bfx.ws.on("error")  # type: ignore
def error_handler(message):
    log.error(f"SP: {message}")


@bfx.ws.on("all")  # type: ignore
def bfxws_data_handler(data):
    """
    emit ticker updates from bitfinex to all
    """
    if isinstance(data, str):
        log.info(f"bfx-info: {data}")


bfx.ws.on("connected", start)
