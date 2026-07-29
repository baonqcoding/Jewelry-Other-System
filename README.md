#  Jewelry Production Order System

Hệ thống quản lý và đặt gia công trang sức (Jewelry Production Order System) hỗ trợ kết nối và tối ưu hóa quy trình làm việc giữa Khách hàng, Nhân viên Kinh doanh, Nhân viên Thiết kế, Nhân viên Gia công và Quản trị viên.

---

##  Tính năng chính (Features)

| Feature / Group | Tính năng | Mô tả |
| :--- | :--- | :--- |
| **Khách hàng (Customer)** | Xem thông tin & Tìm kiếm | Xem thông tin công ty, bộ sưu tập trang sức có sẵn và tìm kiếm sản phẩm theo tên. |
| | Đăng ký & Tài khoản | Tạo tài khoản người dùng để sử dụng các chức năng trên hệ thống. |
| | Yêu cầu gia công | Gửi yêu cầu đặt gia công trang sức theo mẫu có sẵn hoặc theo thiết kế riêng. |
| | Nhận xét & Chỉnh sửa | Nhận xét, thêm và chỉnh sửa chi tiết yêu cầu gia công. |
| | Phê duyệt thiết kế | Phê duyệt bản vẽ thiết kế 3D do nhân viên gửi. |
| | Thanh toán & Hủy đơn | Hỗ trợ các hình thức thanh toán (trả trước, trả sau) và hủy đơn hàng khi chưa bắt đầu sản xuất. |
| **Nhân viên Kinh doanh (Sales Staff)** | Khai báo danh mục & Giá | Khai báo thông tin chi tiết sản phẩm, bảng giá vàng, giá đá áp dụng và mẫu thiết kế kèm định mức chi phí. |
| | Báo giá & Tạo đơn | Khai báo yêu cầu gia công từ khách hàng, báo giá vốn sản phẩm và tạo đơn hàng gia công. |
| | Quản lý & Giao tiếp | Cập nhật, theo dõi trạng thái đơn hàng, tạo hóa đơn và liên lạc giải đáp thắc mắc cho khách hàng. |
| **Nhân viên Thiết kế (Design Staff)** | Thiết kế bản vẽ 3D | Xem yêu cầu gia công, thực hiện thiết kế bản vẽ 3D và gửi bản thiết kế cho khách hàng. |
| | Quản lý thiết kế | Lưu trữ, quản lý các bản thiết kế và cập nhật thông tin phát triển/biểu đồ mua bán trang sức. |
| **Nhân viên Gia công (Production Staff)** | Lập kế hoạch & Vật liệu | Tiếp nhận yêu cầu, lập kế hoạch gia công, quản lý vật liệu và chi phí thực hiện. |
| | Tiến độ & Chất lượng | Cập nhật trạng thái/tiến độ sản xuất, kiểm tra chất lượng sản phẩm và báo cáo lỗi/thiếu hụt vật liệu. |
| | Bàn giao | Xác nhận hoàn thành và bàn giao sản phẩm. |
| **Quản trị viên (Admin / Manager)** | Quản trị hệ thống | Quản lý cao nhất với toàn quyền thao tác: quản lý tài khoản người dùng, sản phẩm, nhà cung cấp, cấu hình hệ thống. |
| | Quản lý đơn hàng & Báo cáo | Phê duyệt, theo dõi, xử lý thay đổi/hủy đơn hàng; xem Dashboard thống kê và tạo báo cáo tồn kho nguyên vật liệu. |
| | An toàn & Dữ liệu | Thực hiện sao lưu (backup) và phục hồi dữ liệu hệ thống. |

---

## Cấu trúc dự án (Project Structure)

