import logging

from server import BinaryWebServer

listen_address = "0.0.0.0"
listen_port = 8080

logging_handler = logging.FileHandler("events.log", encoding = "utf-8")
logging.basicConfig(
    handlers = (logging_handler,), level = logging.INFO,
    format = "[{asctime}] [{levelname}] [{name}] {message}", 
    datefmt = "%H:%M:%S %d/%m/%Y", style="{")

def handle_build_request(request_data):
    return {}

logging.info("Application has been started")
external_server = BinaryWebServer(
    listen_address, listen_port, handle_build_request)
try:
    external_server.start_server()
except KeyboardInterrupt:
    logging.info("Received Ctrl+C. Closing..")
external_server.stop_server()
