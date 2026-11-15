"""US04 - Xem danh sách đơn hàng."""
import pytest
from utils.data import CUSTOMERS, make_order, money


@pytest.mark.tc("TC038")
@pytest.mark.sanity
def test_empty_list_message(form, orders):
    assert orders.row_count() == 0
    assert orders.empty_message() == "Chưa có đơn hàng"
    assert orders.count_label() == 0


@pytest.mark.tc("TC039")
def test_new_order_shows_correct_columns(form, orders):
    form.create_order(make_order(name="Lê Văn Cường", phone="0901112223",
                                 product="Màn hình 24 inch", quantity="2",
                                 payment="Chuyển khoản"))
    assert orders.cell("DH0001", "code") == "DH0001"
    assert orders.cell("DH0001", "name") == "Lê Văn Cường"
    assert orders.cell("DH0001", "phone") == "0901112223"
    assert orders.cell("DH0001", "product") == "Màn hình 24 inch"
    assert orders.cell("DH0001", "qty") == "2"
    assert orders.cell("DH0001", "total") == money(7_000_000)
    assert orders.cell("DH0001", "payment") == "Chuyển khoản"
    assert orders.empty_message() == ""


@pytest.mark.tc("TC040")
def test_order_count_matches_rows(form, orders, create_orders):
    create_orders(*CUSTOMERS)
    assert orders.row_count() == 3
    assert orders.count_label() == 3


@pytest.mark.tc("TC041")
def test_orders_listed_in_creation_order(form, orders, create_orders):
    create_orders(*CUSTOMERS)
    assert orders.codes() == ["DH0001", "DH0002", "DH0003"]
    assert [orders.cell(c, "name") for c in orders.codes()] == [c.name for c in CUSTOMERS]
