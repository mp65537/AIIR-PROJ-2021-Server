import msgpack
import logging

from functools import partial
from http.server import HTTPServer, HTTPStatus, BaseHTTPRequestHandler

MIME_OCTET_STREAM = "application/octet-stream"
MIME_TEXT_PLAIN = "text/plain"

server_logger = logging.getLogger(__name__)

class BinaryWebServer:
    def __init__(self, address, port, request_handler):
        handler_class = partial(HTTPBinaryRequestHandler, 
            handler_func = request_handler)
        self._http_server = HTTPServer((address, port), handler_class)

    def start_server(self):
        self._http_server.serve_forever()

    def stop_server(self):
        self._http_server.server_close()


class HTTPBinaryRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, handler_func = None, **kwargs):
        self._handler_func = handler_func
        super().__init__(*args, **kwargs)

    def do_POST(self):
        server_logger.info("Incomming request: " + self.requestline)
        if self.path != "/api":
            self._handle_failure("Invalid URL: " + self.path)
            return
        content_type = self.headers.get("Content-Type", "")
        if content_type != MIME_OCTET_STREAM:
            self._handle_failure("Improper request 'Content-Type': " + content_type)
            return
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self._handle_failure("Empty request or no 'Content-Length'")
            return
        try:
            input_data = msgpack.unpackb(self.rfile.read(content_length))
        except (msgpack.UnpackException, ValueError) as err:
            self._handle_failure("Failed to unpack request data ({})".format(err))
            return
        output_data = msgpack.packb(self._handler_func(input_data))
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", MIME_OCTET_STREAM)
        self.send_header("Content-Length", str(len(output_data)))
        self.end_headers()
        self.wfile.write(output_data)

    def send_error(self, code, message = None, explain = None):
        self._handle_failure(message)

    def log_request(self, code='-', size='-'):
        if isinstance(code, HTTPStatus):
            code = code.value
        server_logger.info("Responsed with {} to '{}'".format(
            code, self.requestline))

    def log_error(self, format, *args):
        server_logger.error(format % args)

    def log_message(self, format, *args):
        server_logger.info(format % args)

    def _handle_failure(self, warn_message = None):
        if warn_message is not None:
            server_logger.warning(warn_message)
        self.send_response(HTTPStatus.BAD_REQUEST)
        self.send_header("Connection", "close")
        self.send_header("Content-Type", MIME_TEXT_PLAIN)
        self.send_header("Content-Length", "0")
        self.end_headers()
