"""Test the lazy logging implementation."""

import tempfile
from pathlib import Path

from lda.logging.lazy_logger import LazyLDALogger


def test_lazy_logger_no_logs_no_files():
    """Test that lazy logger doesn't create files when not used."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = Path(temp_dir) / "logs"
        
        # Create logger but don't log anything
        logger = LazyLDALogger(log_dir=str(log_dir))
        logger.cleanup()
        
        # Verify no files were created
        assert not log_dir.exists() or not list(log_dir.glob("*.log"))


def test_lazy_logger_with_logs_creates_files():
    """Test that lazy logger creates files when actually logging."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = Path(temp_dir) / "logs"
        
        # Create logger and log something
        logger = LazyLDALogger(log_dir=str(log_dir))
        logger.info("Test message")
        logger.cleanup()
        
        # Verify file was created and has content
        log_files = list(log_dir.glob("*.log"))
        assert len(log_files) == 1
        assert log_files[0].stat().st_size > 0


def test_lazy_logger_cleanup_removes_empty():
    """Test that cleanup removes empty log files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = Path(temp_dir) / "logs"
        
        # Create multiple loggers, only use some
        logger1 = LazyLDALogger(log_dir=str(log_dir))
        logger2 = LazyLDALogger(log_dir=str(log_dir))
        logger3 = LazyLDALogger(log_dir=str(log_dir))
        
        # Only log with logger2
        logger2.warning("Test warning")
        
        # Cleanup all
        logger1.cleanup()
        logger2.cleanup()
        logger3.cleanup()
        
        # Should only have one non-empty log file
        log_files = list(log_dir.glob("*.log"))
        assert len(log_files) == 1
        assert log_files[0].stat().st_size > 0


def test_lazy_logger_operations():
    """Test various logging operations work correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = Path(temp_dir) / "logs"
        
        logger = LazyLDALogger(log_dir=str(log_dir))
        
        # Test different log levels
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message", exception=ValueError("test"))
        
        # Test operation logging
        logger.log_operation("test_op", "success", duration=1.5)
        logger.log_file_operation("create", "/test/file", True)
        logger.log_section_operation("section1", "initialized", True)
        
        # Verify file was created
        log_file = logger.get_log_file()
        assert log_file is not None
        assert Path(log_file).exists()
        
        logger.cleanup()
        
        # File should still exist since we logged
        assert Path(log_file).exists()