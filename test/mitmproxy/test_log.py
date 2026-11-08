import logging
from unittest import mock
import pytest
from PyInstaller.log import level

from mitmproxy import log


def test_logentry():
    e = log.LogEntry("foo", "info")
    assert repr(e) == "LogEntry(foo, info)"

    f = log.LogEntry("foo", "warning")
    assert e == e
    assert e != f
    assert e != 42


def test_dont_pick_up_mutations():
    x = {"foo": "bar"}
    e = log.LogEntry(x, "info")
    x["foo"] = "baz"  # this should not affect the log entry anymore.
    assert repr(e) == "LogEntry({'foo': 'bar'}, info)"


def test_log_debug_deprecated():
    logger = log.Log(master=None)
    with mock.patch("logging.getLogger") as get_logger:
        with pytest.warns(DeprecationWarning, match=r"ctx\.log\.debug\(\) is deprecated"):
            logger.debug("hello")

    get_logger.return_value.debug.assert_called_once_with("hello")


def test_log_info_deprecated():
    logger = log.Log(master=None)
    with mock.patch("logging.getLogger") as get_logger:
        with pytest.warns(DeprecationWarning, match=r"ctx\.log\.info\(\) is deprecated"):
            logger.info("hello")

    get_logger.return_value.info.assert_called_once_with("hello")


def test_log_alert_deprecated():
    logger = log.Log(master=None)
    with mock.patch("logging.getLogger") as get_logger:
        with pytest.warns(DeprecationWarning, match=r"ctx\.log\.alert\(\) is deprecated"):
            logger.alert("hello")

    get_logger.return_value.log.assert_called_once_with(log.ALERT, "hello")


def test_log_warn_deprecated():
    logger = log.Log(master=None)
    with mock.patch("logging.getLogger") as get_logger:
        with pytest.warns(DeprecationWarning, match=r"ctx\.log\.warn\(\) is deprecated"):
            logger.warn("hello")

    get_logger.return_value.warning.assert_called_once_with("hello")


def test_log_error_deprecated():
    logger = log.Log(master=None)
    with mock.patch("logging.getLogger") as get_logger:
        with pytest.warns(DeprecationWarning, match=r"ctx\.log\.error\(\) is deprecated"):
            logger.error("hello")

    get_logger.return_value.error.assert_called_once_with("hello")


def test_log_call_deprecated():
    logger = log.Log(master=None)
    with mock.patch("logging.getLogger") as get_logger:
        with pytest.warns(DeprecationWarning, match=r"ctx\.log\(\) is deprecated"):
            logger("hello", level="warn")

    get_logger.return_value.log.assert_called_once_with(level=logging.WARNING, msg="hello")