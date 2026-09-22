"""
Chay rieng bang Equivalence Partitioning.

Excel: apps/tests/excel_data/testcase_EP.xlsx
  - Conditions
  - TestCases

python manage.py test apps.tests.test_ep_cases -v 2
"""
from __future__ import annotations

from pathlib import Path

from django.test import TestCase
from rest_framework.test import APIClient

from .excel_runner import (
    apply_setup,
    contains_expected,
    extract_response_data,
    load_excel_cases,
    resolve_case,
)

EP_EXCEL = Path(__file__).resolve().parent / "excel_data" / "testcase_EP.xlsx"


def _run(test_case: TestCase, case: dict) -> None:
    client = APIClient()
    ctx = apply_setup(client, case["setup"])
    resolved = resolve_case(case, ctx)
    method = resolved["method"].lower()
    url = resolved["url"]
    payload = resolved["input"] or {}
    fn = getattr(client, method)
    response = (
        fn(url, data=payload, format="json")
        if method in {"post", "put", "patch"}
        else fn(url)
    )
    body = extract_response_data(response)
    test_case.assertEqual(
        response.status_code,
        resolved["expected_status"],
        msg=(
            f"[EP {case['test_id']}] tags={case.get('coverage_tag')}\n"
            f"{case.get('validity')} — {case.get('reason')}\n"
            f"{method.upper()} {url} input={payload}\n"
            f"expected {resolved['expected_status']} got {response.status_code}\n"
            f"body={body}"
        ),
    )
    test_case.assertTrue(
        contains_expected(body, resolved["expected_result"]),
        msg=f"[EP {case['test_id']}] expected {resolved['expected_result']} actual {body}",
    )


class EpCasesExcelTest(TestCase):
    def test_ep_file_exists(self):
        self.assertTrue(EP_EXCEL.exists(), f"Missing {EP_EXCEL}")
        self.assertGreaterEqual(len(load_excel_cases(EP_EXCEL, sheet="TestCases")), 8 * 8)


def _attach() -> None:
    try:
        cases = load_excel_cases(EP_EXCEL, sheet="TestCases")
    except FileNotFoundError:
        return
    used: set[str] = set()
    for case in cases:
        name = f"test_{case['test_id']}".replace("-", "_")
        i = 2
        base = name
        while name in used or hasattr(EpCasesExcelTest, name):
            name = f"{base}_{i}"
            i += 1
        used.add(name)

        def _make(c):
            def _test(self):
                _run(self, c)

            _test.__doc__ = f"{c['test_id']} [{c.get('coverage_tag')}] {c.get('validity')}"
            _test.__name__ = name
            return _test

        setattr(EpCasesExcelTest, name, _make(case))


_attach()
