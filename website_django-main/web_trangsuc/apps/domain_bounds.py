"""
Domain bounds cho backend — dung thiet ke BVA + Equivalence Partitioning.

Auth: xem auth_bounds.py
"""
from __future__ import annotations

import re
from typing import Any

# ---- Product ----
PRODUCT_NAME_MIN = 1
PRODUCT_NAME_MAX = 100
PRODUCT_PRICE_MIN = 0
PRODUCT_PRICE_MAX = 100_000_000
PRODUCT_DETAIL_MAX = 500

# ---- Category ----
CATEGORY_NAME_MIN = 1
CATEGORY_NAME_MAX = 100
CATEGORY_SLUG_MIN = 1
CATEGORY_SLUG_MAX = 50
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# ---- Order ----
TRANSACTION_ID_MAX = 50

# ---- Shipping ----
ADDRESS_MIN = 1
ADDRESS_MAX = 200
CITY_MIN = 1
CITY_MAX = 100
STATE_MAX = 100
MOBILE_MIN = 10
MOBILE_MAX = 10
MOBILE_PATTERN = re.compile(r"^\d{10}$")

# ---- Cart updateItem ----
VALID_CART_ACTIONS = {"add", "remove"}


def _str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def err_len(field: str, n: int, lo: int, hi: int) -> str | None:
    if n < lo or n > hi:
        return f"{field} must be between {lo} and {hi} characters"
    return None


def validate_product_fields(data: dict, partial: bool = False) -> list[str]:
    errors: list[str] = []

    if "name" in data or not partial:
        name = data.get("name")
        if name is None or name == "":
            errors.append(
                f"name is required (length {PRODUCT_NAME_MIN}-{PRODUCT_NAME_MAX})"
            )
        else:
            text = _str(name) or ""
            msg = err_len("name", len(text), PRODUCT_NAME_MIN, PRODUCT_NAME_MAX)
            if msg:
                errors.append(msg)

    if "price" in data or not partial:
        price = data.get("price")
        if price is None or price == "":
            errors.append(
                f"price is required (range {PRODUCT_PRICE_MIN}-{PRODUCT_PRICE_MAX})"
            )
        else:
            try:
                p = int(price)
            except (TypeError, ValueError):
                errors.append("price must be an integer")
            else:
                if p < PRODUCT_PRICE_MIN or p > PRODUCT_PRICE_MAX:
                    errors.append(
                        f"price must be between {PRODUCT_PRICE_MIN} and {PRODUCT_PRICE_MAX}"
                    )

    if "detail" in data and data.get("detail") not in (None, ""):
        detail = _str(data.get("detail")) or ""
        if len(detail) > PRODUCT_DETAIL_MAX:
            errors.append(
                f"detail must be between 0 and {PRODUCT_DETAIL_MAX} characters"
            )

    return errors


def validate_category_fields(data: dict, partial: bool = False) -> list[str]:
    errors: list[str] = []

    if "name" in data or not partial:
        name = data.get("name")
        if name is None or name == "":
            errors.append(
                f"name is required (length {CATEGORY_NAME_MIN}-{CATEGORY_NAME_MAX})"
            )
        else:
            text = _str(name) or ""
            msg = err_len("name", len(text), CATEGORY_NAME_MIN, CATEGORY_NAME_MAX)
            if msg:
                errors.append(msg)

    if "slug" in data or not partial:
        slug = data.get("slug")
        if slug is None or slug == "":
            errors.append(
                f"slug is required (length {CATEGORY_SLUG_MIN}-{CATEGORY_SLUG_MAX})"
            )
        else:
            text = _str(slug) or ""
            msg = err_len("slug", len(text), CATEGORY_SLUG_MIN, CATEGORY_SLUG_MAX)
            if msg:
                errors.append(msg)
            elif not SLUG_PATTERN.fullmatch(text):
                errors.append("slug must be lowercase letters, numbers, hyphens")

    if "is_sub" in data and data.get("is_sub") not in (True, False, 0, 1, "true", "false", "0", "1", None):
        # DRF may coerce; only flag clearly invalid types later
        pass

    return errors


def validate_order_fields(data: dict, partial: bool = False) -> list[str]:
    errors: list[str] = []
    if "transaction_id" in data and data.get("transaction_id") not in (None, ""):
        tid = _str(data.get("transaction_id")) or ""
        if len(tid) > TRANSACTION_ID_MAX:
            errors.append(
                f"transaction_id must be between 0 and {TRANSACTION_ID_MAX} characters"
            )
    if "complete" in data and data.get("complete") not in (
        True,
        False,
        None,
        0,
        1,
        "true",
        "false",
        "0",
        "1",
        "True",
        "False",
    ):
        errors.append("complete must be a boolean")
    return errors


def validate_shipping_fields(data: dict, partial: bool = False) -> list[str]:
    errors: list[str] = []

    if "address" in data or not partial:
        address = data.get("address")
        if address is None or address == "":
            errors.append(
                f"address is required (length {ADDRESS_MIN}-{ADDRESS_MAX})"
            )
        else:
            text = _str(address) or ""
            msg = err_len("address", len(text), ADDRESS_MIN, ADDRESS_MAX)
            if msg:
                errors.append(msg)

    if "city" in data or not partial:
        city = data.get("city")
        if city is None or city == "":
            errors.append(f"city is required (length {CITY_MIN}-{CITY_MAX})")
        else:
            text = _str(city) or ""
            msg = err_len("city", len(text), CITY_MIN, CITY_MAX)
            if msg:
                errors.append(msg)

    if "state" in data and data.get("state") not in (None, ""):
        state = _str(data.get("state")) or ""
        if len(state) > STATE_MAX:
            errors.append(f"state must be between 0 and {STATE_MAX} characters")

    if "mobile" in data or not partial:
        mobile = data.get("mobile")
        if mobile is None or mobile == "":
            errors.append(
                f"mobile is required (length {MOBILE_MIN}-{MOBILE_MAX} digits)"
            )
        else:
            text = _str(mobile) or ""
            if len(text) < MOBILE_MIN or len(text) > MOBILE_MAX:
                errors.append(
                    f"mobile must be between {MOBILE_MIN} and {MOBILE_MAX} characters"
                )
            elif not MOBILE_PATTERN.fullmatch(text):
                errors.append("mobile must be exactly 10 digits")

    return errors


def validate_cart_action(action: Any) -> str | None:
    if action is None or action == "":
        return "action is required (add|remove)"
    text = _str(action) or ""
    if text not in VALID_CART_ACTIONS:
        return "action must be add or remove"
    return None
