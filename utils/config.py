"""Cấu hình chung. Có thể ghi đè bằng biến môi trường."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEMO_APP_DIR = ROOT / "demo_app"
LOG_DIR = ROOT / "logs"
SCREENSHOT_DIR = ROOT / "screenshots"
REPORT_DIR = ROOT / "reports"
TRACE_DIR = REPORT_DIR / "traces"

# Nếu để trống, framework tự chạy web demo trong thư mục demo_app/
BASE_URL = os.getenv("BASE_URL", "").rstrip("/")
BROWSER = os.getenv("BROWSER", "chromium")          # chromium | firefox | webkit
HEADLESS = os.getenv("HEADED", "0") != "1"          # HEADED=1 để xem trình duyệt chạy
SLOW_MO = int(os.getenv("SLOW_MO", "0"))            # ms, tiện khi demo
DEFAULT_TIMEOUT_MS = int(os.getenv("TIMEOUT_MS", "5000"))
VIEWPORT = {"width": 1280, "height": 900}

for _d in (LOG_DIR, SCREENSHOT_DIR, REPORT_DIR, TRACE_DIR):
    _d.mkdir(parents=True, exist_ok=True)
