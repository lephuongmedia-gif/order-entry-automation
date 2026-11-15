"""Test cố ý FAIL để trình diễn log + screenshot + report + trace.
Chỉ chạy khi đặt biến môi trường DEMO_FAIL=1.

    DEMO_FAIL=1 pytest tests/test_demo_failure.py
"""
import os
import pytest
from utils.data import make_order

pytestmark = pytest.mark.skipif(os.getenv("DEMO_FAIL") != "1",
                                reason="Đặt DEMO_FAIL=1 để chạy test demo lỗi")


def test_intentional_failure_for_demo(form, orders):
    form.create_order(make_order())
    assert orders.cell("DH0001", "total") == "999 ₫", "Cố ý sai để demo screenshot khi fail"
