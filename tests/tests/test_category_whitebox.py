from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category

class CategoryWhiteBoxTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Tạo sẵn 1 category cha làm dữ liệu mẫu
        self.parent_cat = Category.objects.create(
            name="Trang sức Nam",
            slug="trang-suc-nam",
            is_sub=False
        )

    # 1. Statement & Condition Coverage: Test tạo danh mục hợp lệ
    def test_create_valid_category_statement_coverage(self):
        data = {
            "name": "Nhẫn Kim Cương",
            "slug": "nhan-kim-cuong",
            "is_sub": False,
            "sub_category": None
        }
        response = self.client.post('/api/categories/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    # 2. Branch Coverage (Nhánh `if` lỗi unique slug)
    def test_create_duplicate_slug_branch_coverage(self):
        data = {
            "name": "Trang sức Nam trùng",
            "slug": "trang-suc-nam", # Slug đã tồn tại trong setUp
            "is_sub": False
        }
        response = self.client.post('/api/categories/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 3. Branch/Condition Coverage (Nhánh sub_category hợp lệ)
    def test_create_sub_category_branch_coverage(self):
        data = {
            "name": "Nhẫn Nam",
            "slug": "nhan-nam",
            "is_sub": True,
            "sub_category": self.parent_cat.id
        }
        response = self.client.post('/api/categories/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)