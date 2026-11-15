"""Page Object cho bảng danh sách đơn hàng, tìm kiếm, lọc, sửa, xóa, đổi trạng thái."""
from typing import List
from pages.base_page import BasePage


class OrderListPage(BasePage):
    ROWS = "#order-table tbody tr"
    SEARCH = "#search"
    FILTER_STATUS = "#filter-status"
    COUNT = "#order-count"
    EMPTY_MSG = "#empty-msg"
    MODAL = "#confirm-modal"
    BTN_CONFIRM_YES = "#btn-confirm-yes"
    BTN_CONFIRM_NO = "#btn-confirm-no"

    # ---- bảng ----
    def row_count(self) -> int:
        return self.loc(self.ROWS).count()

    def codes(self) -> List[str]:
        return [self.loc(self.ROWS).nth(i).locator("td.code").inner_text().strip()
                for i in range(self.row_count())]

    def row(self, code: str):
        return self.loc(f"{self.ROWS}[data-order-id='{code}']")

    def cell(self, code: str, column: str) -> str:
        """column: code | name | phone | product | qty | total | payment"""
        return self.row(code).locator(f"td.{column}").inner_text().strip()

    def count_label(self) -> int:
        return int(self.text(self.COUNT))

    def empty_message(self) -> str:
        return self.text(self.EMPTY_MSG) if self.is_visible(self.EMPTY_MSG) else ""

    # ---- tìm kiếm / lọc ----
    def search(self, keyword: str) -> None:
        self.fill(self.SEARCH, keyword)

    def clear_search(self) -> None:
        self.fill(self.SEARCH, "")

    def filter_by_status(self, label: str) -> None:
        self.select(self.FILTER_STATUS, label)

    # ---- hành động trên dòng ----
    def click_edit(self, code: str) -> None:
        self.log.info("Bấm Sửa đơn %s", code)
        self.row(code).locator("button.btn-edit").click()

    def click_delete(self, code: str) -> None:
        self.log.info("Bấm Xóa đơn %s", code)
        self.row(code).locator("button.btn-delete").click()

    def confirm_delete(self) -> None:
        self.click(self.BTN_CONFIRM_YES)

    def cancel_delete(self) -> None:
        self.click(self.BTN_CONFIRM_NO)

    def is_modal_open(self) -> bool:
        return self.is_visible(self.MODAL)

    def change_status(self, code: str, label: str) -> None:
        self.log.info("Đổi trạng thái đơn %s -> %s", code, label)
        self.row(code).locator(".status-select").select_option(label=label)

    def status_of(self, code: str) -> str:
        return self.row(code).locator(".status-select").input_value()