```text
Jewelry-Other-System/
├── myworld/                    # Môi trường ảo Python (Virtual Environment)
│   ├── Lib/
│   ├── Scripts/
│   └── pyvenv.cfg
│
└── web_trangsuc/               # Thư mục chính của ứng dụng Django
    ├── apps/                   # App xử lý nghiệp vụ chính của hệ thống
    │   ├── static/             # Chứa tài nguyên tĩnh (CSS, JS, Images)
    │   │   ├── css/
    │   │   ├── images/
    │   │   ├── img/
    │   │   └── js/
    │   ├── templates/          # Chứa các giao diện HTML
    │   ├── __init__.py
    │   ├── admin.py            # Cấu hình giao diện Quản trị Django Admin
    │   ├── api_urls.py         # Định tuyến các đường dẫn API
    │   ├── api_views.py        # Logic xử lý API
    │   ├── apps.py             # Cấu hình App
    │   ├── models.py           # Định nghĩa cấu trúc Cơ sở dữ liệu
    │   ├── serializers.py      # Chuyển đổi dữ liệu cho API (Django REST Framework)
    │   ├── tests.py            # Viết unit test cho ứng dụng
    │   ├── urls.py             # Định tuyến đường dẫn chính của App
    │   └── views.py            # Logic xử lý giao diện/màn hình
    │
    ├── productionFiles/        # Thư mục lưu trữ tài liệu/file sản xuất
    ├── web_trangsuc/           # Cấu hình gốc dự án (settings.py, urls.py, wsgi.py)
    ├── db.sqlite3              # Cơ sở dữ liệu SQLite
    ├── Dockerfile              # Cấu hình container hóa dự án với Docker
    ├── manage.py               # Lệnh quản trị dự án Django
    └── requirements.txt        # Danh sách thư viện/gói phụ thuộc
```

---

##  Hướng dẫn cài đặt và khởi chạy dự án

### Bước 1: Tạo môi trường ảo (Virtual Environment)
Mở terminal tại thư mục gốc của dự án và chạy lệnh:
```bash
python -m venv env
```

---

### Bước 2: Kích hoạt môi trường ảo

* **Đối với Command Prompt (CMD):**
  ```cmd
  env\Scripts\activate
  ```

### Bước 3: Di chuyển vào thư mục dự án
```bash
cd web_trangsuc
```
### Bước 4: Cài đặt các thư viện cần thiết
```bash
pip install djangorestframework
pip install -r requirements.txt
```

### Bước 5: Khởi chạy dự án

```bash
# Áp dụng cơ sở dữ liệu
python manage.py migrate

# Khởi chạy server
python manage.py runserver
```
### Hoàn thành!
Nếu khởi chạy thành công, terminal sẽ hiển thị địa chỉ đường dẫn:
> **URL:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
##  Kiến trúc kỹ thuật

### Giao thức & Định dạng dữ liệu (Data Format & API)

```text
+-------------------+------------------------------------------+
| HTTP Request Header| JSON Payload (Order Info, Design Metadata)|
+-------------------+------------------------------------------+
```

Sử dụng **RESTful API** kết hợp **Django REST Framework (DRF)** với định dạng dữ liệu **JSON** để xử lý giao tiếp giữa giao diện người dùng và backend.

### Mô hình xử lý luồng công việc (Order Workflow Lifecycle)

```text
Khách hàng (Tạo yêu cầu / Đặt hàng)
├── Sales Staff     <- Khai báo giá, báo giá vốn & xác nhận đơn hàng
├── Design Staff    <- Xem yêu cầu, thiết kế bản vẽ 3D & tải lên hệ thống
├── Production Staff<- Tiếp nhận, lập kế hoạch, kiểm tra vật liệu & gia công
└── Admin / Manager <- Giám sát tiến độ, duyệt đơn hàng & tổng hợp báo cáo
```

Dữ liệu và tính toàn vẹn của đơn hàng được đảm bảo thông qua các giao dịch **Atomic Transaction** (`@transaction.atomic`) trong Django trên mọi thao tác chuyển trạng thái đơn.

---

## Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
| :--- | :--- | :--- |
| **Port 8000 đã bị chiếm** | Port 8000 đang được sử dụng bởi ứng dụng khác | Chạy lại server với port khác: `python manage.py runserver 8080` |
| **ModuleNotFoundError** | Chưa kích hoạt virtual environment hoặc chưa cài library | Chạy lệnh `env\Scripts\activate` và `pip install -r requirements.txt` |
| **OperationalError / Migration** | Cơ sở dữ liệu SQLite chưa được đồng bộ hoặc bị lỗi schema | Chạy lệnh `python manage.py makemigrations` rồi `python manage.py migrate` |
| **Lỗi PowerShell ExecutionPolicy** | Hệ thống chặn kích hoạt script môi trường ảo | Chạy `Set-ExecutionPolicy Unrestricted -Scope CurrentUser` trên PowerShell |

---

## Yêu cầu hệ thống

* **Python**: 3.10 trở lên
* **Hệ điều hành**: Windows / macOS / Linux
* **Framework & Thư viện**: `Django`, `djangorestframework`
