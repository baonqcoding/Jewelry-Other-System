"""
White-box tests cho Register / Login / Logout.

File chạy chính (Django discover):
  website_django-main/web_trangsuc/apps/test_auth_whitebox.py

  cd website_django-main/web_trangsuc
  python manage.py test apps.test_auth_whitebox
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class RegisterAPIWhiteBoxTest(TestCase):
    """
    register_api:
      if username exists → 400
      else create_user → 201
    """

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/register/"
        User.objects.create_user(
            username="existing_user",
            email="old@example.com",
            password="Passw0rd!",
        )

    def test_register_success_statement_coverage(self):
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
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_register_duplicate_username_branch_coverage(self):
        before = User.objects.count()
        response = self.client.post(
            self.url,
            {
                "username": "existing_user",
                "email": "dup@example.com",
                "password": "Passw0rd!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Username already exists")
        self.assertEqual(User.objects.count(), before)


class LoginAPIWhiteBoxTest(TestCase):
    """
    login_api:
      authenticate OK → 200
      authenticate None → 401
    """

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/login/"
        User.objects.create_user(username="login_user", password="Passw0rd!")

    def test_login_success_branch_true(self):
        response = self.client.post(
            self.url,
            {"username": "login_user", "password": "Passw0rd!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Login successful")

    def test_login_wrong_password_branch_false(self):
        response = self.client.post(
            self.url,
            {"username": "login_user", "password": "wrong"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_unknown_user_branch_false(self):
        response = self.client.post(
            self.url,
            {"username": "ghost", "password": "Passw0rd!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutAPIWhiteBoxTest(TestCase):
    """logout_api: đường thẳng → luôn 200."""

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/logout/"
        User.objects.create_user(username="logout_user", password="Passw0rd!")

    def test_logout_when_authenticated_statement_coverage(self):
        self.client.login(username="logout_user", password="Passw0rd!")
        response = self.client.post(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logout successful")

    def test_logout_when_anonymous_statement_coverage(self):
        response = self.client.post(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RegisterViewWhiteBoxTest(TestCase):
    """
    register view:
      POST valid → redirect login
      POST invalid → render lại
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse("register")
        User.objects.create_user(username="taken", password="Passw0rd!")

    def _valid_payload(self, username="fresh_user"):
        return {
            "username": username,
            "email": f"{username}@example.com",
            "first_name": "Van",
            "last_name": "A",
            "password1": "ComplexPass1!",
            "password2": "ComplexPass1!",
        }

    def test_register_get_renders_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register_post_valid_branch(self):
        response = self.client.post(self.url, self._valid_payload())
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="fresh_user").exists())

    def test_register_post_password_mismatch_invalid_branch(self):
        data = self._valid_payload("mismatch_user")
        data["password2"] = "DifferentPass1!"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="mismatch_user").exists())

    def test_register_post_duplicate_username_invalid_branch(self):
        response = self.client.post(self.url, self._valid_payload("taken"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username="taken").count(), 1)


class LoginViewWhiteBoxTest(TestCase):
    """
    loginPage:
      authenticated → redirect home
      POST OK → redirect home
      POST fail → render + message
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse("login")
        self.user = User.objects.create_user(username="web_login", password="Passw0rd!")

    def test_login_get_anonymous_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_get_when_authenticated_redirects_home(self):
        self.client.login(username="web_login", password="Passw0rd!")
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("home"))

    def test_login_post_success_branch(self):
        response = self.client.post(
            self.url, {"username": "web_login", "password": "Passw0rd!"}
        )
        self.assertRedirects(response, reverse("home"))

    def test_login_post_wrong_password_branch(self):
        response = self.client.post(
            self.url, {"username": "web_login", "password": "bad"}
        )
        self.assertEqual(response.status_code, 200)
        messages = list(response.context["messages"])
        self.assertTrue(any("Invalid username or password." in str(m) for m in messages))


class LogoutViewWhiteBoxTest(TestCase):
    """logoutPage: logout → redirect login."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("logout")
        User.objects.create_user(username="web_logout", password="Passw0rd!")

    def test_logout_clears_session_and_redirects(self):
        self.client.login(username="web_logout", password="Passw0rd!")
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_when_anonymous_still_redirects(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("login"))
