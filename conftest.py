"""Fixture dùng chung + hook chụp màn hình / log / trace khi test FAIL."""
import base64
import functools
import http.server
import re
import threading
from datetime import datetime

import pytest
from playwright.sync_api import sync_playwright

from pages.order_form_page import OrderFormPage
from pages.order_list_page import OrderListPage
from utils import config
from utils.logger import get_logger

try:
    from pytest_html import extras as html_extras
except ImportError:  # chạy được cả khi chưa cài pytest-html
    html_extras = None

log = get_logger("conftest")


# ------------------------------------------------------------------ server demo
class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture(scope="session")
def base_url():
    """Dùng BASE_URL nếu có, ngược lại tự phục vụ thư mục demo_app/."""
    if config.BASE_URL:
        log.info("Test trên môi trường: %s", config.BASE_URL)
        yield config.BASE_URL
        return
    handler = functools.partial(_QuietHandler, directory=str(config.DEMO_APP_DIR))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_address[1]}"
    log.info("Chạy web demo tại %s", url)
    yield url
    server.shutdown()


# ------------------------------------------------------------------ trình duyệt
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as pw:
        launcher = getattr(pw, config.BROWSER)
        br = launcher.launch(headless=config.HEADLESS, slow_mo=config.SLOW_MO)
        log.info("Mở trình duyệt %s (headless=%s)", config.BROWSER, config.HEADLESS)
        yield br
        br.close()


@pytest.fixture
def context(browser, request):
    """Mỗi test một context mới => localStorage sạch, test độc lập nhau."""
    ctx = browser.new_context(viewport=config.VIEWPORT, locale="vi-VN")
    ctx.set_default_timeout(config.DEFAULT_TIMEOUT_MS)
    ctx.tracing.start(screenshots=True, snapshots=True)
    yield ctx
    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    if failed:
        name = re.sub(r"[^\w\-]+", "_", request.node.name)[:80]
        trace_path = config.TRACE_DIR / f"{name}.zip"
        ctx.tracing.stop(path=str(trace_path))
        log.error("Đã lưu trace: %s", trace_path)
    else:
        ctx.tracing.stop()
    ctx.close()


@pytest.fixture
def page(context):
    pg = context.new_page()
    pg.on("console", lambda m: log.warning("Browser console error: %s", m.text)
          if m.type == "error" else None)
    pg.on("pageerror", lambda e: log.error("Lỗi JavaScript trên trang: %s", e))
    return pg


# ------------------------------------------------------------------ page objects
@pytest.fixture
def form(page, base_url):
    return OrderFormPage(page, base_url).open()


@pytest.fixture
def orders(page, base_url, form):  # phụ thuộc form để trang đã được mở
    return OrderListPage(page, base_url)


@pytest.fixture
def create_orders(form):
    """Tạo nhanh nhiều đơn: create_orders(order1, order2, ...)"""
    def _create(*items):
        for item in items:
            form.create_order(item)
    return _create


# ------------------------------------------------------------------ hook báo cáo
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call":
        tc = item.get_closest_marker("tc")
        tc_id = tc.args[0] if tc else "-"
        log.info("[%s] %s => %s", tc_id, item.name, report.outcome.upper())

    if report.when in ("setup", "call") and report.failed:
        page = item.funcargs.get("page")
        if page is None or page.is_closed():
            return
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = re.sub(r"[^\w\-]+", "_", item.name)[:80]
        path = config.SCREENSHOT_DIR / f"{stamp}_{name}.png"
        try:
            png = page.screenshot(path=str(path), full_page=True)
        except Exception as exc:  # noqa: BLE001
            log.error("Không chụp được màn hình: %s", exc)
            return
        log.error("TEST FAIL: %s | screenshot: %s | url: %s", item.nodeid, path, page.url)
        if html_extras is not None:
            extra = getattr(report, "extras", [])
            extra.append(html_extras.image(base64.b64encode(png).decode(),
                                           mime_type="image/png", extension="png"))
            extra.append(html_extras.url(page.url, name="URL khi fail"))
            report.extras = extra
