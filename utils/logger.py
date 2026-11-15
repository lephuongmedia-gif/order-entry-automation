"""Logger ghi ra console và file logs/test_run.log."""
import logging
from utils.config import LOG_DIR

_FMT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
_configured = False


def _configure() -> None:
    global _configured
    if _configured:
        return
    root = logging.getLogger("autotest")
    root.setLevel(logging.INFO)
    root.propagate = False
    formatter = logging.Formatter(_FMT, "%H:%M:%S")

    file_handler = logging.FileHandler(LOG_DIR / "test_run.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    root.addHandler(file_handler)
    root.addHandler(console)
    _configured = True


def get_logger(name: str) -> logging.Logger:
    _configure()
    return logging.getLogger(f"autotest.{name}")
