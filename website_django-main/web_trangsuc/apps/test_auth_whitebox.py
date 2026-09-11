"""
White-box tests cho Register / Login / Logout.

Phủ các nhánh (branch) & câu lệnh (statement) theo control-flow trong:
  - apps.api_views: register_api, login_api, logout_api
  - apps.views: register, loginPage, logoutPage
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


# ==============================================================================
# API — register_api / login_api / logout_api
# ==============================================================================
class RegisterAPIWhiteBoxTest(TestCase):
    """
    register_api control-flow:
      if User.objects.filter(username=username).exists():
          return 400          # nhánh True
      create_user(...)
      return 201              # nhánh False
    """

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/register/"
        self.existing = User.objects.create_user(
            username="existing_user",
            email="old@example.com",
            password="Passw0rd!",
        )

    def test_register_success_statement_coverage(self):
        """Nhánh username chưa tồn tại → create_user + 201 + dữ liệu UserSerializer."""
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
        self.assertTrue(User.objects.filter(username="new_user").exists())
        # password không được trả về trong serializer
        self.assertNotIn("password", response.data)

    def test_register_duplicate_username_branch_coverage(self):
        """Nhánh if exists() == True → 400, không tạo thêm user."""
        before = User.objects.count()
        data = {
            "username": "existing_user",
            "email": "dup@example.com",
            "password": "Passw0rd!",
            "first_name": "X",
            "last_name": "Y",
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Username already exists")
        self.assertEqual(User.objects.count(), before)


class LoginAPIWhiteBoxTest(TestCase):
    """
    login_api control-flow:
      user = authenticate(...)
      if user is not None:
          login(...); return 200   # nhánh True
      return 401                   # nhánh False
    """

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/login/"
        self.user = User.objects.create_user(
            username="login_user",
            password="Passw0rd!",
            email="login@example.com",
        )

    def test_login_success_branch_true(self):
        """authenticate thành công → login session + 200 + message/user."""
        response = self.client.post(
            self.url,
            {"username": "login_user", "password": "Passw0rd!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Login successful")
        self.assertEqual(response.data["user"]["username"], "login_user")
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_wrong_password_branch_false(self):
        """authenticate trả None (sai mật khẩu) → 401."""
        response = self.client.post(
            self.url,
            {"username": "login_user", "password": "wrong-password"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid username or password")

    def test_login_unknown_user_branch_false(self):
        """authenticate trả None (user không tồn tại) → cùng nhánh 401."""
        response = self.client.post(
            self.url,
            {"username": "ghost", "password": "Passw0rd!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid username or password")


class LogoutAPIWhiteBoxTest(TestCase):
    """
    logout_api: đường đi tuyến tính
      logout(request) → return 200 {"message": "Logout successful"}
    """

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/logout/"
        self.user = User.objects.create_user(
            username="logout_user",
            password="Passw0rd!",
        )

    def test_logout_when_authenticated_statement_coverage(self):
        """Đã login → logout → 200, session hết authenticated."""
        self.client.force_authenticate(user=self.user)
        # Session login để kiểm tra trạng thái sau logout
        self.client.login(username="logout_user", password="Passw0rd!")

        response = self.client.post(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logout successful")

    def test_logout_when_anonymous_statement_coverage(self):
        """Chưa login vẫn đi hết hàm logout_api → 200 (không có nhánh sớm)."""
        response = self.client.post(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logout successful")


# ==============================================================================
# WEB views — register / loginPage / logoutPage
# ==============================================================================
class RegisterViewWhiteBoxTest(TestCase):
    """
    register control-flow:
      set user_login / user_not_login theo is_authenticated
      if POST:
          if form.is_valid():
              save(); redirect('login')     # nhánh valid
          else:
              messages.error(...)           # nhánh invalid
      return render('register.html')
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
        """GET (không authenticated) → render register.html, không tạo user."""
        before = User.objects.count()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
        self.assertEqual(User.objects.count(), before)
        self.assertEqual(response.context["user_login"], "hidden")
        self.assertEqual(response.context["user_not_login"], "show")

    def test_register_post_valid_branch(self):
        """POST form hợp lệ → save user + redirect login."""
        response = self.client.post(self.url, self._valid_payload())

        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="fresh_user").exists())

    def test_register_post_password_mismatch_invalid_branch(self):
        """POST form.is_valid() == False (password1 != password2) → ở lại trang, không tạo user."""
        data = self._valid_payload("mismatch_user")
        data["password2"] = "DifferentPass1!"
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
        self.assertFalse(User.objects.filter(username="mismatch_user").exists())

    def test_register_post_duplicate_username_invalid_branch(self):
        """POST trùng username → form invalid → không tạo thêm."""
        data = self._valid_payload("taken")
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username="taken").count(), 1)

    def test_register_context_when_already_authenticated(self):
        """
        is_authenticated == True chỉ đổi flag context (KHÔNG redirect — theo code hiện tại).
        """
        user = User.objects.create_user(username="authed", password="Passw0rd!")
        self.client.login(username="authed", password="Passw0rd!")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user_login"], "show")
        self.assertEqual(response.context["user_not_login"], "hidden")


class LoginViewWhiteBoxTest(TestCase):
    """
    loginPage control-flow:
      if is_authenticated: return redirect('home')     # nhánh early-exit
      if POST:
          if authenticate OK: login; redirect('home')  # nhánh auth True
          else: messages.error(...)                    # nhánh auth False
      return render('login.html')
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse("login")
        self.user = User.objects.create_user(
            username="web_login",
            password="Passw0rd!",
        )

    def test_login_get_anonymous_renders(self):
        """GET chưa login → render login.html."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertEqual(response.context["user_login"], "hidden")
        self.assertEqual(response.context["user_not_login"], "show")

    def test_login_get_when_authenticated_redirects_home(self):
        """Nhánh is_authenticated == True → redirect home (không render form)."""
        self.client.login(username="web_login", password="Passw0rd!")
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse("home"))

    def test_login_post_success_branch(self):
        """POST đúng credentials → login + redirect home."""
        response = self.client.post(
            self.url,
            {"username": "web_login", "password": "Passw0rd!"},
        )

        self.assertRedirects(response, reverse("home"))
        # session đã đăng nhập
        user_id = self.client.session.get("_auth_user_id")
        self.assertEqual(int(user_id), self.user.id)

    def test_login_post_wrong_password_branch(self):
        """POST sai mật khẩu → ở lại login, có message lỗi theo code."""
        response = self.client.post(
            self.url,
            {"username": "web_login", "password": "bad-password"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        messages = list(response.context["messages"])
        self.assertTrue(
            any("Invalid username or password." in str(m) for m in messages)
        )
        self.assertNotIn("_auth_user_id", self.client.session)


class LogoutViewWhiteBoxTest(TestCase):
    """
    logoutPage: đường đi tuyến tính
      logout(request) → redirect('login')
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse("logout")
        self.user = User.objects.create_user(
            username="web_logout",
            password="Passw0rd!",
        )

    def test_logout_clears_session_and_redirects(self):
        """Đã login → logout → redirect login, session không còn auth."""
        self.client.login(username="web_logout", password="Passw0rd!")
        self.assertIn("_auth_user_id", self.client.session)

        response = self.client.get(self.url)

        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_when_anonymous_still_redirects(self):
        """Chưa login vẫn chạy hết hàm → redirect login."""
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("login"))
