import logzero
from logzero import logger
import configparser
from logzero import setup_logger


class FingreenLogger:
    def __init__(self):
        logger = setup_logger()
        logzero.loglevel(logzero.INFO)

        log_file = self.get_log_file()
        logzero.logfile(log_file, maxBytes=1e6, backupCount=3)
        log_level = self.get_log_level()
        logzero.loglevel(log_level)
        self.logger = logger

    def get_log_file(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        log_file =  config["logger"]["file"]
        return log_file

    def get_log_level(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        level =  config["logger"]["level"]
        level = level.upper()
        if level == "NOTSET":
            return logzero.NOTSET
        elif  level == "CRITICAL":
            return logzero.CRITICAL
        elif  level == "ERROR":
            return logzero.ERROR
        elif  level == "WARN":
            return logzero.WARN
        elif level == "DEBUG":
            return logzero.DEBUG
        else :
            return logzero.INFO
