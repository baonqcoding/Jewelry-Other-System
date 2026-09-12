"""
Utilities: doc Excel testcase + setup fixture + so khop expected_result.
"""
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from openpyxl import load_workbook

from apps.models import Category, Order, OrderItem, Product, ShippingAddress
from django.contrib.auth.models import User


EXCEL_PATH = Path(__file__).resolve().parent / "excel_data" / "backend_api_tests.xlsx"

PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_]+)\}")


def _parse_json(value: Any, default=None):
    if value is None or value == "":
        return default if default is not None else {}
    if isinstance(value, (dict, list)):
        return value
    text = str(value).strip()
    if not text:
        return default if default is not None else {}
    return json.loads(text)


def load_excel_cases(path: Path | None = None, sheet: str | None = None) -> list[dict]:
    """Doc tat ca sheet (tru README) thanh list dict testcase."""
    workbook_path = path or EXCEL_PATH
    if not workbook_path.exists():
        raise FileNotFoundError(
            f"Khong tim thay Excel: {workbook_path}. "
            f"Them file apps/tests/excel_data/backend_api_tests.xlsx vao project."
        )

    wb = load_workbook(workbook_path, data_only=True)
    cases: list[dict] = []

    for sheet_name in wb.sheetnames:
        if sheet_name.upper() in {"README", "BOUNDS"}:
            continue
        if sheet is not None and sheet_name != sheet:
            continue

        ws = wb[sheet_name]
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            continue
        headers = [str(h).strip() if h is not None else "" for h in rows[0]]

        for row in rows[1:]:
            if row is None or all(c is None or str(c).strip() == "" for c in row):
                continue
            item = {headers[i]: row[i] for i in range(len(headers)) if headers[i]}
            if "expected_status" not in headers or item.get("expected_status") in (None, ""):
                continue
            enabled = str(item.get("enabled", "Y")).strip().upper()
            if enabled in {"N", "NO", "0", "FALSE"}:
                continue

            cases.append(
                {
                    "sheet": sheet_name,
                    "test_id": str(item.get("test_id", "")).strip(),
                    "description": str(item.get("description") or "").strip(),
                    "method": str(item.get("method") or "GET").strip().upper(),
                    "url": str(item.get("url") or "").strip(),
                    "setup": _parse_json(item.get("setup"), {}),
                    "input": _parse_json(item.get("input"), {}),
                    "expected_status": int(item.get("expected_status")),
                    "expected_result": _parse_json(item.get("expected_result"), {}),
                }
            )
    return cases


def apply_setup(client, setup: dict) -> dict[str, Any]:
    """
    Tao fixture theo setup JSON. Tra ve context placeholder:
    product_id, category_id, order_id, order_item_id, shipping_id, user_id, username, password
    """
    ctx: dict[str, Any] = {}
    users_by_name: dict[str, User] = {}

    for u in setup.get("users", []):
        user = User.objects.create_user(
            username=u["username"],
            password=u.get("password", "Passw0rd!"),
            email=u.get("email", f"{u['username']}@example.com"),
            first_name=u.get("first_name", ""),
            last_name=u.get("last_name", ""),
        )
        users_by_name[user.username] = user
        ctx["user_id"] = user.id
        ctx["username"] = user.username
        ctx["password"] = u.get("password", "Passw0rd!")

    categories_by_slug: dict[str, Category] = {}
    for c in setup.get("categories", []):
        cat = Category.objects.create(
            name=c.get("name", "Category"),
            slug=c["slug"],
            is_sub=c.get("is_sub", False),
        )
        categories_by_slug[cat.slug] = cat
        ctx["category_id"] = cat.id

    products: list[Product] = []
    for p in setup.get("products", []):
        product = Product.objects.create(
            name=p.get("name", "Product"),
            price=p.get("price", 1000),
            detail=p.get("detail", ""),
        )
        for slug in p.get("category_slugs", []):
            if slug in categories_by_slug:
                product.category.add(categories_by_slug[slug])
            elif Category.objects.filter(slug=slug).exists():
                product.category.add(Category.objects.get(slug=slug))
        products.append(product)
        ctx["product_id"] = product.id

    orders: list[Order] = []
    for o in setup.get("orders", []):
        customer = None
        if "customer_username" in o:
            customer = users_by_name.get(o["customer_username"])
        elif users_by_name:
            customer = next(iter(users_by_name.values()))
        order = Order.objects.create(
            customer=customer,
            complete=o.get("complete", False),
            transaction_id=o.get("transaction_id"),
        )
        orders.append(order)
        ctx["order_id"] = order.id

    for oi in setup.get("order_items", []):
        order = orders[-1] if orders else None
        product = products[-1] if products else None
        item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=oi.get("quantity", 1),
        )
        ctx["order_item_id"] = item.id

    for s in setup.get("shippings", []):
        customer = next(iter(users_by_name.values())) if users_by_name else None
        order = orders[-1] if orders else None
        shipping = ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=s.get("address", "Address"),
            city=s.get("city", "City"),
            state=s.get("state", "State"),
            mobile=s.get("mobile", "0912345678"),
        )
        ctx["shipping_id"] = shipping.id

    login_as = setup.get("login_as")
    if login_as:
        password = ctx.get("password", "Passw0rd!")
        # neu login_as khac user cuoi, lay password tu users list
        for u in setup.get("users", []):
            if u["username"] == login_as:
                password = u.get("password", "Passw0rd!")
                break
        assert client.login(username=login_as, password=password), (
            f"Khong login duoc user {login_as}"
        )

    return ctx


