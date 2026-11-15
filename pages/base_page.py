"""Lớp cha của mọi Page Object: bọc các thao tác Playwright và ghi log."""
from playwright.sync_api import Page, Locator
from utils.logger import get_logger


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.log = get_logger(self.__class__.__name__)

    # ---- điều hướng ----
    def goto(self, path: str = "") -> None:
        url = f"{self.base_url}{path}"
        self.log.info("Mở trang: %s", url)
        self.page.goto(url)

    def reload(self) -> None:
        self.log.info("Tải lại trang")
        self.page.reload()

    # ---- thao tác ----
    def loc(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def click(self, selector: str) -> None:
        self.log.info("Click: %s", selector)
        self.loc(selector).click()

    def fill(self, selector: str, value: str) -> None:
        self.log.info("Nhập '%s' vào %s", value, selector)
        self.loc(selector).fill(value)

    def select(self, selector: str, label: str) -> None:
        self.log.info("Chọn '%s' ở %s", label, selector)
        self.loc(selector).select_option(label=label)

    # ---- đọc dữ liệu ----
    def text(self, selector: str) -> str:
        return self.loc(selector).inner_text().strip()

    def value(self, selector: str) -> str:
        return self.loc(selector).input_value()

    def is_visible(self, selector: str) -> bool:
        return self.loc(selector).is_visible()
