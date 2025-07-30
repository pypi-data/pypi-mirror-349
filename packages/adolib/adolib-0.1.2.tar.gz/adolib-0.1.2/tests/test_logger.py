import io
import pytest
from adolib.logger import SimpleLogger

def test_info_log(capsys):
    logger = SimpleLogger(use_timestamp=False)
    logger.info("info test")
    captured = capsys.readouterr()
    assert "INFO: info test" in captured.out

def test_warning_log(capsys):
    logger = SimpleLogger(use_timestamp=False)
    logger.warning("warning test")
    captured = capsys.readouterr()
    assert "WARNING: warning test" in captured.err

def test_error_log(capsys):
    logger = SimpleLogger(use_timestamp=False)
    logger.error("error test")
    captured = capsys.readouterr()
    assert "ERROR: error test" in captured.err
