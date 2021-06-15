import logging

from head import start_head, is_head
from worker import start_worker

logging_handler = logging.FileHandler("events.log", encoding = "utf-8")
logging.basicConfig(
    handlers = (logging_handler,), level = logging.INFO,
    format = "[{asctime}] [{levelname}] [{name}] {message}", 
    datefmt = "%H:%M:%S %d/%m/%Y", style="{")

if __name__ == "__main__":
    if is_head():
        start_head()
    else:
        start_worker()
