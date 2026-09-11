"""
Excel-driven tests cho backend.

Doc: apps/tests/excel_data/backend_api_tests.xlsx
Moi dong Excel (enabled=Y) = 1 testcase pass/fail.

Chay:
  python manage.py test apps.tests.test_excel_driven -v 2
"""
from __future__ import annotations

from django.test import TestCase
from rest_framework.test import APIClient

from .excel_runner import (
    EXCEL_PATH,
    apply_setup,
    contains_expected,
    extract_response_data,
    load_excel_cases,
    resolve_case,
)


def _run_excel_case(test_case: TestCase, case: dict) -> None:
    client = APIClient()
    ctx = apply_setup(client, case["setup"])
    resolved = resolve_case(case, ctx)

    method = resolved["method"].lower()
    url = resolved["url"]
    payload = resolved["input"] or {}

    request_fn = getattr(client, method)
    if method in {"post", "put", "patch"}:
        response = request_fn(url, data=payload, format="json")
    else:
        response = request_fn(url)

    actual_status = response.status_code
    actual_body = extract_response_data(response)
    expected_status = resolved["expected_status"]
    expected_body = resolved["expected_result"]

    test_case.assertEqual(
        actual_status,
        expected_status,
        msg=(
            f"[{case['test_id']}] {case['description']}\n"
            f"URL: {method.upper()} {url}\n"
            f"Input: {payload}\n"
            f"Expected status: {expected_status}, Actual: {actual_status}\n"
            f"Response: {actual_body}"
        ),
    )

    test_case.assertTrue(
        contains_expected(actual_body, expected_body),
        msg=(
            f"[{case['test_id']}] {case['description']}\n"
            f"Expected result (subset): {expected_body}\n"
            f"Actual response: {actual_body}"
        ),
    )


class ExcelDrivenBackendTest(TestCase):
    """
    Test method duoc gan dong tu Excel luc import module.
    Sua data trong file .xlsx — khong hard-code assertion tung API.
    """

    def test_excel_file_exists_and_has_cases(self):
        self.assertTrue(
            EXCEL_PATH.exists(),
            f"Thieu file Excel: {EXCEL_PATH}",
        )
        cases = load_excel_cases()
        self.assertGreater(len(cases), 0, "Excel khong co testcase enabled nao")


def _attach_excel_tests() -> None:
    try:
        cases = load_excel_cases()
    except FileNotFoundError:
        return

    used_names: set[str] = set()
    for case in cases:
        base = f"test_{case['sheet']}_{case['test_id']}".replace("-", "_")
        method_name = base
        i = 2
        while method_name in used_names or hasattr(ExcelDrivenBackendTest, method_name):
            method_name = f"{base}_{i}"
            i += 1
        used_names.add(method_name)

        def _make(c):
            def _test(self):
                _run_excel_case(self, c)

            _test.__doc__ = f"{c['test_id']}: {c['description']}"
            _test.__name__ = method_name
            return _test

        setattr(ExcelDrivenBackendTest, method_name, _make(case))


_attach_excel_tests()
