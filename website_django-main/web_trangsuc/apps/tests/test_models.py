"""
White-box: logic thuoc tinh/model backend (khong qua UI).

Phu __str__, ImageURL, get_cart_items, get_cart_total, get_total.
"""
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from apps.models import Product
from .helpers import (
    make_category,
    make_order,
    make_order_item,
    make_product,
    make_shipping,
    make_user,
)


class CategoryModelWhiteBoxTest(TestCase):
    def test_str_returns_name(self):
        category = make_category(name="Nhan")
        self.assertEqual(str(category), "Nhan")

    def test_sub_category_self_relation(self):
        parent = make_category(name="Cha", slug="cha")
        child = make_category(
            name="Con", slug="con", is_sub=True, sub_category=parent
        )
        self.assertEqual(child.sub_category, parent)
        self.assertIn(child, parent.sub_categories.all())

    def test_slug_unique_constraint(self):
        make_category(slug="unique-slug")
        with self.assertRaises(IntegrityError):
            make_category(name="Khac", slug="unique-slug")


class ProductModelWhiteBoxTest(TestCase):
    def test_str_returns_name(self):
        product = make_product(name="Vong bac")
        self.assertEqual(str(product), "Vong bac")

    def test_image_url_empty_when_no_image(self):
        product = make_product()
        self.assertEqual(product.ImageURL, "")

    def test_category_m2m(self):
        category = make_category()
        product = make_product()
        product.category.add(category)
        self.assertIn(category, product.category.all())
        self.assertIn(product, category.product.all())

    def test_price_zero_allowed(self):
        product = make_product(name="KM", price=0)
        product.full_clean()
        self.assertEqual(product.price, 0)

    def test_price_negative_full_clean_fails(self):
        product = Product(name="Am", price=-1)
        with self.assertRaises(ValidationError):
            product.full_clean()


class OrderModelWhiteBoxTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.product = make_product(price=100000)
        self.order = make_order(self.user)

    def test_str_returns_id(self):
        self.assertEqual(str(self.order), str(self.order.id))

    def test_cart_empty(self):
        self.assertEqual(self.order.get_cart_items, 0)
        self.assertEqual(self.order.get_cart_total, 0)

    def test_cart_with_items(self):
        make_order_item(self.order, self.product, quantity=2)
        make_order_item(self.order, make_product(name="Khac", price=50000), quantity=3)
        self.assertEqual(self.order.get_cart_items, 5)
        self.assertEqual(self.order.get_cart_total, 2 * 100000 + 3 * 50000)


class OrderItemModelWhiteBoxTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.product = make_product(price=800000)
        self.order = make_order(self.user)

    def test_get_total(self):
        item = make_order_item(self.order, self.product, quantity=4)
        self.assertEqual(item.get_total, 800000 * 4)

    def test_get_total_quantity_zero(self):
        item = make_order_item(self.order, self.product, quantity=0)
        self.assertEqual(item.get_total, 0)

    def test_default_quantity_is_zero(self):
        item = make_order_item(self.order, self.product, quantity=None)
        # helper luon truyen quantity; tao truc tiep de test default
        from apps.models import OrderItem

        OrderItem.objects.filter(id=item.id).delete()
        created = OrderItem.objects.create(order=self.order, product=self.product)
        self.assertEqual(created.quantity, 0)


class ShippingAddressModelWhiteBoxTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.order = make_order(self.user)

    def test_str_returns_address(self):
        address = make_shipping(self.user, self.order, address="456 Le Loi")
        self.assertEqual(str(address), "456 Le Loi")

    def test_mobile_max_length_full_clean(self):
        address = make_shipping(self.user, self.order, mobile="0912345678")
        self.assertEqual(len(address.mobile), 10)
        address.full_clean()
