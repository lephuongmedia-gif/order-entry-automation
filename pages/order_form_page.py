"""Page Object cho form tạo / sửa đơn hàng."""
from pages.base_page import BasePage
from utils.data import Order, to_int


class OrderFormPage(BasePage):
    PATH = "/index.html"

    NAME = "#customer-name"
    PHONE = "#phone"
    EMAIL = "#email"
    PRODUCT = "#product"
    UNIT_PRICE = "#unit-price"
    QUANTITY = "#quantity"
    ADDRESS = "#address"
    PAY_COD = "#pay-cod"
    PAY_BANK = "#pay-bank"
    NOTE = "#note"
    TOTAL = "#total"
    BTN_SUBMIT = "#btn-submit"
    BTN_RESET = "#btn-reset"
    BTN_CANCEL_EDIT = "#btn-cancel-edit"
    MESSAGE = "#msg"
    FORM_TITLE = "#form-title"
    ERROR_PREFIX = "#err-"

    def open(self) -> "OrderFormPage":
        self.goto(self.PATH)
        return self

    # ---- nhập liệu ----
    def fill_order(self, order: Order) -> None:
        self.fill(self.NAME, order.name)
        self.fill(self.PHONE, order.phone)
        self.fill(self.EMAIL, order.email)
        if order.product:
            self.select(self.PRODUCT, order.product)
        self.fill(self.QUANTITY, order.quantity)
        self.fill(self.ADDRESS, order.address)
        self.click(self.PAY_BANK if order.payment == "Chuyển khoản" else self.PAY_COD)
        self.fill(self.NOTE, order.note)

    def submit(self) -> None:
        self.click(self.BTN_SUBMIT)

    def create_order(self, order: Order) -> None:
        self.fill_order(order)
        self.submit()

    def reset(self) -> None:
        self.click(self.BTN_RESET)

    def cancel_edit(self) -> None:
        self.click(self.BTN_CANCEL_EDIT)

    def select_product(self, label: str) -> None:
        self.select(self.PRODUCT, label)

    def set_quantity(self, value: str) -> None:
        self.fill(self.QUANTITY, value)

    def set_field(self, selector: str, value: str) -> None:
        self.fill(selector, value)

    # ---- đọc trạng thái ----
    def message(self) -> str:
        return self.text(self.MESSAGE)

    def error(self, field: str) -> str:
        """field: customer-name | phone | email | product | quantity | address"""
        return self.text(f"{self.ERROR_PREFIX}{field}")

    def all_errors(self) -> dict:
        fields = ["customer-name", "phone", "email", "product", "quantity", "address"]
        return {f: self.error(f) for f in fields}

    def total_text(self) -> str:
        return self.text(self.TOTAL)

    def total_value(self) -> int:
        return to_int(self.total_text())

    def unit_price_text(self) -> str:
        return self.value(self.UNIT_PRICE)

    def form_title(self) -> str:
        return self.text(self.FORM_TITLE)

    def submit_label(self) -> str:
        return self.text(self.BTN_SUBMIT)

    def is_cancel_edit_visible(self) -> bool:
        return self.is_visible(self.BTN_CANCEL_EDIT)

    def field_value(self, selector: str) -> str:
        return self.value(selector)

    def selected_payment(self) -> str:
        return "Chuyển khoản" if self.loc(self.PAY_BANK).is_checked() else "COD"
