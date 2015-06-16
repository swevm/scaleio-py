import logging


class ScaleIOLogger: 
    instance = None

    @classmethod
    def get(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        # How to use:
        # loggerInstance = ScaleIOLogger.get()
        # logger = loggerInstance.getLogger('DEBUG')
        logging.basicConfig(format='%(asctime)s: %(levelname)s %(module)s:%(funcName)s | %(message)s',level=self._get_log_level(debugLevel))
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Logger initialized!")
        
    def getLogger(self, loglevel):
        return _get_log_level(loglevel)
    
    @staticmethod
    def _get_log_level(level):
        """
        small static method to get logging level
        :param str level: string of the level e.g. "INFO"
        :returns logging.<LEVEL>: appropriate debug level
        """
        # default to DEBUG
        if level is None or level == "DEBUG":
            return logging.DEBUG

        level = level.upper()
        # Make debugging configurable
        if level == "INFO":
            return logging.INFO
        elif level == "WARNING":
            return logging.WARNING
        elif level == "CRITICAL":
            return logging.CRITICAL
        elif level == "ERROR":
            return logging.ERROR
        elif level == "FATAL":
            return logging.FATAL
        else:
            raise Exception("UnknownLogLevelException: enter a valid log level")
