from logging import LogRecord

from pytest import LogCaptureFixture, fixture, mark

from ..src.logs import *


@fixture(autouse= True)
def setCaplogLvl(caplog: LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)
    caplog.clear()


class TestLogs:
    @mark.parametrize('msg', [
        'Debug test message',
    ])
    def test_debug(self, msg: str, caplog: LogCaptureFixture) -> None:
        debugLog(msg)
        record: LogRecord = caplog.records[0]
        assert record.message == msg
        assert record.levelno == logging.DEBUG
        assert record.name == 'PyUtils.pyUtils.src.logs'

    @mark.parametrize('msg', [
        'Info test message',
    ])
    def test_info(self, msg: str, caplog: LogCaptureFixture) -> None:
        infoLog(msg)
        record: LogRecord = caplog.records[0]
        assert record.message == msg
        assert record.levelno == logging.INFO
        assert record.name == 'PyUtils.pyUtils.src.logs'

    @mark.parametrize('msg', [
        'Warning test message',
    ])
    def test_warning(self, msg: str, caplog: LogCaptureFixture) -> None:
        warningLog(msg)
        record: LogRecord = caplog.records[0]
        assert record.message == msg
        assert record.levelno == logging.WARNING
        assert record.name == 'PyUtils.pyUtils.src.logs'

    @mark.parametrize('msg', [
        'Error test message',
    ])
    def test_error(self, msg: str, caplog: LogCaptureFixture) -> None:
        errorLog(msg)
        record: LogRecord = caplog.records[0]
        assert record.message == msg
        assert record.levelno == logging.ERROR
        assert record.name == 'PyUtils.pyUtils.src.logs'

    @mark.parametrize('msg', [
        'Critical test message',
    ])
    def test_critical(self, msg: str, caplog: LogCaptureFixture) -> None:
        criticalLog(msg)
        record: LogRecord = caplog.records[0]
        assert record.message == msg
        assert record.levelno == logging.CRITICAL
        assert record.name == 'PyUtils.pyUtils.src.logs'

    @mark.parametrize('lvl, nMessages', [
        (logging.DEBUG, 5),
        (logging.INFO, 4),
        (logging.WARNING, 3),
        (logging.ERROR, 2),
        (logging.CRITICAL, 1),
    ])
    def test_setLoggingLevel(self, lvl: int, nMessages: int,  caplog: LogCaptureFixture) -> None:
        setLoggingLevel(lvl)
        debugLog('Debug test message')
        infoLog('Info test message')
        warningLog('Warning test message')
        errorLog('Error test message')
        criticalLog('Critical test message')
        assert len(caplog.records) == nMessages
