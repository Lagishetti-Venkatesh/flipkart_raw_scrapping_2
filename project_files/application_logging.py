import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


class application_logger:
    """
    Handles data logging and creates a log file
    """

    def __init__(self, log_name):
        self.log_name = log_name
        self.FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
        self.current_time = datetime.now().strftime("%H:%M:%S")

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.FORMATTER)
        return console_handler

    def get_file_handler(self):
        file_handler = TimedRotatingFileHandler(
            f"{os.getcwd()}/Application_log_data/" + self.log_name + '_' + self.current_time + '.log',
            when='midnight')
        file_handler.setFormatter(self.FORMATTER)
        return file_handler

    def get_logger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())

        # with this pattern, it's rarely necessary to propagate the error up to parent
        logger.propagate = False
        return logger
