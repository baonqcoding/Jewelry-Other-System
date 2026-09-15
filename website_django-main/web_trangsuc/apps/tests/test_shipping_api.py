"""
White-box: shipping_address_list / shipping_address_detail (apps.api_views)

list:
  GET  -> all addresses
  POST -> is_valid True  -> 201
          is_valid False -> 400

detail:
  DoesNotExist -> 404
  GET / PUT valid / PUT invalid / DELETE
"""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.models import ShippingAddress
from .helpers import make_order, make_shipping, make_user


class ShippingAddressListWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/shipping-addresses/"
        self.user = make_user()
        self.order = make_order(self.user)

    def test_get_empty_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_returns_existing(self):
        make_shipping(self.user, self.order, city="Da Nang")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["city"], "Da Nang")

    def test_post_valid_creates_address(self):
        data = {
            "customer": self.user.id,
            "order": self.order.id,
            "address": "456 Le Loi",
            "city": "HCM",
            "state": "HCM",
            "mobile": "0987654321",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShippingAddress.objects.count(), 1)
        self.assertEqual(response.data["mobile"], "0987654321")

    def test_post_invalid_order_branch(self):
        response = self.client.post(
            self.url,
            {
                "customer": self.user.id,
                "order": 99999,
                "address": "X",
                "city": "Y",
                "mobile": "0912345678",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ShippingAddress.objects.count(), 0)

    def test_post_mobile_over_max_length_invalid_branch(self):
        """mobile max_length=10 -> 11 ky tu fail serializer."""
        response = self.client.post(
            self.url,
            {
                "customer": self.user.id,
                "order": self.order.id,
                "address": "X",
                "city": "Y",
                "mobile": "09123456789",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ShippingAddressDetailWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        self.order = make_order(self.user)
        self.address = make_shipping(self.user, self.order)
        self.url = f"/api/shipping-addresses/{self.address.id}/"

    def test_get_existing(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["address"], "123 Nguyen Trai")

    def test_not_found_branch(self):
        response = self.client.get("/api/shipping-addresses/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Shipping address not found")

    def test_put_valid_branch(self):
        data = {
            "customer": self.user.id,
            "order": self.order.id,
            "address": "789 Tran Hung Dao",
            "city": "Hue",
            "state": "Hue",
            "mobile": "0900000000",
        }
        response = self.client.put(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.address.refresh_from_db()
        self.assertEqual(self.address.city, "Hue")
        self.assertEqual(self.address.mobile, "0900000000")

    def test_put_invalid_branch(self):
        response = self.client.put(
            self.url,
            {
                "customer": 99999,
                "order": self.order.id,
                "address": "X",
                "city": "Y",
                "mobile": "0912345678",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.address.refresh_from_db()
        self.assertEqual(self.address.city, "Ha Noi")

    def test_delete_success(self):
        pk = self.address.id
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            response.data["message"], "Shipping address deleted successfully"
        )
        self.assertFalse(ShippingAddress.objects.filter(id=pk).exists())

    def test_delete_not_found_branch(self):
        response = self.client.delete("/api/shipping-addresses/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
