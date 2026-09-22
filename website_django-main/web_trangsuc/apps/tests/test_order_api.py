"""
White-box: order_list / order_detail (apps.api_views)

order_list:
  GET  -> all orders
  POST -> is_valid True  -> 201
          is_valid False -> 400

order_detail:
  DoesNotExist -> 404
  GET / PUT valid / PUT invalid / DELETE
"""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.models import Order
from .helpers import make_order, make_user


class OrderListWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/orders/"
        self.user = make_user()

    def test_get_empty_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_returns_existing(self):
        order = make_order(self.user, transaction_id="TX-1")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], order.id)
        self.assertEqual(response.data[0]["transaction_id"], "TX-1")

    def test_post_valid_creates_order(self):
        data = {
            "customer": self.user.id,
            "complete": False,
            "transaction_id": "TX-NEW",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(response.data["transaction_id"], "TX-NEW")

    def test_post_invalid_customer_branch(self):
        response = self.client.post(
            self.url, {"customer": 99999, "complete": False}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)


class OrderDetailWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        self.order = make_order(self.user, transaction_id="TX-OLD")
        self.url = f"/api/orders/{self.order.id}/"

    def test_get_existing(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["transaction_id"], "TX-OLD")

    def test_not_found_branch(self):
        response = self.client.get("/api/orders/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Order not found")

    def test_put_valid_branch(self):
        data = {
            "customer": self.user.id,
            "complete": True,
            "transaction_id": "TX-DONE",
        }
        response = self.client.put(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertTrue(self.order.complete)
        self.assertEqual(self.order.transaction_id, "TX-DONE")

    def test_put_invalid_branch(self):
        response = self.client.put(
            self.url,
            {"customer": 99999, "complete": True, "transaction_id": "X"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.order.refresh_from_db()
        self.assertFalse(self.order.complete)

    def test_delete_success(self):
        pk = self.order.id
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["message"], "Order deleted successfully")
        self.assertFalse(Order.objects.filter(id=pk).exists())

    def test_delete_not_found_branch(self):
        response = self.client.delete("/api/orders/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
