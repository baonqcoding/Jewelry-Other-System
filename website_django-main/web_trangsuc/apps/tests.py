from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse


class RegisterAPIBranchTest(TestCase):

    def setUp(self):
        self.client = APIClient()


    # TC_AUTH_01
    # Branch TRUE:
    # Username đã tồn tại
    def test_register_duplicate_username(self):

        User.objects.create_user(
            username="testuser",
            password="password123"
        )

        response = self.client.post(
            reverse("register_api"),
            {
                "username": "testuser",
                "email": "test@gmail.com",
                "password": "password123",
                "first_name": "Test",
                "last_name": "User"
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.data["error"],
            "Username already exists"
        )


    # TC_AUTH_02
    # Branch FALSE:
    # Username chưa tồn tại
    def test_register_new_username(self):

        response = self.client.post(
            reverse("register_api"),
            {
                "username": "newuser",
                "email": "new@gmail.com",
                "password": "password123",
                "first_name": "New",
                "last_name": "User"
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            User.objects.filter(
                username="newuser"
            ).exists()
        )