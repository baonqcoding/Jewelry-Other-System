import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.models import Product, Order, OrderItem

class UpdateItemWhiteboxTest(TestCase):
    def setUp(self):
        # Tạo dữ liệu giả
        self.user = User.objects.create_user(username='testuser', password='123')
        self.product = Product.objects.create(name='Nhẫn Vàng', price=1000000)
        self.client = Client()
        self.client.login(username='testuser', password='123')
        self.url = reverse('update_item') # Đảm bảo tên route này đúng trong urls.py của bạn

    # Test Case 1: Hành động "add" (Thêm sản phẩm)
    def test_update_item_add(self):
        data = {'productId': self.product.id, 'action': 'add'}
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        # Kiểm tra xem OrderItem đã được tạo với quantity = 1 chưa
        order = Order.objects.get(customer=self.user, complete=False)
        order_item = OrderItem.objects.get(order=order, product=self.product)
        self.assertEqual(order_item.quantity, 1)

    # Test Case 2: Hành động "remove" khi quantity > 1
    def test_update_item_remove_more_than_one(self):
        # Tạo sẵn order item với quantity = 2
        order = Order.objects.create(customer=self.user, complete=False)
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=2)
        
        data = {'productId': self.product.id, 'action': 'remove'}
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        order_item.refresh_from_db()
        self.assertEqual(order_item.quantity, 1) # Phải giảm xuống 1

    # Test Case 3: Hành động "remove" khi quantity = 1 (Xóa sản phẩm) - Whitebox Branch
    def test_update_item_remove_to_zero(self):
        # Tạo sẵn order item với quantity = 1
        order = Order.objects.create(customer=self.user, complete=False)
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=1)
        
        data = {'productId': self.product.id, 'action': 'remove'}
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        # Kiểm tra xem OrderItem đã bị xóa khỏi DB chưa
        self.assertFalse(OrderItem.objects.filter(id=order_item.id).exists())

    # Test Case 4: Lỗi khi productId không tồn tại - Whitebox Exception
    def test_update_item_invalid_product(self):
        data = {'productId': 99999, 'action': 'add'} # ID không tồn tại
        with self.assertRaises(Product.DoesNotExist):
             self.client.post(self.url, data=json.dumps(data), content_type='application/json')