from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Product, Order, OrderItem, ShippingAddress


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Nhẫn",
            slug="nhan",
        )

    def test_create_category_success(self):
        """Kiểm tra tạo category thành công với dữ liệu hợp lệ"""
        self.assertEqual(self.category.name, "Nhẫn")
        self.assertEqual(self.category.slug, "nhan")
        self.assertFalse(self.category.is_sub)

    def test_str_returns_name(self):
        """__str__ phải trả về đúng tên category"""
        self.assertEqual(str(self.category), "Nhẫn")

    def test_slug_must_be_unique(self):
        """Slug trùng phải bị từ chối (unique=True)"""
        with self.assertRaises(Exception):
            Category.objects.create(name="Nhẫn 2", slug="nhan")

    def test_sub_category_relationship(self):
        """Kiểm tra quan hệ self-referencing (danh mục con)"""
        sub = Category.objects.create(
            name="Nhẫn cưới",
            slug="nhan-cuoi",
            sub_category=self.category,
            is_sub=True,
        )
        self.assertEqual(sub.sub_category, self.category)
        self.assertIn(sub, self.category.sub_categories.all())


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Nhẫn", slug="nhan")
        self.product = Product.objects.create(
            name="Nhẫn kim cương",
            price=5000000,
            detail="Nhẫn kim cương 18K",
        )
        self.product.category.add(self.category)

    def test_create_product_success(self):
        """Kiểm tra tạo product thành công"""
        self.assertEqual(self.product.name, "Nhẫn kim cương")
        self.assertEqual(self.product.price, 5000000)

    def test_str_returns_name(self):
        self.assertEqual(str(self.product), "Nhẫn kim cương")

    def test_product_category_relationship(self):
        """Kiểm tra quan hệ ManyToMany với Category"""
        self.assertIn(self.category, self.product.category.all())

    def test_price_boundary_zero(self):
        """Boundary value: giá = 0 vẫn phải tạo được (không có validator chặn)"""
        product = Product.objects.create(name="Sản phẩm khuyến mãi", price=0)
        self.assertEqual(product.price, 0)

    def test_price_negative_currently_allowed(self):
        """
        Model hiện KHÔNG có validator chặn giá âm.
        Test này ghi nhận hành vi hiện tại — nên bổ sung validate ở
        model hoặc serializer nếu muốn chặn giá trị âm.
        """
        product = Product.objects.create(name="Lỗi test giá âm", price=-1000)
        self.assertEqual(product.price, -1000)

    def test_image_url_property_when_no_image(self):
        """ImageURL phải trả về chuỗi rỗng khi không có ảnh"""
        self.assertEqual(self.product.ImageURL, '')


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(name="Vòng cổ", slug="vong-co")
        self.product = Product.objects.create(name="Vòng cổ bạc", price=1000000)
        self.product.category.add(self.category)
        self.order = Order.objects.create(customer=self.user)

    def test_create_order_success(self):
        """Kiểm tra tạo order thành công, mặc định complete=False"""
        self.assertEqual(self.order.customer, self.user)
        self.assertFalse(self.order.complete)

    def test_str_returns_id(self):
        self.assertEqual(str(self.order), str(self.order.id))

    def test_cart_items_empty_order(self):
        """Order chưa có OrderItem nào -> get_cart_items = 0"""
        self.assertEqual(self.order.get_cart_items, 0)

    def test_cart_total_empty_order(self):
        """Order chưa có OrderItem nào -> get_cart_total = 0"""
        self.assertEqual(self.order.get_cart_total, 0)

    def test_cart_items_and_total_with_items(self):
        """Kiểm tra tính tổng số lượng và tổng tiền khi có OrderItem"""
        OrderItem.objects.create(product=self.product, order=self.order, quantity=2)
        OrderItem.objects.create(product=self.product, order=self.order, quantity=3)

        self.assertEqual(self.order.get_cart_items, 5)
        self.assertEqual(self.order.get_cart_total, 5 * self.product.price)


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser2", password="12345")
        self.product = Product.objects.create(name="Bông tai", price=800000)
        self.order = Order.objects.create(customer=self.user)

    def test_get_total_calculation(self):
        """get_total phải bằng price * quantity"""
        item = OrderItem.objects.create(
            product=self.product, order=self.order, quantity=4
        )
        self.assertEqual(item.get_total, 800000 * 4)

    def test_get_total_boundary_quantity_zero(self):
        """Boundary value: quantity = 0 -> get_total = 0"""
        item = OrderItem.objects.create(
            product=self.product, order=self.order, quantity=0
        )
        self.assertEqual(item.get_total, 0)

    def test_default_quantity_is_zero(self):
        """Không truyền quantity -> mặc định = 0 theo model"""
        item = OrderItem.objects.create(product=self.product, order=self.order)
        self.assertEqual(item.quantity, 0)


class ShippingAddressModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser3", password="12345")
        self.order = Order.objects.create(customer=self.user)

    def test_create_shipping_address_success(self):
        address = ShippingAddress.objects.create(
            customer=self.user,
            order=self.order,
            address="123 Nguyễn Trãi",
            city="Hà Nội",
            state="Hà Nội",
            mobile="0912345678",
        )
        self.assertEqual(address.city, "Hà Nội")

    def test_str_returns_address(self):
        address = ShippingAddress.objects.create(
            customer=self.user,
            order=self.order,
            address="456 Lê Lợi",
        )
        self.assertEqual(str(address), "456 Lê Lợi")

    def test_mobile_max_length(self):
        """mobile giới hạn tối đa 10 ký tự — kiểm tra field constraint"""
        address = ShippingAddress.objects.create(
            customer=self.user,
            order=self.order,
            mobile="0912345678",  # đúng 10 ký tự
        )
        self.assertEqual(len(address.mobile), 10)