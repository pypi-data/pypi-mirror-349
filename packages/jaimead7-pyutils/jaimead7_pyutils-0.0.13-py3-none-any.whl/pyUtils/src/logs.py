import logging


class Styles:
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DEBUG = '\033[94m'
    INFO = '\033[0m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    CRITICAL = '\033[101m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'


class _MyFormatter(logging.Formatter):
    def format(self, record) -> str:
        try:
            customStyle: str = str(record.customStyle)
        except AttributeError:
            customStyle = Styles.ENDC
        arrow: str = '-' * (10-len(record.levelname)) + '>'
        log_fmt: str = f'{customStyle}{record.levelname} {arrow} %(asctime)s:{Styles.ENDC} {record.msg}'
        formatter = logging.Formatter(log_fmt, datefmt='%d/%m/%Y %H:%M:%S')
        return formatter.format(record)


def setLoggingLevel(lvl: int = logging.DEBUG) -> int:
    _logger: logging.Logger = logging.getLogger(__name__)
    _logger.setLevel(lvl)

_logger: logging.Logger = logging.getLogger(__name__)
setLoggingLevel()
_streamHandler = logging.StreamHandler()
_streamHandler.setFormatter(_MyFormatter())
_logger.addHandler(_streamHandler)

def debugLog(msg: str, style: Styles = Styles.DEBUG) -> None:
    _logger.debug(f'{msg}', extra= {'customStyle': style})

def infoLog(msg: str, style: Styles = Styles.INFO) -> None:
    _logger.info(f'{msg}', extra= {'customStyle': style})

def warningLog(msg: str, style: Styles = Styles.WARNING) -> None:
    _logger.warning(f'{msg}', extra= {'customStyle': style})

def errorLog(msg: str, style: Styles = Styles.ERROR) -> None:
    _logger.error(f'{msg}', extra= {'customStyle': style})

def criticalLog(msg: str, style: Styles = Styles.CRITICAL) -> None:
    _logger.critical(f'{msg}', extra= {'customStyle': style})
