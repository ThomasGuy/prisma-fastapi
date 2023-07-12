import logging
from bfxapi.utils.custom_logger import CustomLogger

logging.basicConfig(
    filename="./logs/log.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p",
)

logger = CustomLogger("LOG", logLevel="DEBUG")

logger.info("Captains Log...")