def _replace_placeholders(value: Any, ctx: dict[str, Any]) -> Any:
    if isinstance(value, dict):
        return {k: _replace_placeholders(v, ctx) for k, v in value.items()}
    if isinstance(value, list):
        return [_replace_placeholders(v, ctx) for v in value]
    if isinstance(value, str):
        def repl(match):
            key = match.group(1)
            if key not in ctx:
                return match.group(0)
            return str(ctx[key])

        replaced = PLACEHOLDER_RE.sub(repl, value)
        # neu toan bo string la so sau replace -> int (cho FK fields)
        if replaced.isdigit() and value != replaced:
            return int(replaced)
        # neu string dang "[\"{category_id}\"]" da thanh "[\"1\"]" -> parse list?
        # handled by json already; for single "{category_id}" as whole string:
        if value.startswith("{") and value.endswith("}") and value.count("{") == 1:
            key = value[1:-1]
            if key in ctx:
                return ctx[key]
        return replaced
    return value


def resolve_case(case: dict, ctx: dict[str, Any]) -> dict:
    resolved = deepcopy(case)
    resolved["url"] = _replace_placeholders(case["url"], ctx)
    resolved["input"] = _replace_placeholders(case["input"], ctx)
    resolved["expected_result"] = _replace_placeholders(case["expected_result"], ctx)
    return resolved


def contains_expected(actual: Any, expected: Any) -> bool:
    """
    So khop subset:
    - expected {} / None -> pass (chi check status)
    - dict: moi key trong expected phai co trong actual va match de quy
    - list: moi phan tu expected[i] match actual[i] (theo thu tu) neu expected ngan hon/bang
      neu expected la list object subset, tim tung expected item xuat hien trong actual
    - scalar: ==
    """
    if expected in ({}, None, ""):
        return True

    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        for key, exp_val in expected.items():
            if key not in actual:
                return False
            if not contains_expected(actual[key], exp_val):
                return False
        return True

    if isinstance(expected, list):
        if not isinstance(actual, list):
            return False
        if not expected:
            return actual == []
        # moi expected item phai match it nhat 1 actual item (subset)
        for exp_item in expected:
            if not any(contains_expected(act_item, exp_item) for act_item in actual):
                return False
        return True

    return actual == expected


def extract_response_data(response) -> Any:
    """Lay JSON body tu DRF Response / Django JsonResponse / empty 204."""
    if getattr(response, "data", None) is not None:
        # DRF Response
        data = response.data
        # ErrorDetail -> str khi dump; convert via json roundtrip
        try:
            return json.loads(json.dumps(data, default=str))
        except TypeError:
            return data

    content = getattr(response, "content", b"") or b""
    if not content:
        return {}
    try:
        return json.loads(content.decode("utf-8"))
    except Exception:
        return {"_raw": content.decode("utf-8", errors="replace")}
