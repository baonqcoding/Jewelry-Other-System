"""
Unit tests cho ham kiem tra logic bounds (auth_bounds + domain_bounds).

Tap trung BVA: min-1, min, max, max+1 va mot so lop EP (charset/format).
Khong can DB.
"""
from django.test import SimpleTestCase

from apps.auth_bounds import (
    EMAIL_MAX_LENGTH,
    EMAIL_MIN_LENGTH,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
    validate_email,
    validate_login_payload,
    validate_password,
    validate_register_payload,
    validate_username,
)
from apps.domain_bounds import (
    PRODUCT_NAME_MAX,
    PRODUCT_NAME_MIN,
    PRODUCT_PRICE_MAX,
    PRODUCT_PRICE_MIN,
    CATEGORY_SLUG_MAX,
    CATEGORY_SLUG_MIN,
    MOBILE_MAX,
    MOBILE_MIN,
    TRANSACTION_ID_MAX,
    validate_cart_action,
    validate_category_fields,
    validate_order_fields,
    validate_product_fields,
    validate_shipping_fields,
)


class AuthUsernameBoundsUnitTest(SimpleTestCase):
    def test_bva_username_min_minus_1_invalid(self):
        # tag: BVA:auth.username.min-1
        self.assertIsNotNone(validate_username(""))

    def test_bva_username_min_valid(self):
        # tag: BVA:auth.username.min
        self.assertIsNone(validate_username("a"))
        self.assertEqual(len("a"), USERNAME_MIN_LENGTH)

    def test_bva_username_max_valid(self):
        # tag: BVA:auth.username.max
        value = "a" * USERNAME_MAX_LENGTH
        self.assertIsNone(validate_username(value))

    def test_bva_username_max_plus_1_invalid(self):
        # tag: BVA:auth.username.max+1
        value = "a" * (USERNAME_MAX_LENGTH + 1)
        self.assertIsNotNone(validate_username(value))

    def test_ep_username_invalid_charset(self):
        # tag: EP:auth.username.invalid.charset
        self.assertIsNotNone(validate_username("bad-name"))


class AuthPasswordBoundsUnitTest(SimpleTestCase):
    def test_bva_password_min_minus_1_invalid(self):
        self.assertIsNotNone(validate_password("x" * (PASSWORD_MIN_LENGTH - 1)))

    def test_bva_password_min_valid(self):
        self.assertIsNone(validate_password("x" * PASSWORD_MIN_LENGTH))

    def test_bva_password_max_valid(self):
        self.assertIsNone(validate_password("x" * PASSWORD_MAX_LENGTH))

    def test_bva_password_max_plus_1_invalid(self):
        self.assertIsNotNone(validate_password("x" * (PASSWORD_MAX_LENGTH + 1)))


class AuthEmailBoundsUnitTest(SimpleTestCase):
    def test_ep_email_invalid_format(self):
        self.assertIsNotNone(validate_email("notanemail"))

    def test_bva_email_min_valid_format(self):
        # a@b.c length 5 == EMAIL_MIN_LENGTH
        email = "a@b.c"
        self.assertEqual(len(email), EMAIL_MIN_LENGTH)
        self.assertIsNone(validate_email(email))

    def test_bva_email_too_long_invalid(self):
        email = "a" * (EMAIL_MAX_LENGTH - 4) + "@b.co"
        # ensure strictly longer than max
        while len(email) <= EMAIL_MAX_LENGTH:
            email = "a" + email
        self.assertGreater(len(email), EMAIL_MAX_LENGTH)
        self.assertIsNotNone(validate_email(email))


class AuthPayloadUnitTest(SimpleTestCase):
    def test_register_payload_valid(self):
        errors = validate_register_payload(
            {
                "username": "user_ok",
                "password": "Passw0rd!",
                "email": "ok@test.com",
                "first_name": "An",
                "last_name": "B",
            }
        )
        self.assertEqual(errors, [])

    def test_login_payload_missing_password_invalid(self):
        errors = validate_login_payload({"username": "u1", "password": ""})
        self.assertTrue(errors)


