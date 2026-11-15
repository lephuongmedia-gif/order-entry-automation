# Order Entry – Playwright Automation Framework

Framework kiểm thử tự động cho website **nhập đơn hàng** (Python + Playwright + pytest), áp dụng **Page Object Model**.
Có sẵn web demo trong `demo_app/` nên clone về là chạy được ngay.

## Tính năng bắt buộc của đề bài
| Yêu cầu | Cách đáp ứng |
|---|---|
| Playwright / Selenium | Playwright (sync API) |
| Page Object Model | `pages/` – `BasePage`, `OrderFormPage`, `OrderListPage` |
| Log | `utils/logger.py` → console + `logs/test_run.log` |
| Báo cáo | `reports/report.html` (pytest-html, tự chứa ảnh) |
| Screenshot khi fail | Hook `pytest_runtest_makereport` trong `conftest.py` → `screenshots/` và nhúng vào report |
| Trace khi fail (thêm) | `reports/traces/*.zip`, mở bằng `playwright show-trace` |
| ≥ 40% automation coverage | 60/66 test case tự động hóa (xem sheet *Coverage* trong file Excel) |

## Cấu trúc
```
demo_app/        Web demo (HTML/JS) – hệ thống được test
pages/           Page Objects (locator + hành động, KHÔNG có assert)
tests/           Test scripts (assert nằm ở đây), mỗi file = 1 User Story
utils/           config, logger, test data
conftest.py      fixture (server, browser, page) + hook screenshot/log/trace khi fail
pytest.ini       cấu hình pytest + report
```
Mỗi test gắn marker `@pytest.mark.tc("TCxxx")` để đối chiếu với file test case Excel.

## Cài đặt
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

## Chạy test
```bash
pytest                              # chạy tất cả, sinh reports/report.html
pytest -m sanity                    # chỉ test sanity
pytest tests/test_validation.py     # 1 file
pytest -k "TC001 or phone"          # lọc theo tên
HEADED=1 SLOW_MO=300 pytest         # xem trình duyệt chạy (Windows PowerShell: $env:HEADED=1)
BROWSER=firefox pytest              # đổi trình duyệt (cần: playwright install firefox)
BASE_URL=https://ten-mien-cua-ban pytest   # test website thật thay vì web demo
```

## Demo screenshot khi fail
```bash
DEMO_FAIL=1 pytest tests/test_demo_failure.py
```
Kết quả: ảnh trong `screenshots/`, ảnh nhúng trong `reports/report.html`, dòng lỗi trong `logs/test_run.log`, trace trong `reports/traces/`.
Xem trace: `playwright show-trace reports/traces/<tên>.zip`

## Áp dụng cho website của nhóm
1. Sửa selector trong `pages/*.py` cho khớp website thật (chỉ sửa ở đây, test không đổi).
2. Đặt `BASE_URL`, sửa `OrderFormPage.PATH`.
3. Sửa thông báo mong đợi trong `tests/` nếu câu chữ khác.

> Lưu ý: không cài `pytest-playwright` cùng framework này vì fixture `page` / `browser` sẽ bị trùng tên.
