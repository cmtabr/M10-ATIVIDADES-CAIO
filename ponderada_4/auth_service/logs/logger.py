import logging
from datetime import datetime
import os

class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self._setup_handlers(name)
    
    def _setup_handlers(self, name: str):
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('[%(asctime)s] [%(name)s] | %(levelname)s -> %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        log_file_name = os.path.join("./logs/data/", datetime.now().strftime(f"{name}_%Y_%m_%d_%H_%M.log"))
        file_handler = logging.FileHandler(log_file_name)
        file_formatter = logging.Formatter('[%(asctime)5s] [%(name)s] | %(levelname)s -> %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
    def get_logger(self):
        return self.logger
