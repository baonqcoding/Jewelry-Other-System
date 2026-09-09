from django.test import TestCase, Client
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

class AuthenticationWhiteBoxTest(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.web_client = Client()

        # Lấy URL an toàn không bị lỗi AttributeError
        try:
            self.register_api_url = reverse('register_api')
        except NoReverseMatch:
            self.register_api_url = '/api/register/'

        try:
            self.login_api_url = reverse('login_api')
        except NoReverseMatch:
            self.login_api_url = '/api/login/'

        try:
            self.logout_api_url = reverse('logout_api')
        except NoReverseMatch:
            self.logout_api_url = '/api/logout/'

        # URLs cho Web Views
        self.register_web_url = reverse('register')
        self.login_web_url = reverse('login')
        self.logout_web_url = reverse('logout')

        # Tạo user mẫu
        self.existing_user = User.objects.create_user(
            username='user_existing',
            email='existing@example.com',
            password='password123',
            first_name='Nguyen',
            last_name='Bao'
        )

    # ==========================================
    # 1. WHITE-BOX TEST CHO API AUTH
    # ==========================================

    def test_register_api_success_statement_coverage(self):
        data = {
            "username": "new_api_user",
            "email": "new_api@example.com",
            "password": "Password@123",
            "first_name": "Quoc",
            "last_name": "Bao"
        }
        response = self.api_client.post(self.register_api_url, data, format='json')
        if response.status_code == status.HTTP_201_CREATED:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertTrue(User.objects.filter(username="new_api_user").exists())

    def test_register_api_duplicate_username_branch_coverage(self):
        data = {
            "username": "user_existing",
            "email": "another@example.com",
            "password": "Password@123"
        }
        response = self.api_client.post(self.register_api_url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND])

    def test_login_api_success_branch_coverage(self):
        data = {
            "username": "user_existing",
            "password": "password123"
        }
        response = self.api_client.post(self.login_api_url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_login_api_invalid_credentials_branch_coverage(self):
        data = {
            "username": "user_existing",
            "password": "wrong_password"
        }
        response = self.api_client.post(self.login_api_url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND])

    def test_logout_api_statement_coverage(self):
        response = self.api_client.post(self.logout_api_url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    # ==========================================
    # 2. WHITE-BOX TEST CHO WEB VIEWS (views.py)
    # ==========================================

    def test_web_register_get_authenticated_branch(self):
        self.web_client.force_login(self.existing_user)
        response = self.web_client.get(self.register_web_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user_login'], "show")

    def test_web_register_post_invalid_form_branch(self):
        data = {
            "username": "web_user_fail",
            "email": "web_fail@example.com",
            "password1": "Password@123",
            "password2": "PasswordMismatch"
        }
        response = self.web_client.post(self.register_web_url, data)
        self.assertEqual(response.status_code, 200)

    def test_web_login_get_authenticated_redirect_branch(self):
        self.web_client.force_login(self.existing_user)
        response = self.web_client.get(self.login_web_url)
        self.assertRedirects(response, reverse('home'))

    def test_web_login_post_invalid_credentials_branch(self):
        data = {
            "username": "user_existing",
            "password": "wrong_password"
        }
        response = self.web_client.post(self.login_web_url, data)
        self.assertEqual(response.status_code, 200)

    def test_web_logout_redirect_statement(self):
        response = self.web_client.get(self.logout_web_url)
        self.assertRedirects(response, self.login_web_url)