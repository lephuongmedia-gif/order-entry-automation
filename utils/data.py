"""Dữ liệu test và hàm tiện ích."""
import re
from dataclasses import dataclass, replace

PRICES = {
    "Chuột không dây": 150_000,
    "Bàn phím cơ": 450_000,
    "Tai nghe": 800_000,
    "Màn hình 24 inch": 3_500_000,
}


@dataclass
class Order:
    name: str = "Nguyễn Văn An"
    phone: str = "0912345678"
    email: str = "an.nguyen@example.com"
    product: str = "Tai nghe"
    quantity: str = "1"
    address: str = "12 Lê Lợi, Hải Phòng"
    payment: str = "COD"          # COD | Chuyển khoản
    note: str = "Giao giờ hành chính"


def make_order(**overrides) -> Order:
    """Tạo đơn hợp lệ, ghi đè các trường cần thay đổi."""
    return replace(Order(), **overrides)


# 3 khách hàng mẫu dùng cho test tìm kiếm / lọc / xóa
CUSTOMERS = [
    make_order(),
    make_order(name="Trần Thị Bình", phone="0987654321", product="Bàn phím cơ", quantity="2"),
    make_order(name="Lê Văn Cường", phone="0901112223", product="Màn hình 24 inch", payment="Chuyển khoản"),
]


def money(amount: int) -> str:
    """1050000 -> '1.050.000 ₫' (đúng định dạng hiển thị của web)."""
    return f"{amount:,}".replace(",", ".") + " ₫"


def to_int(text: str) -> int:
    """'1.050.000 ₫' -> 1050000"""
    digits = re.sub(r"\D", "", text)
    return int(digits) if digits else 0
