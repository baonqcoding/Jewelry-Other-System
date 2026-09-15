from django.test import TestCase
from django.contrib.auth.models import User
from apps.models import ShippingAddress, Order

class ShippingAddressWhiteboxTest(TestCase):
    
    def setUp(self):
        # Tạo dữ liệu giả (Fixture) trước mỗi test case
        # Tạo 1 user để test trường ForeignKey
        self.user = User.objects.create_user(username='shiptest', password='password123')
        # Tạo 1 order giả (nếu model Order yêu cầu customer, hãy truyền vào)
        self.order = Order.objects.create(customer=self.user, complete=False)

    # ==========================================
    # TEST CASE 1: Happy Path (Tạo với đầy đủ dữ liệu)
    # Mục đích: Bao phủ tất cả các trường khi có dữ liệu
    # ==========================================
    def test_create_shipping_address_full_data(self):
        address = ShippingAddress.objects.create(
            customer=self.user,
            order=self.order,
            address="123 Đường Lê Lợi",
            city="Hồ Chí Minh",
            state="Quận 1",
            mobile="0901234567"
        )
        
        # Kiểm tra dữ liệu đã lưu đúng chưa
        self.assertEqual(address.customer, self.user)
        self.assertEqual(address.order, self.order)
        self.assertEqual(address.city, "Hồ Chí Minh")
        self.assertEqual(address.mobile, "0901234567")
        # Kiểm tra date_added có được tự động thêm không (auto_now_add)
        self.assertIsNotNone(address.date_added)
        
        # Kiểm tra hàm __str__ có trả về đúng address không
        self.assertEqual(str(address), "123 Đường Lê Lợi")

    # ==========================================
    # TEST CASE 2: Null/Blank Fields (Whitebox Branch)
    # Mục đích: Bao phủ nhánh khi các trường null=True bị bỏ trống
    # ==========================================
    def test_create_shipping_address_null_fields(self):
        # Chỉ nhập address, bỏ trống tất cả các trường còn lại (vì có null=True)
        address = ShippingAddress.objects.create(
            address="Chỉ có địa chỉ"
        )
        
        # Kiểm tra các trường có thực sự là None không
        self.assertIsNone(address.customer)
        self.assertIsNone(address.order)
        self.assertIsNone(address.city)
        self.assertIsNone(address.state)
        self.assertIsNone(address.mobile)

    # ==========================================
    # TEST CASE 3: __str__ với address bị None (Edge Case)
    # Mục đích: Đảm bảo hàm __str__ không bị crash khi address=None
    # ==========================================
    def test_str_method_with_null_address(self):
        address = ShippingAddress(address=None)
        # Trong Python, str(None) sẽ trả về chuỗi "None", đây là hành vi mong đợi
        self.assertEqual(str(address), "None")

    # ==========================================
    # TEST CASE 4: Kiểm tra ràng buộc max_length (Boundary)
    # Mục đích: Đảm bảo mobile không vượt quá 10 ký tự
    # ==========================================
    def test_mobile_max_length_constraint(self):
        # Tạo đối tượng với mobile dài 11 ký tự (vượt quá max_length=10)
        address = ShippingAddress(
            address="Test Mobile",
            mobile="12345678901" # 11 ký tự
        )
        
        # full_clean() sẽ kiểm tra tất cả các ràng buộc của model
        # Mong đợi sẽ có lỗi ValidationError được ném ra
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            address.full_clean()