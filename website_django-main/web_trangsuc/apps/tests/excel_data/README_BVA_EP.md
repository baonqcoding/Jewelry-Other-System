# Backend BVA + Equivalence Partitioning

File chính: `backend_bva_ep_tests.xlsx`

## Phạm vi
API REST + `/update_item/` (JSON). **Không** test UI/HTML.

## Bounds (code)
- `apps/auth_bounds.py` — Register/Login
- `apps/domain_bounds.py` — Product, Category, Order, Shipping, Cart

## Sheet
| Sheet | Nội dung |
|---|---|
| Bounds | Bảng biên + lớp tương đương |
| Auth / Product / Category / Order / OrderItem / Shipping / UpdateItem | Testcase theo module |
| All_Cases | Gộp tất cả (tham khảo; runner bỏ qua sheet này để tránh trùng) |

## Chạy
```bash
python manage.py test apps.tests.test_bva_ep_excel -v 2
```
