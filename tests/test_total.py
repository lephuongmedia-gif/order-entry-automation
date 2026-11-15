"""US03 - Hiển thị đơn giá và tính tổng tiền tự động."""
import pytest
from utils.data import PRICES, money


@pytest.mark.tc("TC032")
@pytest.mark.sanity
def test_unit_price_shown_after_choosing_product(form):
    form.select_product("Tai nghe")
    assert form.unit_price_text() == money(PRICES["Tai nghe"])


@pytest.mark.tc("TC033")
@pytest.mark.sanity
def test_total_equals_price_times_quantity(form):
    form.select_product("Tai nghe")
    form.set_quantity("3")
    assert form.total_text() == "2.400.000 ₫"
    assert form.total_value() == PRICES["Tai nghe"] * 3


@pytest.mark.tc("TC034")
def test_total_updates_when_quantity_changes(form):
    form.select_product("Bàn phím cơ")
    form.set_quantity("2")
    assert form.total_value() == 900_000
    form.set_quantity("4")
    assert form.total_value() == 1_800_000


@pytest.mark.tc("TC035")
def test_total_updates_when_product_changes(form):
    form.set_quantity("2")
    form.select_product("Chuột không dây")
    assert form.total_value() == 300_000
    form.select_product("Màn hình 24 inch")
    assert form.total_value() == 7_000_000


@pytest.mark.tc("TC036")
def test_total_at_max_quantity(form):
    form.select_product("Màn hình 24 inch")
    form.set_quantity("99")
    assert form.total_text() == "346.500.000 ₫"


@pytest.mark.tc("TC037")
def test_total_is_zero_when_no_product_selected(form):
    form.set_quantity("5")
    assert form.total_text() == "0 ₫"
    assert form.unit_price_text() == "0 ₫"
