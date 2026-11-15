"""US01 - Tạo đơn hàng mới."""
import pytest
from utils.data import make_order, money, PRICES


@pytest.mark.tc("TC001")
@pytest.mark.sanity
def test_create_order_with_full_info(form, orders):
    form.create_order(make_order(quantity="2"))
    assert form.message() == "Tạo đơn hàng thành công"
    assert orders.codes() == ["DH0001"]
    assert orders.cell("DH0001", "name") == "Nguyễn Văn An"
    assert orders.cell("DH0001", "phone") == "0912345678"
    assert orders.cell("DH0001", "product") == "Tai nghe"
    assert orders.cell("DH0001", "qty") == "2"
    assert orders.cell("DH0001", "total") == money(PRICES["Tai nghe"] * 2)
    assert orders.cell("DH0001", "payment") == "COD"
    assert orders.status_of("DH0001") == "Mới"


@pytest.mark.tc("TC002")
@pytest.mark.sanity
def test_create_order_required_fields_only(form, orders):
    form.create_order(make_order(email="", note=""))
    assert form.message() == "Tạo đơn hàng thành công"
    assert orders.row_count() == 1


@pytest.mark.tc("TC003")
def test_order_code_auto_increments(form, orders, create_orders):
    create_orders(make_order(), make_order(name="Trần Thị Bình"))
    assert orders.codes() == ["DH0001", "DH0002"]


@pytest.mark.tc("TC004")
def test_form_is_cleared_after_create(form, orders):
    form.create_order(make_order(payment="Chuyển khoản", quantity="5"))
    assert form.field_value(form.NAME) == ""
    assert form.field_value(form.PHONE) == ""
    assert form.field_value(form.ADDRESS) == ""
    assert form.field_value(form.QUANTITY) == "1"
    assert form.selected_payment() == "COD"
    assert form.total_text() == "0 ₫"


@pytest.mark.tc("TC005")
def test_create_order_with_bank_transfer(form, orders):
    form.create_order(make_order(payment="Chuyển khoản"))
    assert orders.cell("DH0001", "payment") == "Chuyển khoản"


@pytest.mark.tc("TC006")
def test_reset_button_clears_form(form):
    form.fill_order(make_order(quantity="7", payment="Chuyển khoản"))
    form.reset()
    assert form.field_value(form.NAME) == ""
    assert form.field_value(form.PHONE) == ""
    assert form.field_value(form.EMAIL) == ""
    assert form.field_value(form.QUANTITY) == "1"
    assert form.selected_payment() == "COD"
    assert form.total_text() == "0 ₫"


@pytest.mark.tc("TC007")
def test_order_persists_after_reload(form, orders):
    form.create_order(make_order())
    form.reload()
    assert orders.codes() == ["DH0001"]
    assert orders.cell("DH0001", "name") == "Nguyễn Văn An"


@pytest.mark.tc("TC008")
def test_create_order_with_vietnamese_unicode_name(form, orders):
    form.create_order(make_order(name="Trần Thị Bích Ngọc"))
    assert orders.cell("DH0001", "name") == "Trần Thị Bích Ngọc"
