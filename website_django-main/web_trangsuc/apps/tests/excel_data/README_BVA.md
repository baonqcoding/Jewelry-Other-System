# Auth BVA Excel

File: `auth_bva_tests.xlsx`

## Boundary (apps/auth_bounds.py)

| Field | Min | Max | Required |
|---|---|---|---|
| username | 1 | 20 | Yes (`[A-Za-z0-9_]`) |
| password | 8 | 32 | Yes |
| email | 5 | 50 | Yes (register) |
| first_name | 0 | 30 | No |
| last_name | 0 | 30 | No |

## Chạy

```bash
python manage.py test apps.tests.test_auth_bva_excel -v 2
```

Sheets: `Register_BVA`, `Login_BVA`, `Bounds`, `README`
