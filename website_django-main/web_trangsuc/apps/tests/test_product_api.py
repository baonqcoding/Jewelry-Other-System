"""
White-box: product_list / product_detail (apps.api_views)

product_list:
  GET  -> serialize all products
  POST -> is_valid True  -> 201
          is_valid False -> 400

product_detail:
  DoesNotExist -> 404
  GET    -> 200
  PUT    -> is_valid True  -> 200
            is_valid False -> 400
  DELETE -> 204
"""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.models import Product
from .helpers import make_category, make_product


class ProductListWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/products/"
        self.category = make_category()

    def test_get_empty_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_returns_existing_products(self):
        product = make_product(name="Bong tai")
        product.category.add(self.category)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Bong tai")

    def test_post_valid_creates_product(self):
        data = {
            "name": "Lac tay",
            "price": 500000,
            "detail": "Bac 925",
            "category": [self.category.id],
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Lac tay")
        self.assertTrue(Product.objects.filter(name="Lac tay").exists())

    def test_post_missing_price_invalid_branch(self):
        response = self.client.post(
            self.url, {"name": "Thieu gia"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Product.objects.filter(name="Thieu gia").exists())

    def test_post_negative_price_invalid_branch(self):
        """MinValueValidator(0) tren model -> serializer.is_valid() False."""
        response = self.client.post(
            self.url, {"name": "Gia am", "price": -1}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Product.objects.filter(name="Gia am").exists())

    def test_method_not_allowed(self):
        response = self.client.put(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ProductDetailWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = make_category()
        self.product = make_product()
        self.product.category.add(self.category)
        self.url = f"/api/products/{self.product.id}/"

    def test_get_existing(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.product.id)
        self.assertEqual(response.data["name"], self.product.name)

    def test_get_not_found_branch(self):
        response = self.client.get("/api/products/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Product not found")

    def test_put_valid_branch(self):
        data = {
            "name": "Nhan updated",
            "price": 2000000,
            "detail": "Moi",
            "category": [self.category.id],
        }
        response = self.client.put(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Nhan updated")
        self.assertEqual(self.product.price, 2000000)

    def test_put_invalid_branch(self):
        response = self.client.put(
            self.url, {"name": "X", "price": -10}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Nhan kim cuong")

    def test_delete_success(self):
        pk = self.product.id
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["message"], "Product deleted successfully")
        self.assertFalse(Product.objects.filter(id=pk).exists())

    def test_delete_not_found_branch(self):
        response = self.client.delete("/api/products/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Product not found")
