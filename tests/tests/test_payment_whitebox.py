from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.models import Order

class PaymentWhiteboxTest(TestCase):
    
    def setUp(self):
        # Tạo sẵn user để dùng cho test
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.url = reverse('payment') # Giả sử tên route là 'payment' trong urls.py

    # TEST CASE 1: Bao phủ nhánh IF (Người dùng đã đăng nhập)
    def test_payment_logged_in(self):
        # Đăng nhập
        self.client.login(username='testuser', password='password123')
        
        # Gọi request
        response = self.client.get(self.url)
        
        # Kiểm tra
        self.assertEqual(response.status_code, 200)
        # Kiểm tra xem logic đã chạy đúng nhánh if chưa
        self.assertEqual(response.context['user_login'], 'show')
        self.assertEqual(response.context['user_not_login'], 'hidden')
        # Kiểm tra xem Order có được tạo ra không
        self.assertTrue(Order.objects.filter(customer=self.user, complete=False).exists())

      # TEST CASE 2: Bao phủ nhánh ELSE (Người dùng chưa đăng nhập)
    def test_payment_not_logged_in(self):
        # KHÔNG đăng nhập, gọi request trực tiếp
        response = self.client.get(self.url)
        
        # Kiểm tra xem code có chạy thành công không (status 200)
        self.assertEqual(response.status_code, 200)
        # Kiểm tra xem logic đã chạy đúng nhánh else chưa
        self.assertEqual(response.context['user_login'], 'hidden')
        self.assertEqual(response.context['user_not_login'], 'show')
        self.assertEqual(response.context['cartItems'], 0) # Giỏ hàng trống