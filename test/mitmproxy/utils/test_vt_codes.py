import io
import os
import sys
import ctypes
import importlib
from unittest import mock
import pytest
from mitmproxy.utils import vt_codes
from mitmproxy.utils.vt_codes import ensure_supported


def test_simple():
    assert not ensure_supported(io.StringIO())


@pytest.fixture
def win_vt(monkeypatch):
    fake_windll = mock.MagicMock()
    monkeypatch.setattr(os, "name", "nt")
    monkeypatch.setattr(ctypes, "windll", fake_windll, raising=False)
    mod = importlib.reload(vt_codes)
    yield mod, fake_windll.kernel32
    monkeypatch.undo()
    importlib.reload(vt_codes)


def test_win_not_a_tty(win_vt):
    mod, kernel32 = win_vt
    assert mod.ensure_supported(io.StringIO()) is False
    kernel32.GetStdHandle.assert_not_called()

def test_win_tty_but_not_std_stream(win_vt):
    mod, kernel32 = win_vt
    f = mock.Mock()
    f.isatty.return_value = True

    assert mod.ensure_supported(f) is False
    kernel32.GetStdHandle.assert_not_called()

def test_win_get_console_mode_fails(win_vt, monkeypatch):
    mod, kernel32 = win_vt
    f = mock.Mock()
    f.isatty.return_value = True
    monkeypatch.setattr(sys, "stdout", f)
    kernel32.GetConsoleMode.return_value = 0

    assert not mod.ensure_supported(f)
    kernel32.SetConsoleMode.assert_not_called()
    
    
def test_win_success_enables_vt(win_vt, monkeypatch):
    mod, kernel32 = win_vt
    f = mock.Mock()
    f.isatty.return_value = True
    monkeypatch.setattr(sys, "stderr", f)
    kernel32.GetConsoleMode.return_value = 1
    kernel32.SetConsoleMode.return_value = 1

    assert mod.ensure_supported(f)
    kernel32.GetStdHandle.assert_called_once_with(mod.STD_ERROR_HANDLE)
    handle, mode = kernel32.SetConsoleMode.call_args.args
    assert mode & mod.ENABLE_VIRTUAL_TERMINAL_PROCESSING