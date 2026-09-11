"""
White-box: order_item_list / order_item_detail (apps.api_views)

order_item_list: duong thang GET -> serialize all
order_item_detail:
  DoesNotExist -> 404
  else GET 200
"""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .helpers import make_order, make_order_item, make_product, make_user


class OrderItemListWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/order-items/"

    def test_get_empty_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_returns_existing(self):
        user = make_user()
        order = make_order(user)
        product = make_product()
        item = make_order_item(order, product, quantity=3)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], item.id)
        self.assertEqual(response.data[0]["quantity"], 3)

    def test_post_not_allowed(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class OrderItemDetailWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = make_user()
        order = make_order(user)
        product = make_product()
        self.item = make_order_item(order, product, quantity=2)
        self.url = f"/api/order-items/{self.item.id}/"

    def test_get_existing(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.item.id)
        self.assertEqual(response.data["quantity"], 2)

    def test_not_found_branch(self):
        response = self.client.get("/api/order-items/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "OrderItem not found")
