"""US07 - Xóa đơn hàng."""
import pytest
from utils.data import CUSTOMERS


@pytest.mark.tc("TC054")
@pytest.mark.sanity
def test_delete_order_after_confirm(form, orders, create_orders):
    create_orders(*CUSTOMERS)
    orders.click_delete("DH0002")
    assert orders.is_modal_open()
    orders.confirm_delete()
    assert not orders.is_modal_open()
    assert "DH0002" not in orders.codes()
    assert orders.count_label() == 2


@pytest.mark.tc("TC055")
def test_cancel_delete_keeps_order(form, orders, create_orders):
    create_orders(*CUSTOMERS)
    orders.click_delete("DH0002")
    orders.cancel_delete()
    assert not orders.is_modal_open()
    assert orders.codes() == ["DH0001", "DH0002", "DH0003"]


@pytest.mark.tc("TC056")
def test_delete_does_not_affect_other_orders(form, orders, create_orders):
    create_orders(*CUSTOMERS)
    orders.click_delete("DH0002")
    orders.confirm_delete()
    assert orders.codes() == ["DH0001", "DH0003"]
    assert orders.cell("DH0001", "name") == CUSTOMERS[0].name
    assert orders.cell("DH0003", "name") == CUSTOMERS[2].name


@pytest.mark.tc("TC057")
def test_deleting_last_order_shows_empty_message(form, orders, create_orders):
    create_orders(CUSTOMERS[0])
    orders.click_delete("DH0001")
    orders.confirm_delete()
    assert orders.row_count() == 0
    assert orders.empty_message() == "Chưa có đơn hàng"
