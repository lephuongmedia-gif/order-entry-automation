"""US08 - Cập nhật trạng thái đơn hàng."""
import pytest
from utils.data import make_order


@pytest.mark.tc("TC058")
@pytest.mark.sanity
def test_new_order_has_status_new(form, orders):
    form.create_order(make_order())
    assert orders.status_of("DH0001") == "Mới"


@pytest.mark.tc("TC059")
def test_change_status_to_shipping(form, orders):
    form.create_order(make_order())
    orders.change_status("DH0001", "Đang giao")
    assert orders.status_of("DH0001") == "Đang giao"


@pytest.mark.tc("TC060")
def test_change_status_to_done(form, orders):
    form.create_order(make_order())
    orders.change_status("DH0001", "Đang giao")
    orders.change_status("DH0001", "Hoàn thành")
    assert orders.status_of("DH0001") == "Hoàn thành"


@pytest.mark.tc("TC061")
def test_status_persists_after_reload(form, orders):
    form.create_order(make_order())
    orders.change_status("DH0001", "Hoàn thành")
    form.reload()
    assert orders.status_of("DH0001") == "Hoàn thành"
