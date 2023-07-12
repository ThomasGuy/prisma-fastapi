import tomli
from bfxapi.constants import WS_HOST, PUB_WS_HOST

with open("config.toml", mode="rb") as f:
    config = tomli.load(f)

coins = config["coins"]
