"""US02 - Kiểm tra dữ liệu đầu vào."""
import pytest
from utils.data import make_order

NAME_RANGE = "từ 2 đến 50"
PHONE_BAD = "không hợp lệ"
QTY_RANGE = "từ 1 đến 99"
ADDR_RANGE = "từ 5 đến 200"

# (trường lỗi, dữ liệu ghi đè, nội dung lỗi mong đợi)
INVALID_CASES = [
    pytest.param("customer-name", dict(name="A"), NAME_RANGE, marks=pytest.mark.tc("TC010"), id="name-1-char"),
    pytest.param("customer-name", dict(name="A" * 51), NAME_RANGE, marks=pytest.mark.tc("TC012"), id="name-51-chars"),
    pytest.param("customer-name", dict(name="   "), "Vui lòng nhập tên", marks=pytest.mark.tc("TC013"), id="name-spaces-only"),
    pytest.param("phone", dict(phone="0123abc789"), PHONE_BAD, marks=pytest.mark.tc("TC014"), id="phone-letters"),
    pytest.param("phone", dict(phone="012345678"), PHONE_BAD, marks=pytest.mark.tc("TC015"), id="phone-9-digits"),
    pytest.param("phone", dict(phone="01234567890"), PHONE_BAD, marks=pytest.mark.tc("TC016"), id="phone-11-digits"),
    pytest.param("phone", dict(phone="1234567890"), PHONE_BAD, marks=pytest.mark.tc("TC017"), id="phone-not-start-0"),
    pytest.param("email", dict(email="abc@"), "Email không hợp lệ", marks=pytest.mark.tc("TC018"), id="email-bad-format"),
    pytest.param("product", dict(product=""), "Vui lòng chọn sản phẩm", marks=pytest.mark.tc("TC019"), id="product-empty"),
    pytest.param("quantity", dict(quantity="0"), QTY_RANGE, marks=pytest.mark.tc("TC020"), id="qty-0"),
    pytest.param("quantity", dict(quantity="100"), QTY_RANGE, marks=pytest.mark.tc("TC023"), id="qty-100"),
    pytest.param("quantity", dict(quantity="-5"), QTY_RANGE, marks=pytest.mark.tc("TC024"), id="qty-negative"),
    pytest.param("quantity", dict(quantity="1.5"), QTY_RANGE, marks=pytest.mark.tc("TC025"), id="qty-decimal"),
    pytest.param("quantity", dict(quantity=""), "Vui lòng nhập số lượng", marks=pytest.mark.tc("TC026"), id="qty-empty"),
    pytest.param("address", dict(address="abcd"), ADDR_RANGE, marks=pytest.mark.tc("TC027"), id="address-4-chars"),
]


@pytest.mark.sanity
@pytest.mark.tc("TC009")
def test_submit_empty_form_shows_required_errors(form, orders):
    form.submit()
    errors = form.all_errors()
    assert "Vui lòng nhập tên" in errors["customer-name"]
    assert "Vui lòng nhập số điện thoại" in errors["phone"]
    assert "Vui lòng chọn sản phẩm" in errors["product"]
    assert "Vui lòng nhập địa chỉ" in errors["address"]
    assert errors["email"] == "", "Email không bắt buộc"
    assert orders.row_count() == 0
    assert form.message() == ""


@pytest.mark.parametrize("field, overrides, expected", INVALID_CASES)
def test_invalid_input_is_rejected(form, orders, field, overrides, expected):
    form.create_order(make_order(**overrides))
    assert expected in form.error(field), f"Lỗi hiển thị: '{form.error(field)}'"
    assert orders.row_count() == 0
    assert form.message() == ""


VALID_BOUNDARY_CASES = [
    pytest.param(dict(name="Ab"), marks=pytest.mark.tc("TC011"), id="name-2-chars"),
    pytest.param(dict(name="A" * 50), marks=pytest.mark.tc("TC031"), id="name-50-chars"),
    pytest.param(dict(quantity="1"), marks=pytest.mark.tc("TC021"), id="qty-1"),
    pytest.param(dict(quantity="99"), marks=pytest.mark.tc("TC022"), id="qty-99"),
    pytest.param(dict(address="Số 12"), marks=pytest.mark.tc("TC028"), id="address-5-chars"),
]


@pytest.mark.parametrize("overrides", VALID_BOUNDARY_CASES)
def test_boundary_values_are_accepted(form, orders, overrides):
    form.create_order(make_order(**overrides))
    assert form.message() == "Tạo đơn hàng thành công"
    assert orders.row_count() == 1


@pytest.mark.tc("TC029")
def test_script_in_name_is_not_executed(page, form, orders):
    dialogs = []
    page.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))
    payload = "<script>alert(1)</script>"
    form.create_order(make_order(name=payload))
    assert orders.cell("DH0001", "name") == payload
    assert dialogs == [], "Không được thực thi script"


@pytest.mark.tc("TC030")
def test_error_disappears_after_correcting_input(form, orders):
    form.create_order(make_order(phone="123"))
    assert PHONE_BAD in form.error("phone")
    form.set_field(form.PHONE, "0912345678")
    form.submit()
    assert form.error("phone") == ""
    assert form.message() == "Tạo đơn hàng thành công"
