# src/infrastructure/logs/logging.py
import logging
import logging_loki
import time
from src.domain.interfaces import ILogger

class LokiLogger(ILogger):
    def __init__(self, url: str):
        self.logger = logging.getLogger("app-logger")
        # Configura el handler de Loki
        handler = logging_loki.LokiHandler(url=url, version="1")
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def info(self, message: str, **kwargs):
        self.logger.info(message, extra={"tags": kwargs})

    def error(self, message: str, **kwargs):
        self.logger.error(message, extra={"tags": kwargs})
