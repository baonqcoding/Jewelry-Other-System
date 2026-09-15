"""
White-box: register_api / login_api / logout_api (apps.api_views)

register_api:
  username exists -> 400
  else create_user -> 201

login_api:
  authenticate not None -> 200
  else -> 401

logout_api: duong thang -> 200
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from .helpers import make_user


class RegisterAPIWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/register/"
        make_user(username="existing_user")

    def test_register_success_branch(self):
        data = {
            "username": "new_user",
            "email": "new@example.com",
            "password": "Passw0rd!",
            "first_name": "An",
            "last_name": "Nguyen",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "new_user")
        self.assertEqual(response.data["email"], "new@example.com")
        self.assertEqual(response.data["first_name"], "An")
        self.assertEqual(response.data["last_name"], "Nguyen")
        self.assertNotIn("password", response.data)
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_register_duplicate_username_branch(self):
        before = User.objects.count()
        response = self.client.post(
            self.url,
            {
                "username": "existing_user",
                "email": "dup@example.com",
                "password": "Passw0rd!",
                "first_name": "X",
                "last_name": "Y",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Username already exists")
        self.assertEqual(User.objects.count(), before)

    def test_get_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class LoginAPIWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/login/"
        self.user = make_user(username="login_user", password="Passw0rd!")

    def test_login_success_branch(self):
        response = self.client.post(
            self.url,
            {"username": "login_user", "password": "Passw0rd!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Login successful")
        self.assertEqual(response.data["user"]["username"], "login_user")
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_wrong_password_branch(self):
        response = self.client.post(
            self.url,
            {"username": "login_user", "password": "sai-mat-khau"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid username or password")

    def test_login_unknown_user_branch(self):
        response = self.client.post(
            self.url,
            {"username": "ghost", "password": "Passw0rd!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid username or password")


class LogoutAPIWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/logout/"
        make_user(username="logout_user", password="Passw0rd!")

    def test_logout_when_authenticated(self):
        self.client.login(username="logout_user", password="Passw0rd!")
        response = self.client.post(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logout successful")

    def test_logout_when_anonymous(self):
        response = self.client.post(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logout successful")
