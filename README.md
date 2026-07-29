

**Tính năng **
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

**Cấu trúc dự án**

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
```
