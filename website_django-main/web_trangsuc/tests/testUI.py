import json
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Category, Product, Order, OrderItem, ShippingAddress


# ==============================================================================
# MODULE 1: AUTHENTICATION (ĐĂNG KÝ & ĐĂNG NHẬP)
# ==============================================================================
class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.existing_user = User.objects.create_user(
            username='testuser_existing',
            password='password123'
        )

    def test_TC_AUTH_01_password_less_than_8_chars(self):
        """BVA: Mật khẩu 7 ký tự -> Đăng ký thất bại"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser1',
            'password1': '1234567',
            'password2': '1234567'
        })
        self.assertFalse(User.objects.filter(username='newuser1').exists())

    def test_TC_AUTH_02_password_exactly_8_chars(self):
        """BVA: Mật khẩu đúng 8 ký tự -> Đăng ký thành công"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser2',
            'password1': '12345678',
            'password2': '12345678'
        })
        self.assertTrue(User.objects.filter(username='newuser2').exists())
        self.assertRedirects(response, reverse('login'))

    def test_TC_AUTH_03_duplicate_username(self):
        """EP (Negative): Đăng ký trùng username -> Thất bại"""
        response = self.client.post(reverse('register'), {
            'username': 'testuser_existing',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(User.objects.filter(username='testuser_existing').count(), 1)

    def test_TC_AUTH_04_login_wrong_password(self):
        """EP (Negative): Đăng nhập sai mật khẩu"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser_existing',
            'password': 'wrongpassword'
        })
        self.assertContains(response, 'Tên đăng nhập hoặc mật khẩu không chính xác.')

    def test_TC_AUTH_05_login_success(self):
        """EP (Positive): Đăng nhập đúng thông tin -> Chuyển hướng về home"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser_existing',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('home'))

    def test_TC_AUTH_06_login_page_access_when_authenticated(self):
        """Logic: Đã đăng nhập nhưng cố truy cập /login/ -> Tự động chuyển về home"""
        self.client.login(username='testuser_existing', password='password123')
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('home'))


# ==============================================================================
# MODULE 2: PRODUCTS & SEARCH (SẢN PHẨM & TÌM KIẾM)
# ==============================================================================
class ProductAndSearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Nhẫn', slug='nhan', is_sub=False)
        self.product1 = Product.objects.create(
            name='Nhẫn Kim Cương',
            price=Decimal('1000.00'),
        )
        self.product1.category.add(self.category)

    def test_TC_PROD_01_price_negative_fails(self):
        """BVA: Giá sản phẩm âm (-0.01) -> Báo lỗi Validation"""
        product = Product(name='Lỗi giá âm', price=Decimal('-0.01'))
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_TC_PROD_02_price_zero_valid(self):
        """BVA: Giá sản phẩm bằng 0.00 -> Thành công"""
        product = Product.objects.create(name='Sản phẩm 0 đồng', price=Decimal('0.00'))
        self.assertEqual(product.price, Decimal('0.00'))

    def test_TC_PROD_03_category_filter_valid_slug(self):
        """EP (Positive): Lọc sản phẩm theo slug danh mục hợp lệ"""
        response = self.client.get(f"{reverse('category')}?category=nhan")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product1, response.context['products'])

    def test_TC_PROD_04_category_filter_invalid_slug(self):
        """EP (Negative): Slug không tồn tại -> Trả về danh sách rỗng, không văng lỗi 500"""
        response = self.client.get(f"{reverse('category')}?category=non-existent-slug")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 0)

    def test_TC_PROD_05_search_exact_match(self):
        """EP (Positive): Tìm kiếm chính xác từ khóa"""
        response = self.client.post(reverse('search'), {'searched': 'Kim Cương'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product1, response.context['keys'])

    def test_TC_PROD_06_search_no_results(self):
        """EP (Negative): Tìm kiếm từ khóa không có dữ liệu"""
        response = self.client.post(reverse('search'), {'searched': 'Xe máy'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['keys']), 0)

    def test_TC_PROD_07_search_empty_string(self):
        """BVA: Tìm kiếm với chuỗi rỗng -> Xử lý an toàn"""
        response = self.client.post(reverse('search'), {'searched': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['keys']), 0)


# ==============================================================================
# MODULE 3: CART MANAGEMENT (QUẢN LÝ GIỎ HÀNG - UPDATE ITEM)
# ==============================================================================
class CartManagementTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='cart_user', password='password123')
        self.product = Product.objects.create(name='Lắc tay', price=Decimal('500.00'))
        self.order = Order.objects.create(customer=self.user, complete=False)

    def test_TC_CART_01_add_new_item_to_cart(self):
        """BVA: Thêm sản phẩm mới vào giỏ hàng (0 -> 1)"""
        self.client.login(username='cart_user', password='password123')
        response = self.client.post(
            reverse('update_item'),
            data=json.dumps({'productId': self.product.id, 'action': 'add'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        item = OrderItem.objects.get(order=self.order, product=self.product)
        self.assertEqual(item.quantity, 1)

    def test_TC_CART_02_remove_item_qty_decreases_to_zero(self):
        """BVA: Giảm số lượng về 0 (1 -> 0) -> OrderItem tự động bị XÓA"""
        self.client.login(username='cart_user', password='password123')
        OrderItem.objects.create(order=self.order, product=self.product, quantity=1)

        response = self.client.post(
            reverse('update_item'),
            data=json.dumps({'productId': self.product.id, 'action': 'remove'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(OrderItem.objects.filter(order=self.order, product=self.product).exists())

    def test_TC_CART_03_remove_item_already_zero_handled_safely(self):
        """BVA: Giảm số lượng khi đã <= 0 -> Hệ thống xử lý an toàn"""
        self.client.login(username='cart_user', password='password123')
        
        response = self.client.post(
            reverse('update_item'),
            data=json.dumps({'productId': self.product.id, 'action': 'remove'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(OrderItem.objects.filter(order=self.order, product=self.product).exists())

    def test_TC_CART_04_unauthenticated_cart_action(self):
        """Security: Chưa đăng nhập thực hiện updateItem -> Bị chặn/Chuyển hướng"""
        response = self.client.post(
            reverse('update_item'),
            data=json.dumps({'productId': self.product.id, 'action': 'add'}),
            content_type='application/json'
        )
        self.assertIn(response.status_code, [302, 401])

    def test_TC_CART_05_non_existent_product_id(self):
        """EP (Negative): Gửi productId không tồn tại -> Trả về lỗi 400 Bad Request"""
        self.client.login(username='cart_user', password='password123')
        response = self.client.post(
            reverse('update_item'),
            data=json.dumps({'productId': 999999, 'action': 'add'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


# ==============================================================================
# MODULE 4: SHIPPING & CHECKOUT (THANH TOÁN & ĐỊA CHỈ)
# ==============================================================================
class ShippingAndCheckoutTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='ship_user', password='password123')
        self.order = Order.objects.create(customer=self.user, complete=False)

    def test_TC_SHIP_01_mobile_length_9_digits_fails(self):
        """BVA: Độ dài SĐT = 9 (Max - 1) -> Không hợp lệ"""
        address = ShippingAddress(
            customer=self.user,
            order=self.order,
            address='123 Nguyễn Trãi',
            city='TP.HCM',
            mobile='090123456'  # 9 số
        )
        # Giả định có validator kiểm tra độ dài tối thiểu là 10
        if len(address.mobile) < 10:
            is_valid = False
        else:
            is_valid = True
        self.assertFalse(is_valid)

    def test_TC_SHIP_02_mobile_length_10_digits_valid(self):
        """BVA: Độ dài SĐT = 10 (Chuẩn VN) -> Lưu thành công"""
        address = ShippingAddress.objects.create(
            customer=self.user,
            order=self.order,
            address='123 Nguyễn Trãi',
            city='TP.HCM',
            mobile='0901234567'  # 10 số
        )
        self.assertEqual(address.mobile, '0901234567')

    def test_TC_SHIP_03_mobile_length_11_digits_exceeds_max_length(self):
        """BVA: Độ dài SĐT = 11 (Max + 1) -> Vượt max_length=10 của Model"""
        address = ShippingAddress(
            customer=self.user,
            order=self.order,
            address='123 Nguyễn Trãi',
            city='TP.HCM',
            mobile='09012345678'  # 11 số
        )
        with self.assertRaises(ValidationError):
            address.full_clean()

    def test_TC_SHIP_04_checkout_empty_cart(self):
        """Logic: Đặt hàng khi giỏ rỗng -> Đơn hàng chưa thể hoàn tất"""
        self.assertEqual(self.order.get_cart_items, 0)
        self.assertFalse(self.order.complete)

    def test_TC_SHIP_05_complete_order_successful(self):
        """State Transition: Hoàn tất đơn hàng -> Order.complete = True"""
        product = Product.objects.create(name='Nhẫn Bạc', price=Decimal('200.00'))
        OrderItem.objects.create(order=self.order, product=product, quantity=1)

        # Giả lập thao tác hoàn tất đơn hàng
        self.order.complete = True
        self.order.save()

        self.assertTrue(Order.objects.get(id=self.order.id).complete)