class ProductBoundsUnitTest(SimpleTestCase):
    def test_bva_name_min_valid(self):
        errors = validate_product_fields({"name": "A", "price": 1})
        self.assertEqual(errors, [])
        self.assertEqual(len("A"), PRODUCT_NAME_MIN)

    def test_bva_name_max_plus_1_invalid(self):
        errors = validate_product_fields(
            {"name": "N" * (PRODUCT_NAME_MAX + 1), "price": 1}
        )
        self.assertTrue(errors)

    def test_bva_price_min_valid(self):
        errors = validate_product_fields({"name": "P", "price": PRODUCT_PRICE_MIN})
        self.assertEqual(errors, [])

    def test_bva_price_min_minus_1_invalid(self):
        errors = validate_product_fields({"name": "P", "price": PRODUCT_PRICE_MIN - 1})
        self.assertTrue(errors)

    def test_bva_price_max_valid(self):
        errors = validate_product_fields({"name": "P", "price": PRODUCT_PRICE_MAX})
        self.assertEqual(errors, [])

    def test_bva_price_max_plus_1_invalid(self):
        errors = validate_product_fields({"name": "P", "price": PRODUCT_PRICE_MAX + 1})
        self.assertTrue(errors)

    def test_ep_price_invalid_type(self):
        errors = validate_product_fields({"name": "P", "price": "abc"})
        self.assertTrue(errors)


class CategoryBoundsUnitTest(SimpleTestCase):
    def test_bva_slug_min_valid(self):
        errors = validate_category_fields({"name": "A", "slug": "a"})
        self.assertEqual(errors, [])
        self.assertEqual(len("a"), CATEGORY_SLUG_MIN)

    def test_bva_slug_max_plus_1_invalid(self):
        errors = validate_category_fields(
            {"name": "A", "slug": "a" * (CATEGORY_SLUG_MAX + 1)}
        )
        self.assertTrue(errors)

    def test_ep_slug_invalid_charset(self):
        errors = validate_category_fields({"name": "A", "slug": "Bad_Slug"})
        self.assertTrue(errors)


class OrderBoundsUnitTest(SimpleTestCase):
    def test_bva_transaction_id_max_valid(self):
        errors = validate_order_fields({"transaction_id": "T" * TRANSACTION_ID_MAX})
        self.assertEqual(errors, [])

    def test_bva_transaction_id_max_plus_1_invalid(self):
        errors = validate_order_fields(
            {"transaction_id": "T" * (TRANSACTION_ID_MAX + 1)}
        )
        self.assertTrue(errors)


class ShippingBoundsUnitTest(SimpleTestCase):
    def test_bva_mobile_exact_valid(self):
        errors = validate_shipping_fields(
            {
                "address": "A",
                "city": "HN",
                "mobile": "0123456789",
            }
        )
        self.assertEqual(errors, [])
        self.assertEqual(len("0123456789"), MOBILE_MIN)
        self.assertEqual(len("0123456789"), MOBILE_MAX)

    def test_bva_mobile_min_minus_1_invalid(self):
        errors = validate_shipping_fields(
            {"address": "A", "city": "HN", "mobile": "012345678"}
        )
        self.assertTrue(errors)

    def test_bva_mobile_max_plus_1_invalid(self):
        errors = validate_shipping_fields(
            {"address": "A", "city": "HN", "mobile": "01234567890"}
        )
        self.assertTrue(errors)

    def test_ep_mobile_invalid_charset(self):
        errors = validate_shipping_fields(
            {"address": "A", "city": "HN", "mobile": "091234567a"}
        )
        self.assertTrue(errors)


class CartActionBoundsUnitTest(SimpleTestCase):
    def test_ep_action_valid_add_remove(self):
        self.assertIsNone(validate_cart_action("add"))
        self.assertIsNone(validate_cart_action("remove"))

    def test_ep_action_invalid(self):
        self.assertIsNotNone(validate_cart_action("noop"))
        self.assertIsNotNone(validate_cart_action(""))
