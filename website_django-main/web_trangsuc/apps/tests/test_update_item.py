"""
White-box: updateItem (apps.views) — JSON backend, khong phai UI.

Control-flow:
  parse body -> get product -> get_or_create order/item
  if action == 'add':    quantity += 1
  elif action == 'remove': quantity -= 1
  save
  if quantity <= 0: delete item
  return JsonResponse
"""
import json

from django.test import Client, TestCase
from django.urls import reverse

from apps.models import OrderItem
from .helpers import make_order, make_order_item, make_product, make_user


class UpdateItemWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("update_item")
        self.user = make_user(username="cart_user", password="Passw0rd!")
        self.product = make_product()
        self.client.login(username="cart_user", password="Passw0rd!")

    def _post(self, product_id, action):
        return self.client.post(
            self.url,
            data=json.dumps({"productId": product_id, "action": action}),
            content_type="application/json",
        )

    def test_add_creates_item_quantity_one(self):
        """Item moi default quantity=0, nhanh add -> 1."""
        response = self._post(self.product.id, "add")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Item updated successfully")
        item = OrderItem.objects.get(product=self.product)
        self.assertEqual(item.quantity, 1)

    def test_add_increments_existing_quantity(self):
        order = make_order(self.user)
        make_order_item(order, self.product, quantity=2)
        response = self._post(self.product.id, "add")
        self.assertEqual(response.status_code, 200)
        item = OrderItem.objects.get(order=order, product=self.product)
        self.assertEqual(item.quantity, 3)

    def test_remove_decrements_quantity(self):
        """quantity 2, nhanh remove, van > 0 -> khong xoa."""
        order = make_order(self.user)
        make_order_item(order, self.product, quantity=2)
        response = self._post(self.product.id, "remove")
        self.assertEqual(response.status_code, 200)
        item = OrderItem.objects.get(order=order, product=self.product)
        self.assertEqual(item.quantity, 1)

    def test_remove_deletes_when_quantity_reaches_zero(self):
        """quantity 1, remove -> 0 -> if quantity <= 0 -> delete."""
        order = make_order(self.user)
        make_order_item(order, self.product, quantity=1)
        response = self._post(self.product.id, "remove")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            OrderItem.objects.filter(order=order, product=self.product).exists()
        )

    def test_remove_on_new_item_deletes(self):
        """get_or_create quantity=0, remove -> -1 -> delete."""
        response = self._post(self.product.id, "remove")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(OrderItem.objects.filter(product=self.product).exists())

    def test_unknown_action_returns_400(self):
        """EP invalid: action khong thuoc {add, remove} -> 400."""
        order = make_order(self.user)
        make_order_item(order, self.product, quantity=4)
        response = self._post(self.product.id, "noop")
        self.assertEqual(response.status_code, 400)
        self.assertIn("action", response.json()["error"])
        item = OrderItem.objects.get(order=order, product=self.product)
        self.assertEqual(item.quantity, 4)
