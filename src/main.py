import logging

logging_handler = logging.FileHandler("events.log", encoding = "utf-8")
logging.basicConfig(
    handlers = (logging_handler,), level = logging.INFO,
    format = "[{asctime}] [{levelname}] [{name}] {message}", 
    datefmt = "%H:%M:%S %d/%m/%Y", style="{")
