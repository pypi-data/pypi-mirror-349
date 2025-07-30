import io
import pytest
from adolib.logger import SimpleLogger

def test_debug_log(capsys):
    logger = SimpleLogger(use_timestamp=False)
    logger.debug("debug test")
    captured = capsys.readouterr()
    assert "DEBUG: debug test" in captured.out

def test_info_log(capsys):
    logger = SimpleLogger(use_timestamp=False)
    logger.info("info test")
    captured = capsys.readouterr()
    assert "INFO: info test" in captured.out

def test_success_log(capsys):
    logger = SimpleLogger(use_timestamp=False)
    logger.success("success test")
    captured = capsys.readouterr()
    assert "SUCCESS: success test" in captured.out

def test_warning_log(capsys):
    logger = SimpleLogger(use_timestamp=False)
    logger.warning("warning test")
    captured = capsys.readouterr()
    assert "WARNING: warning test" in captured.out

def test_error_log(capsys):
    logger = SimpleLogger(use_timestamp=False)
    logger.error("error test")
    captured = capsys.readouterr()
    assert "ERROR: error test" in captured.err

def test_critical_log(capsys):
    logger = SimpleLogger(use_timestamp=False)
    logger.critical("critical test")
    captured = capsys.readouterr()
    assert "CRITICAL: critical test" in captured.err