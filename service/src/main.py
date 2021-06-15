import logging

from head import start_head, is_head
from worker import start_worker
import sys
logging_handler = logging.FileHandler("events.log", encoding = "utf-8")
stdout_handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(
    handlers = (logging_handler,stdout_handler), level = logging.INFO,
    format = "[{asctime}] [{levelname}] [{name}] {message}", 
    datefmt = "%H:%M:%S %d/%m/%Y", style="{")

if __name__ == "__main__":
    if is_head():
        start_head()
    else:
        start_worker()
