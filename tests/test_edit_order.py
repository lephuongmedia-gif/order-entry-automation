"""US06 - Sửa đơn hàng."""
import pytest
from utils.data import make_order


@pytest.fixture
def one_order(form, orders):
    form.create_order(make_order())
    return orders


@pytest.mark.tc("TC050")
@pytest.mark.sanity
def test_edit_loads_order_into_form(form, one_order):
    one_order.click_edit("DH0001")
    assert form.form_title() == "Sửa đơn hàng DH0001"
    assert form.submit_label() == "Cập nhật đơn hàng"
    assert form.is_cancel_edit_visible()
    assert form.field_value(form.NAME) == "Nguyễn Văn An"
    assert form.field_value(form.PHONE) == "0912345678"
    assert form.field_value(form.QUANTITY) == "1"
    assert form.field_value(form.ADDRESS) == "12 Lê Lợi, Hải Phòng"
    assert form.total_text() == "800.000 ₫"


@pytest.mark.tc("TC051")
@pytest.mark.sanity
def test_update_order_keeps_code_and_status(form, one_order):
    one_order.change_status("DH0001", "Đang giao")
    one_order.click_edit("DH0001")
    form.set_quantity("3")
    form.submit()
    assert form.message() == "Cập nhật đơn hàng thành công"
    assert one_order.codes() == ["DH0001"]
    assert one_order.cell("DH0001", "qty") == "3"
    assert one_order.cell("DH0001", "total") == "2.400.000 ₫"
    assert one_order.status_of("DH0001") == "Đang giao"
    assert form.form_title() == "Tạo đơn hàng mới"


@pytest.mark.tc("TC052")
def test_update_with_invalid_data_is_rejected(form, one_order):
    one_order.click_edit("DH0001")
    form.set_field(form.PHONE, "123")
    form.submit()
    assert "không hợp lệ" in form.error("phone")
    assert one_order.cell("DH0001", "phone") == "0912345678"
    assert form.form_title() == "Sửa đơn hàng DH0001"


@pytest.mark.tc("TC053")
def test_cancel_edit_returns_to_create_mode(form, one_order):
    one_order.click_edit("DH0001")
    form.set_field(form.NAME, "Tên khác")
    form.cancel_edit()
    assert form.form_title() == "Tạo đơn hàng mới"
    assert form.submit_label() == "Tạo đơn hàng"
    assert form.field_value(form.NAME) == ""
    assert one_order.cell("DH0001", "name") == "Nguyễn Văn An"
