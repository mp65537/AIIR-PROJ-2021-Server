import logging

class ListLoggingHandler(logging.Handler):
    def __init__(self, log_list):
        super().__init__()

    def emit(self, record):
        self.log_list.append(self.format(record))
