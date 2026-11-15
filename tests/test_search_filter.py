"""US05 - Tìm kiếm và lọc đơn hàng."""
import pytest
from utils.data import CUSTOMERS


@pytest.fixture
def three_orders(form, orders, create_orders):
    create_orders(*CUSTOMERS)   # DH0001 An, DH0002 Bình, DH0003 Cường
    return orders


@pytest.mark.tc("TC043")
@pytest.mark.sanity
def test_search_by_name_case_insensitive(three_orders):
    three_orders.search("TRẦN")
    assert three_orders.codes() == ["DH0002"]
    three_orders.search("bình")
    assert three_orders.codes() == ["DH0002"]


@pytest.mark.tc("TC044")
def test_search_by_phone(three_orders):
    three_orders.search("0901112223")
    assert three_orders.codes() == ["DH0003"]


@pytest.mark.tc("TC045")
def test_search_by_order_code(three_orders):
    three_orders.search("dh0001")
    assert three_orders.codes() == ["DH0001"]


@pytest.mark.tc("TC046")
def test_search_no_result_shows_message(three_orders):
    three_orders.search("zzzz")
    assert three_orders.row_count() == 0
    assert three_orders.empty_message() == "Không tìm thấy đơn hàng phù hợp"
    assert three_orders.count_label() == 0


@pytest.mark.tc("TC047")
def test_clearing_search_restores_full_list(three_orders):
    three_orders.search("zzzz")
    three_orders.clear_search()
    assert three_orders.row_count() == 3


@pytest.mark.tc("TC048")
@pytest.mark.sanity
def test_filter_by_status(three_orders):
    three_orders.change_status("DH0002", "Đang giao")
    three_orders.filter_by_status("Đang giao")
    assert three_orders.codes() == ["DH0002"]
    three_orders.filter_by_status("Mới")
    assert three_orders.codes() == ["DH0001", "DH0003"]
    three_orders.filter_by_status("Tất cả trạng thái")
    assert three_orders.row_count() == 3


@pytest.mark.tc("TC049")
def test_combine_search_and_status_filter(three_orders):
    three_orders.change_status("DH0003", "Đang giao")
    three_orders.search("văn")                      # An + Cường
    three_orders.filter_by_status("Mới")
    assert three_orders.codes() == ["DH0001"]
