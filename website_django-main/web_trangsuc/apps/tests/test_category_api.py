"""
White-box: category_list / category_detail (apps.api_views)

category_list:
  GET  -> all categories
  POST -> is_valid True  -> 201
          is_valid False -> 400 (thieu slug / slug trung)

category_detail:
  DoesNotExist -> 404
  GET / PUT valid / PUT invalid / DELETE
"""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.models import Category
from .helpers import make_category


class CategoryListWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/categories/"

    def test_get_empty_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_returns_existing(self):
        make_category(name="Vong co", slug="vong-co")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["slug"], "vong-co")

    def test_post_valid_creates_category(self):
        data = {
            "name": "Nhan Kim Cuong",
            "slug": "nhan-kim-cuong",
            "is_sub": False,
            "sub_category": None,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)

    def test_post_sub_category_branch(self):
        parent = make_category(name="Trang suc Nam", slug="trang-suc-nam")
        data = {
            "name": "Nhan Nam",
            "slug": "nhan-nam",
            "is_sub": True,
            "sub_category": parent.id,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        child = Category.objects.get(slug="nhan-nam")
        self.assertTrue(child.is_sub)
        self.assertEqual(child.sub_category_id, parent.id)

    def test_post_missing_slug_invalid_branch(self):
        response = self.client.post(
            self.url, {"name": "Thieu slug", "is_sub": False}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_duplicate_slug_invalid_branch(self):
        make_category(slug="trung-slug")
        response = self.client.post(
            self.url,
            {"name": "Khac ten", "slug": "trung-slug", "is_sub": False},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.filter(slug="trung-slug").count(), 1)


class CategoryDetailWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = make_category()
        self.url = f"/api/categories/{self.category.id}/"

    def test_get_existing(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["slug"], "nhan")

    def test_not_found_branch(self):
        response = self.client.get("/api/categories/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Category not found")

    def test_put_valid_branch(self):
        data = {
            "name": "Nhan updated",
            "slug": "nhan-updated",
            "is_sub": False,
            "sub_category": None,
        }
        response = self.client.put(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.slug, "nhan-updated")

    def test_put_invalid_branch(self):
        other = make_category(name="Khac", slug="khac")
        response = self.client.put(
            self.url,
            {
                "name": "Trung slug",
                "slug": other.slug,
                "is_sub": False,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_success(self):
        pk = self.category.id
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["message"], "Category deleted successfully")
        self.assertFalse(Category.objects.filter(id=pk).exists())

    def test_delete_not_found_branch(self):
        response = self.client.delete("/api/categories/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
