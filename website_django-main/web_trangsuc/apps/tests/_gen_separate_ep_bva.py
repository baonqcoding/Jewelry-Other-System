"""
Generate two separate Excel workbooks matching assignment templates:

1) testcase_EP.xlsx  — Equivalence Partitioning (>=8 TC / chuc nang)
2) testcase_BVA.xlsx — Boundary Value Analysis (>=8 TC / chuc nang co bien)

Columns (assignment):
  Conditions table: Conditions | Valid Partitions | Tag | Invalid Partitions | Tag | Valid Boundaries | Tag
  TestCases table:  Test Case | Input | Expected Outcome | New Tags Covered
Plus automation cols: method, url, setup, expected_status, expected_result, enabled, validity, reason
"""
from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

BASE = Path(__file__).resolve().parent / "excel_data"
EP_OUT = BASE / "testcase_EP.xlsx"
BVA_OUT = BASE / "testcase_BVA.xlsx"

TC_HEADERS = [
    "test_case",
    "input",
    "expected_outcome",
    "new_tags_covered",
    "validity",
    "reason",
    "enabled",
    "method",
    "url",
    "setup",
    "expected_status",
    "expected_result",
]

COND_HEADERS = [
    "conditions",
    "valid_partitions",
    "tag_valid",
    "invalid_partitions",
    "tag_invalid",
    "valid_boundaries",
    "tag_boundary",
]


def bold(ws):
    for c in ws[1]:
        c.font = Font(bold=True)


def tc(test_case, input_json, expected_outcome, tags, validity, reason,
       method, url, setup, status, result, enabled="Y"):
    return [
        test_case, input_json, expected_outcome, tags, validity, reason,
        enabled, method, url, setup, status, result,
    ]


# =============================================================================
# EP — conditions + cases (>=8 per feature)
# Features: Register, Login, Product, Category, Order, OrderItem, Shipping, Cart
# =============================================================================

EP_CONDITIONS = [
    COND_HEADERS,
    ["Register.username", "unique + [A-Za-z0-9_] len 1..20", "EP_REG_U_V",
     "empty; duplicate; charset invalid", "EP_REG_U_I", "-", "-"],
    ["Register.password", "len 8..32", "EP_REG_P_V", "empty; too short class", "EP_REG_P_I", "-", "-"],
    ["Register.email", "valid format", "EP_REG_E_V", "missing @; empty", "EP_REG_E_I", "-", "-"],
    ["Login.credentials", "correct user/pass", "EP_LOGIN_V", "wrong password; unknown user", "EP_LOGIN_I", "-", "-"],
    ["Product.name/price", "valid name+int price", "EP_PROD_V", "empty name; non-int price; not found id", "EP_PROD_I", "-", "-"],
    ["Category.slug", "valid unique slug", "EP_CAT_V", "duplicate; bad charset; empty name; 404", "EP_CAT_I", "-", "-"],
    ["Order.customer/complete", "valid FK + bool", "EP_ORD_V", "invalid FK; 404", "EP_ORD_I", "-", "-"],
    ["OrderItem.list/detail", "empty/non-empty/found", "EP_OI_V", "not found", "EP_OI_I", "-", "-"],
    ["Shipping.address/mobile", "valid address+10 digits", "EP_SHIP_V", "empty address; mobile charset; 404", "EP_SHIP_I", "-", "-"],
    ["Cart.action/auth", "add/remove + authed", "EP_CART_V", "bad action; anon; missing product", "EP_CART_I", "-", "-"],
]

EP_CASES: list[list] = []

# --- Register (8+) ---
EP_CASES += [
    tc("EP_REG_01", '{"username":"user_ok","password":"Passw0rd!","email":"ok@test.com","first_name":"An","last_name":"Nguyen"}',
       "Hợp lệ — tạo user thành công (201)", "EP_REG_U_V,EP_REG_P_V,EP_REG_E_V",
       "Hợp lệ", "Register hợp lệ", "POST", "/api/register/", "{}", 201, '{"username":"user_ok"}'),
    tc("EP_REG_02", '{"username":"taken","password":"Passw0rd!","email":"x@test.com","first_name":"A","last_name":"B"}',
       "Không hợp lệ — username trùng (400)", "EP_REG_U_I",
       "Không hợp lệ", "Username đã tồn tại", "POST", "/api/register/",
       '{"users":[{"username":"taken","password":"Passw0rd!"}]}', 400, '{"error":"Username already exists"}'),
    tc("EP_REG_03", '{"username":"","password":"Passw0rd!","email":"a@b.com"}',
       "Không hợp lệ — username rỗng (400)", "EP_REG_U_I",
       "Không hợp lệ", "Username bắt buộc", "POST", "/api/register/", "{}", 400, "{}"),
    tc("EP_REG_04", '{"username":"bad-name","password":"Passw0rd!","email":"b@test.com"}',
       "Không hợp lệ — charset username (400)", "EP_REG_U_I",
       "Không hợp lệ", "Username chỉ [A-Za-z0-9_]", "POST", "/api/register/", "{}", 400,
       '{"error":"Username may only contain letters, numbers, and underscore"}'),
    tc("EP_REG_05", '{"username":"embad","password":"Passw0rd!","email":"notanemail"}',
       "Không hợp lệ — email sai format (400)", "EP_REG_E_I",
       "Không hợp lệ", "Email thiếu @", "POST", "/api/register/", "{}", 400,
       '{"error":"Email format is invalid"}'),
    tc("EP_REG_06", '{"username":"nopw","password":"","email":"np@test.com"}',
       "Không hợp lệ — password rỗng (400)", "EP_REG_P_I",
       "Không hợp lệ", "Password bắt buộc", "POST", "/api/register/", "{}", 400, "{}"),
    tc("EP_REG_07", '{"username":"u_mail","password":"Passw0rd!","email":"good@mail.com"}',
       "Hợp lệ — email đúng format (201)", "EP_REG_E_V",
       "Hợp lệ", "Email hợp lệ", "POST", "/api/register/", "{}", 201, '{"username":"u_mail"}'),
    tc("EP_REG_08", '{"username":"u_pw","password":"Abcdef12","email":"pw@mail.com"}',
       "Hợp lệ — password thuộc lớp độ dài hợp lệ (201)", "EP_REG_P_V",
       "Hợp lệ", "Password hợp lệ", "POST", "/api/register/", "{}", 201, '{"username":"u_pw"}'),
]

# --- Login (8+) ---
EP_CASES += [
    tc("EP_LOGIN_01", '{"username":"loginok","password":"Passw0rd!"}',
       "Hợp lệ — đăng nhập đúng (200)", "EP_LOGIN_V",
       "Hợp lệ", "Credentials đúng", "POST", "/api/login/",
       '{"users":[{"username":"loginok","password":"Passw0rd!"}]}', 200, '{"message":"Login successful"}'),
    tc("EP_LOGIN_02", '{"username":"loginfail","password":"WrongPass1"}',
       "Không hợp lệ — sai password (401)", "EP_LOGIN_I",
       "Không hợp lệ", "Password sai", "POST", "/api/login/",
       '{"users":[{"username":"loginfail","password":"Passw0rd!"}]}', 401,
       '{"error":"Invalid username or password"}'),
    tc("EP_LOGIN_03", '{"username":"ghost_user","password":"Passw0rd!"}',
       "Không hợp lệ — user không tồn tại (401)", "EP_LOGIN_I",
       "Không hợp lệ", "Unknown user", "POST", "/api/login/", "{}", 401,
       '{"error":"Invalid username or password"}'),
    tc("EP_LOGIN_04", '{"username":"","password":"Passw0rd!"}',
       "Không hợp lệ — username rỗng (400)", "EP_LOGIN_I",
       "Không hợp lệ", "Username required", "POST", "/api/login/", "{}", 400, "{}"),
    tc("EP_LOGIN_05", '{"username":"loginok","password":""}',
       "Không hợp lệ — password rỗng (400)", "EP_LOGIN_I",
       "Không hợp lệ", "Password required", "POST", "/api/login/",
       '{"users":[{"username":"loginok","password":"Passw0rd!"}]}', 400, "{}"),
    tc("EP_LOGIN_06", '{}',
       "Hợp lệ — logout khi đã login (200)", "EP_LOGIN_V",
       "Hợp lệ", "Logout authenticated", "POST", "/api/logout/",
       '{"users":[{"username":"out1","password":"Passw0rd!"}],"login_as":"out1"}', 200,
       '{"message":"Logout successful"}'),
    tc("EP_LOGIN_07", '{}',
       "Hợp lệ — logout anonymous (200)", "EP_LOGIN_V",
       "Hợp lệ", "Logout anonymous idempotent", "POST", "/api/logout/", "{}", 200,
       '{"message":"Logout successful"}'),
    tc("EP_LOGIN_08", '{"username":"loginok2","password":"Passw0rd!"}',
       "Hợp lệ — login lại sau khi tạo user (200)", "EP_LOGIN_V",
       "Hợp lệ", "Valid credentials class", "POST", "/api/login/",
       '{"users":[{"username":"loginok2","password":"Passw0rd!"}]}', 200,
       '{"message":"Login successful"}'),
]

# --- Product (8+) ---
EP_CASES += [
    tc("EP_PROD_01", '{}', "Hợp lệ — list rỗng (200)", "EP_PROD_V",
       "Hợp lệ", "Empty set", "GET", "/api/products/", "{}", 200, "[]"),
    tc("EP_PROD_02", '{}', "Hợp lệ — list có dữ liệu (200)", "EP_PROD_V",
       "Hợp lệ", "Non-empty set", "GET", "/api/products/",
       '{"categories":[{"name":"Nhan","slug":"nhan"}],"products":[{"name":"SP1","price":1000,"category_slugs":["nhan"]}]}',
       200, '[{"name":"SP1","price":1000}]'),
    tc("EP_PROD_03", '{"name":"Lac tay","price":500000,"detail":"Bac","category":["{category_id}"]}',
       "Hợp lệ — tạo product (201)", "EP_PROD_V",
       "Hợp lệ", "Valid create", "POST", "/api/products/",
       '{"categories":[{"name":"Nhan","slug":"nhan"}]}', 201, '{"name":"Lac tay","price":500000}'),
    tc("EP_PROD_04", '{"name":"","price":1000}',
       "Không hợp lệ — name rỗng (400)", "EP_PROD_I",
       "Không hợp lệ", "Empty name", "POST", "/api/products/", "{}", 400, "{}"),
    tc("EP_PROD_05", '{"name":"BadPrice","price":"abc"}',
       "Không hợp lệ — price không phải int (400)", "EP_PROD_I",
       "Không hợp lệ", "Invalid price type", "POST", "/api/products/", "{}", 400, "{}"),
    tc("EP_PROD_06", '{}', "Hợp lệ — GET product tồn tại (200)", "EP_PROD_V",
       "Hợp lệ", "Found id", "GET", "/api/products/{product_id}/",
       '{"products":[{"name":"Xem","price":99}]}', 200, '{"name":"Xem"}'),
    tc("EP_PROD_07", '{}', "Không hợp lệ — GET product 404", "EP_PROD_I",
       "Không hợp lệ", "Not found", "GET", "/api/products/99999/", "{}", 404,
       '{"error":"Product not found"}'),
    tc("EP_PROD_08", '{}', "Hợp lệ — DELETE product (204)", "EP_PROD_V",
       "Hợp lệ", "Delete found", "DELETE", "/api/products/{product_id}/",
       '{"products":[{"name":"Xoa","price":1}]}', 204, "{}"),
]

# --- Category (8+) ---
EP_CASES += [
    tc("EP_CAT_01", '{"name":"Trang suc","slug":"trang-suc","is_sub":false,"sub_category":null}',
       "Hợp lệ — tạo category cha (201)", "EP_CAT_V",
       "Hợp lệ", "Valid parent", "POST", "/api/categories/", "{}", 201,
       '{"slug":"trang-suc","is_sub":false}'),
    tc("EP_CAT_02", '{"name":"Con","slug":"con","is_sub":true,"sub_category":"{category_id}"}',
       "Hợp lệ — tạo subcategory (201)", "EP_CAT_V",
       "Hợp lệ", "Valid child", "POST", "/api/categories/",
       '{"categories":[{"name":"Cha","slug":"cha"}]}', 201, '{"slug":"con","is_sub":true}'),
    tc("EP_CAT_03", '{"name":"B","slug":"trung","is_sub":false}',
       "Không hợp lệ — slug trùng (400)", "EP_CAT_I",
       "Không hợp lệ", "Duplicate slug", "POST", "/api/categories/",
       '{"categories":[{"name":"A","slug":"trung"}]}', 400, "{}"),
    tc("EP_CAT_04", '{"name":"Bad","slug":"Bad_Slug","is_sub":false}',
       "Không hợp lệ — slug charset (400)", "EP_CAT_I",
       "Không hợp lệ", "Invalid slug charset", "POST", "/api/categories/", "{}", 400,
       '{"error":"slug must be lowercase letters, numbers, hyphens"}'),
    tc("EP_CAT_05", '{"name":"","slug":"empty-name","is_sub":false}',
       "Không hợp lệ — name rỗng (400)", "EP_CAT_I",
       "Không hợp lệ", "Empty name", "POST", "/api/categories/", "{}", 400, "{}"),
    tc("EP_CAT_06", '{}', "Không hợp lệ — GET 404", "EP_CAT_I",
       "Không hợp lệ", "Not found", "GET", "/api/categories/99999/", "{}", 404,
       '{"error":"Category not found"}'),
    tc("EP_CAT_07", '{}', "Hợp lệ — DELETE category (204)", "EP_CAT_V",
       "Hợp lệ", "Delete found", "DELETE", "/api/categories/{category_id}/",
       '{"categories":[{"name":"Xoa","slug":"xoa-cat"}]}', 204, "{}"),
    tc("EP_CAT_08", '{}', "Hợp lệ — GET list categories (200)", "EP_CAT_V",
       "Hợp lệ", "List", "GET", "/api/categories/",
       '{"categories":[{"name":"A","slug":"aa"}]}', 200, '[{"slug":"aa"}]'),
]

# --- Order (8+) ---
EP_CASES += [
    tc("EP_ORD_01", '{"customer":"{user_id}","complete":false,"transaction_id":"TX1"}',
       "Hợp lệ — tạo order (201)", "EP_ORD_V",
       "Hợp lệ", "Valid create", "POST", "/api/orders/",
       '{"users":[{"username":"buyer","password":"Passw0rd!"}]}', 201,
       '{"transaction_id":"TX1","complete":false}'),
    tc("EP_ORD_02", '{"customer":"{user_id}","complete":true,"transaction_id":"DONE"}',
       "Hợp lệ — PUT complete=true (200)", "EP_ORD_V",
       "Hợp lệ", "Valid complete true", "PUT", "/api/orders/{order_id}/",
       '{"users":[{"username":"buyer2","password":"Passw0rd!"}],"orders":[{"customer_username":"buyer2","transaction_id":"OLD"}]}',
       200, '{"complete":true,"transaction_id":"DONE"}'),
    tc("EP_ORD_03", '{"customer":99999,"complete":false}',
       "Không hợp lệ — customer FK invalid (400)", "EP_ORD_I",
       "Không hợp lệ", "Invalid FK", "POST", "/api/orders/", "{}", 400, "{}"),
    tc("EP_ORD_04", '{}', "Không hợp lệ — GET 404", "EP_ORD_I",
       "Không hợp lệ", "Not found", "GET", "/api/orders/99999/", "{}", 404,
       '{"error":"Order not found"}'),
    tc("EP_ORD_05", '{}', "Hợp lệ — DELETE order (204)", "EP_ORD_V",
       "Hợp lệ", "Delete found", "DELETE", "/api/orders/{order_id}/",
       '{"users":[{"username":"buyer5","password":"Passw0rd!"}],"orders":[{"customer_username":"buyer5"}]}',
       204, "{}"),
    tc("EP_ORD_06", '{}', "Hợp lệ — GET list orders (200)", "EP_ORD_V",
       "Hợp lệ", "List", "GET", "/api/orders/",
       '{"users":[{"username":"buyer6","password":"Passw0rd!"}],"orders":[{"customer_username":"buyer6","transaction_id":"L1"}]}',
       200, '[{"transaction_id":"L1"}]'),
    tc("EP_ORD_07", '{"customer":"{user_id}","complete":false,"transaction_id":"TX2"}',
       "Hợp lệ — order incomplete class (201)", "EP_ORD_V",
       "Hợp lệ", "complete=false class", "POST", "/api/orders/",
       '{"users":[{"username":"buyer7","password":"Passw0rd!"}]}', 201, '{"complete":false}'),
    tc("EP_ORD_08", '{}', "Hợp lệ — GET order tồn tại (200)", "EP_ORD_V",
       "Hợp lệ", "Found", "GET", "/api/orders/{order_id}/",
       '{"users":[{"username":"buyer8","password":"Passw0rd!"}],"orders":[{"customer_username":"buyer8","transaction_id":"G1"}]}',
       200, '{"transaction_id":"G1"}'),
]

# --- OrderItem (8+) ---
EP_CASES += [
    tc("EP_OI_01", '{}', "Hợp lệ — list rỗng (200)", "EP_OI_V",
       "Hợp lệ", "Empty", "GET", "/api/order-items/", "{}", 200, "[]"),
    tc("EP_OI_02", '{}', "Hợp lệ — list có dữ liệu (200)", "EP_OI_V",
       "Hợp lệ", "Non-empty", "GET", "/api/order-items/",
       '{"users":[{"username":"oi1","password":"Passw0rd!"}],"products":[{"name":"P","price":10}],"orders":[{"customer_username":"oi1"}],"order_items":[{"quantity":3}]}',
       200, '[{"quantity":3}]'),
    tc("EP_OI_03", '{}', "Hợp lệ — GET item tồn tại (200)", "EP_OI_V",
       "Hợp lệ", "Found", "GET", "/api/order-items/{order_item_id}/",
       '{"users":[{"username":"oi2","password":"Passw0rd!"}],"products":[{"name":"P2","price":10}],"orders":[{"customer_username":"oi2"}],"order_items":[{"quantity":2}]}',
       200, '{"quantity":2}'),
    tc("EP_OI_04", '{}', "Không hợp lệ — GET 404", "EP_OI_I",
       "Không hợp lệ", "Not found", "GET", "/api/order-items/99999/", "{}", 404,
       '{"error":"OrderItem not found"}'),
    tc("EP_OI_05", '{}', "Hợp lệ — list sau khi có 1 item (200)", "EP_OI_V",
       "Hợp lệ", "Non-empty class", "GET", "/api/order-items/",
       '{"users":[{"username":"oi3","password":"Passw0rd!"}],"products":[{"name":"P3","price":11}],"orders":[{"customer_username":"oi3"}],"order_items":[{"quantity":1}]}',
       200, '[{"quantity":1}]'),
    tc("EP_OI_06", '{}', "Hợp lệ — detail quantity=5 (200)", "EP_OI_V",
       "Hợp lệ", "Found qty class", "GET", "/api/order-items/{order_item_id}/",
       '{"users":[{"username":"oi4","password":"Passw0rd!"}],"products":[{"name":"P4","price":12}],"orders":[{"customer_username":"oi4"}],"order_items":[{"quantity":5}]}',
       200, '{"quantity":5}'),
    tc("EP_OI_07", '{}', "Không hợp lệ — id âm/không tồn tại (404)", "EP_OI_I",
       "Không hợp lệ", "Not found class", "GET", "/api/order-items/88888/", "{}", 404,
       '{"error":"OrderItem not found"}'),
    tc("EP_OI_08", '{}', "Hợp lệ — empty list khi chưa seed (200)", "EP_OI_V",
       "Hợp lệ", "Empty class again", "GET", "/api/order-items/", "{}", 200, "[]"),
]

# --- Shipping (8+) ---
EP_CASES += [
    tc("EP_SHIP_01", '{"customer":"{user_id}","order":"{order_id}","address":"123 ABC","city":"HN","state":"HN","mobile":"0912345678"}',
       "Hợp lệ — tạo shipping (201)", "EP_SHIP_V",
       "Hợp lệ", "Valid create", "POST", "/api/shipping-addresses/",
       '{"users":[{"username":"ship1","password":"Passw0rd!"}],"orders":[{"customer_username":"ship1"}]}',
       201, '{"mobile":"0912345678","city":"HN"}'),
    tc("EP_SHIP_02", '{"customer":"{user_id}","order":"{order_id}","address":"A","city":"B","mobile":"091234567a"}',
       "Không hợp lệ — mobile có chữ (400)", "EP_SHIP_I",
       "Không hợp lệ", "Mobile charset", "POST", "/api/shipping-addresses/",
       '{"users":[{"username":"ship5","password":"Passw0rd!"}],"orders":[{"customer_username":"ship5"}]}',
       400, '{"error":"mobile must be exactly 10 digits"}'),
    tc("EP_SHIP_03", '{"customer":"{user_id}","order":"{order_id}","address":"","city":"HN","mobile":"0912345678"}',
       "Không hợp lệ — address rỗng (400)", "EP_SHIP_I",
       "Không hợp lệ", "Empty address", "POST", "/api/shipping-addresses/",
       '{"users":[{"username":"ship6","password":"Passw0rd!"}],"orders":[{"customer_username":"ship6"}]}',
       400, "{}"),
    tc("EP_SHIP_04", '{}', "Không hợp lệ — GET 404", "EP_SHIP_I",
       "Không hợp lệ", "Not found", "GET", "/api/shipping-addresses/99999/", "{}", 404,
       '{"error":"Shipping address not found"}'),
    tc("EP_SHIP_05", '{}', "Hợp lệ — GET list (200)", "EP_SHIP_V",
       "Hợp lệ", "List", "GET", "/api/shipping-addresses/",
       '{"users":[{"username":"shipA","password":"Passw0rd!"}],"orders":[{"customer_username":"shipA"}],"shippings":[{"address":"X","city":"Y","mobile":"0911111111"}]}',
       200, '[{"city":"Y"}]'),
    tc("EP_SHIP_06", '{"customer":"{user_id}","order":"{order_id}","address":"Addr2","city":"","mobile":"0912345678"}',
       "Không hợp lệ — city rỗng (400)", "EP_SHIP_I",
       "Không hợp lệ", "Empty city", "POST", "/api/shipping-addresses/",
       '{"users":[{"username":"shipC","password":"Passw0rd!"}],"orders":[{"customer_username":"shipC"}]}',
       400, "{}"),
    tc("EP_SHIP_07", '{"customer":"{user_id}","order":"{order_id}","address":"Addr3","city":"DN","mobile":"0909090909"}',
       "Hợp lệ — mobile 10 số (201)", "EP_SHIP_V",
       "Hợp lệ", "Valid mobile class", "POST", "/api/shipping-addresses/",
       '{"users":[{"username":"shipD","password":"Passw0rd!"}],"orders":[{"customer_username":"shipD"}]}',
       201, '{"mobile":"0909090909"}'),
    tc("EP_SHIP_08", '{}', "Hợp lệ — GET shipping tồn tại (200)", "EP_SHIP_V",
       "Hợp lệ", "Found", "GET", "/api/shipping-addresses/{shipping_id}/",
       '{"users":[{"username":"shipE","password":"Passw0rd!"}],"orders":[{"customer_username":"shipE"}],"shippings":[{"address":"Z","city":"HN","mobile":"0922222222"}]}',
       200, '{"mobile":"0922222222"}'),
]

# --- Cart / UpdateItem (8+) ---
EP_CASES += [
    tc("EP_CART_01", '{"productId":"{product_id}","action":"add"}',
       "Hợp lệ — add (200)", "EP_CART_V",
       "Hợp lệ", "Valid add", "POST", "/update_item/",
       '{"users":[{"username":"cart1","password":"Passw0rd!"}],"products":[{"name":"C1","price":10}],"login_as":"cart1"}',
       200, '{"message":"Item updated successfully"}'),
    tc("EP_CART_02", '{"productId":"{product_id}","action":"remove"}',
       "Hợp lệ — remove (200)", "EP_CART_V",
       "Hợp lệ", "Valid remove", "POST", "/update_item/",
       '{"users":[{"username":"cart2","password":"Passw0rd!"}],"products":[{"name":"C2","price":10}],"orders":[{"customer_username":"cart2"}],"order_items":[{"quantity":1}],"login_as":"cart2"}',
       200, '{"message":"Item updated successfully"}'),
    tc("EP_CART_03", '{"productId":"{product_id}","action":"noop"}',
       "Không hợp lệ — action sai (400)", "EP_CART_I",
       "Không hợp lệ", "Invalid action", "POST", "/update_item/",
       '{"users":[{"username":"cart3","password":"Passw0rd!"}],"products":[{"name":"C3","price":10}],"login_as":"cart3"}',
       400, '{"error":"action must be add or remove"}'),
    tc("EP_CART_04", '{"productId":99999,"action":"add"}',
       "Không hợp lệ — product không tồn tại (404)", "EP_CART_I",
       "Không hợp lệ", "Product not found", "POST", "/update_item/",
       '{"users":[{"username":"cart4","password":"Passw0rd!"}],"login_as":"cart4"}',
       404, '{"error":"Product not found"}'),
    tc("EP_CART_05", '{"productId":"{product_id}","action":"add"}',
       "Không hợp lệ — chưa login (401)", "EP_CART_I",
       "Không hợp lệ", "Unauthenticated", "POST", "/update_item/",
       '{"products":[{"name":"C5","price":10}]}', 401, '{"error":"Authentication required"}'),
    tc("EP_CART_06", '{"productId":"{product_id}","action":""}',
       "Không hợp lệ — action rỗng (400)", "EP_CART_I",
       "Không hợp lệ", "Empty action", "POST", "/update_item/",
       '{"users":[{"username":"cart6","password":"Passw0rd!"}],"products":[{"name":"C6","price":10}],"login_as":"cart6"}',
       400, "{}"),
    tc("EP_CART_07", '{"productId":"{product_id}","action":"add"}',
       "Hợp lệ — add lần 2 (200)", "EP_CART_V",
       "Hợp lệ", "Add again", "POST", "/update_item/",
       '{"users":[{"username":"cart7","password":"Passw0rd!"}],"products":[{"name":"C7","price":10}],"orders":[{"customer_username":"cart7"}],"order_items":[{"quantity":2}],"login_as":"cart7"}',
       200, '{"message":"Item updated successfully"}'),
    tc("EP_CART_08", '{"action":"add"}',
       "Không hợp lệ — thiếu productId (400/404)", "EP_CART_I",
       "Không hợp lệ", "Missing productId", "POST", "/update_item/",
       '{"users":[{"username":"cart8","password":"Passw0rd!"}],"login_as":"cart8"}',
       400, "{}"),
]


# =============================================================================
# BVA — conditions + cases (>=8 per feature with numeric/length bounds)
# =============================================================================

BVA_CONDITIONS = [
    COND_HEADERS,
    ["Register.username len", "-", "-", "-", "-", "min=1, max=20 → points 0,1,20,21", "BVA_REG_U"],
    ["Register.password len", "-", "-", "-", "-", "min=8, max=32 → 7,8,32,33", "BVA_REG_P"],
    ["Register.email len/format", "-", "-", "-", "-", "min≈5 valid; too long invalid", "BVA_REG_E"],
    ["Product.name len", "-", "-", "-", "-", "min=1, max=100 → 0,1,100,101", "BVA_PROD_N"],
    ["Product.price", "-", "-", "-", "-", "min=0, max=1e8 → -1,0,max,max+1", "BVA_PROD_PR"],
    ["Category.slug len", "-", "-", "-", "-", "min=1, max=50 → 0,1,50,51", "BVA_CAT_S"],
    ["Order.transaction_id len", "-", "-", "-", "-", "max=50 → 50,51", "BVA_ORD_T"],
    ["Shipping.mobile len", "-", "-", "-", "-", "exact 10 → 9,10,11", "BVA_SHIP_M"],
    ["Shipping.address len", "-", "-", "-", "-", "min=1 → 0,1", "BVA_SHIP_A"],
]

BVA_CASES: list[list] = []

# Register BVA (8+)
BVA_CASES += [
    tc("BVA_REG_01", '{"username":"","password":"Passw0rd!","email":"a@b.co"}',
       "Không hợp lệ — username len=0 (min-1)", "BVA_REG_U",
       "Không hợp lệ", "username min-1", "POST", "/api/register/", "{}", 400, "{}"),
    tc("BVA_REG_02", '{"username":"a","password":"Passw0rd!","email":"a1@b.co"}',
       "Hợp lệ — username len=1 (min)", "BVA_REG_U",
       "Hợp lệ", "username min", "POST", "/api/register/", "{}", 201, '{"username":"a"}'),
    tc("BVA_REG_03", '{"username":"abcdefghij1234567890","password":"Passw0rd!","email":"u20@b.co"}',
       "Hợp lệ — username len=20 (max)", "BVA_REG_U",
       "Hợp lệ", "username max", "POST", "/api/register/", "{}", 201,
       '{"username":"abcdefghij1234567890"}'),
    tc("BVA_REG_04", '{"username":"abcdefghij12345678901","password":"Passw0rd!","email":"u21@b.co"}',
       "Không hợp lệ — username len=21 (max+1)", "BVA_REG_U",
       "Không hợp lệ", "username max+1", "POST", "/api/register/", "{}", 400, "{}"),
    tc("BVA_REG_05", '{"username":"pw7user","password":"Passw0r","email":"pw7@b.co"}',
       "Không hợp lệ — password len=7 (min-1)", "BVA_REG_P",
       "Không hợp lệ", "password min-1", "POST", "/api/register/", "{}", 400, "{}"),
    tc("BVA_REG_06", '{"username":"pw8user","password":"Passw0rd","email":"pw8@b.co"}',
       "Hợp lệ — password len=8 (min)", "BVA_REG_P",
       "Hợp lệ", "password min", "POST", "/api/register/", "{}", 201, '{"username":"pw8user"}'),
    tc("BVA_REG_07", '{"username":"pw32user","password":"12345678901234567890123456789012","email":"pw32@b.co"}',
       "Hợp lệ — password len=32 (max)", "BVA_REG_P",
       "Hợp lệ", "password max", "POST", "/api/register/", "{}", 201, '{"username":"pw32user"}'),
    tc("BVA_REG_08", '{"username":"pw33user","password":"123456789012345678901234567890123","email":"pw33@b.co"}',
       "Không hợp lệ — password len=33 (max+1)", "BVA_REG_P",
       "Không hợp lệ", "password max+1", "POST", "/api/register/", "{}", 400, "{}"),
    tc("BVA_REG_09", '{"username":"em5user","password":"Passw0rd!","email":"a@b.c"}',
       "Hợp lệ — email len=5 (min format)", "BVA_REG_E",
       "Hợp lệ", "email min", "POST", "/api/register/", "{}", 201, '{"username":"em5user"}'),
]

# Login BVA-ish edges on payload length (8)
BVA_CASES += [
    tc("BVA_LOGIN_01", '{"username":"","password":"Passw0rd!"}',
       "Không hợp lệ — username rỗng tại biên", "BVA_REG_U",
       "Không hợp lệ", "login username min-1", "POST", "/api/login/", "{}", 400, "{}"),
    tc("BVA_LOGIN_02", '{"username":"a","password":"Passw0rd!"}',
       "Không hợp lệ — user biên min không tồn tại (401)", "BVA_REG_U",
       "Không hợp lệ", "unknown at min length", "POST", "/api/login/", "{}", 401,
       '{"error":"Invalid username or password"}'),
    tc("BVA_LOGIN_03", '{"username":"loginb","password":"Passw0r"}',
       "Không hợp lệ — password len=7", "BVA_REG_P",
       "Không hợp lệ", "login password min-1", "POST", "/api/login/",
       '{"users":[{"username":"loginb","password":"Passw0rd!"}]}', 400, "{}"),
    tc("BVA_LOGIN_04", '{"username":"loginb8","password":"Passw0rd"}',
       "Hợp lệ — password đúng biên 8 nếu khớp user", "BVA_REG_P",
       "Hợp lệ", "login password min matched", "POST", "/api/login/",
       '{"users":[{"username":"loginb8","password":"Passw0rd"}]}', 200,
       '{"message":"Login successful"}'),
    tc("BVA_LOGIN_05", '{"username":"u20loginabcdefghij","password":"Passw0rd!"}',
       "Không hợp lệ — username 20 ký tự chưa seed (401)", "BVA_REG_U",
       "Không hợp lệ", "max-len unknown user", "POST", "/api/login/", "{}", 401,
       '{"error":"Invalid username or password"}'),
    tc("BVA_LOGIN_06", '{"username":"loginok","password":"Passw0rd!"}',
       "Hợp lệ — login chuẩn sau seed", "BVA_REG_P",
       "Hợp lệ", "valid login", "POST", "/api/login/",
       '{"users":[{"username":"loginok","password":"Passw0rd!"}]}', 200,
       '{"message":"Login successful"}'),
    tc("BVA_LOGIN_07", '{"username":"abcdefghij12345678901","password":"Passw0rd!"}',
       "Không hợp lệ — username 21 ký tự", "BVA_REG_U",
       "Không hợp lệ", "username max+1 on login", "POST", "/api/login/", "{}", 400, "{}"),
    tc("BVA_LOGIN_08", '{"username":"loginok","password":"123456789012345678901234567890123"}',
       "Không hợp lệ — password 33 ký tự", "BVA_REG_P",
       "Không hợp lệ", "password max+1 on login", "POST", "/api/login/",
       '{"users":[{"username":"loginok","password":"Passw0rd!"}]}', 400, "{}"),
]

# Product BVA (8+)
BVA_CASES += [
    tc("BVA_PROD_01", '{"name":"A","price":10}',
       "Hợp lệ — name len=1 (min)", "BVA_PROD_N",
       "Hợp lệ", "name min", "POST", "/api/products/", "{}", 201, '{"name":"A"}'),
    tc("BVA_PROD_02", '{"name":"' + ("N" * 100) + '","price":10}',
       "Hợp lệ — name len=100 (max)", "BVA_PROD_N",
       "Hợp lệ", "name max", "POST", "/api/products/", "{}", 201, "{}"),
    tc("BVA_PROD_03", '{"name":"' + ("N" * 101) + '","price":10}',
       "Không hợp lệ — name len=101 (max+1)", "BVA_PROD_N",
       "Không hợp lệ", "name max+1", "POST", "/api/products/", "{}", 400, "{}"),
    tc("BVA_PROD_04", '{"name":"","price":10}',
       "Không hợp lệ — name len=0 (min-1)", "BVA_PROD_N",
       "Không hợp lệ", "name min-1", "POST", "/api/products/", "{}", 400, "{}"),
    tc("BVA_PROD_05", '{"name":"Free","price":0}',
       "Hợp lệ — price=0 (min)", "BVA_PROD_PR",
       "Hợp lệ", "price min", "POST", "/api/products/", "{}", 201, '{"price":0}'),
    tc("BVA_PROD_06", '{"name":"Neg","price":-1}',
       "Không hợp lệ — price=-1 (min-1)", "BVA_PROD_PR",
       "Không hợp lệ", "price min-1", "POST", "/api/products/", "{}", 400, "{}"),
    tc("BVA_PROD_07", '{"name":"MaxP","price":100000000}',
       "Hợp lệ — price=max", "BVA_PROD_PR",
       "Hợp lệ", "price max", "POST", "/api/products/", "{}", 201, '{"price":100000000}'),
    tc("BVA_PROD_08", '{"name":"Over","price":100000001}',
       "Không hợp lệ — price=max+1", "BVA_PROD_PR",
       "Không hợp lệ", "price max+1", "POST", "/api/products/", "{}", 400, "{}"),
]

# Category BVA (8+)
BVA_CASES += [
    tc("BVA_CAT_01", '{"name":"X","slug":"a","is_sub":false}',
       "Hợp lệ — slug len=1 (min)", "BVA_CAT_S",
       "Hợp lệ", "slug min", "POST", "/api/categories/", "{}", 201, '{"slug":"a"}'),
    tc("BVA_CAT_02", '{"name":"Long","slug":"' + ("a" * 50) + '","is_sub":false}',
       "Hợp lệ — slug len=50 (max)", "BVA_CAT_S",
       "Hợp lệ", "slug max", "POST", "/api/categories/", "{}", 201, "{}"),
    tc("BVA_CAT_03", '{"name":"Long2","slug":"' + ("a" * 51) + '","is_sub":false}',
       "Không hợp lệ — slug len=51 (max+1)", "BVA_CAT_S",
       "Không hợp lệ", "slug max+1", "POST", "/api/categories/", "{}", 400, "{}"),
    tc("BVA_CAT_04", '{"name":"E","slug":"","is_sub":false}',
       "Không hợp lệ — slug rỗng (min-1)", "BVA_CAT_S",
       "Không hợp lệ", "slug min-1", "POST", "/api/categories/", "{}", 400, "{}"),
    tc("BVA_CAT_05", '{"name":"A","slug":"b","is_sub":false}',
       "Hợp lệ — name len=1 (min)", "BVA_CAT_S",
       "Hợp lệ", "name min with slug", "POST", "/api/categories/", "{}", 201, '{"slug":"b"}'),
    tc("BVA_CAT_06", '{"name":"' + ("C" * 100) + '","slug":"c100","is_sub":false}',
       "Hợp lệ — name len=100 (max)", "BVA_CAT_S",
       "Hợp lệ", "category name max", "POST", "/api/categories/", "{}", 201, '{"slug":"c100"}'),
    tc("BVA_CAT_07", '{"name":"' + ("C" * 101) + '","slug":"c101","is_sub":false}',
       "Không hợp lệ — name len=101", "BVA_CAT_S",
       "Không hợp lệ", "category name max+1", "POST", "/api/categories/", "{}", 400, "{}"),
    tc("BVA_CAT_08", '{"name":"","slug":"emptyn","is_sub":false}',
       "Không hợp lệ — name rỗng", "BVA_CAT_S",
       "Không hợp lệ", "name min-1", "POST", "/api/categories/", "{}", 400, "{}"),
]

# Order BVA (8+)
BVA_CASES += [
    tc("BVA_ORD_01", '{"customer":"{user_id}","complete":false,"transaction_id":"' + ("T" * 50) + '"}',
       "Hợp lệ — transaction_id len=50 (max)", "BVA_ORD_T",
       "Hợp lệ", "txn max", "POST", "/api/orders/",
       '{"users":[{"username":"ob1","password":"Passw0rd!"}]}', 201, "{}"),
    tc("BVA_ORD_02", '{"customer":"{user_id}","complete":false,"transaction_id":"' + ("T" * 51) + '"}',
       "Không hợp lệ — transaction_id len=51", "BVA_ORD_T",
       "Không hợp lệ", "txn max+1", "POST", "/api/orders/",
       '{"users":[{"username":"ob2","password":"Passw0rd!"}]}', 400, "{}"),
    tc("BVA_ORD_03", '{"customer":"{user_id}","complete":false,"transaction_id":""}',
       "Không hợp lệ — transaction_id blank bị từ chối", "BVA_ORD_T",
       "Không hợp lệ", "txn blank not allowed", "POST", "/api/orders/",
       '{"users":[{"username":"ob3","password":"Passw0rd!"}]}', 400, "{}"),
    tc("BVA_ORD_04", '{"customer":"{user_id}","complete":false,"transaction_id":"T"}',
       "Hợp lệ — transaction_id len=1", "BVA_ORD_T",
       "Hợp lệ", "txn len1", "POST", "/api/orders/",
       '{"users":[{"username":"ob4","password":"Passw0rd!"}]}', 201, "{}"),
    tc("BVA_ORD_05", '{"customer":99999,"complete":false,"transaction_id":"X"}',
       "Không hợp lệ — FK invalid gần biên id", "BVA_ORD_T",
       "Không hợp lệ", "invalid customer", "POST", "/api/orders/", "{}", 400, "{}"),
    tc("BVA_ORD_06", '{}', "Không hợp lệ — GET id không tồn tại", "BVA_ORD_T",
       "Không hợp lệ", "order 404 boundary id", "GET", "/api/orders/99999/", "{}", 404,
       '{"error":"Order not found"}'),
    tc("BVA_ORD_07", '{"customer":"{user_id}","complete":true,"transaction_id":"OK"}',
       "Hợp lệ — complete=true tại biên boolean", "BVA_ORD_T",
       "Hợp lệ", "complete true", "POST", "/api/orders/",
       '{"users":[{"username":"ob7","password":"Passw0rd!"}]}', 201, '{"complete":true}'),
    tc("BVA_ORD_08", '{"customer":"{user_id}","complete":false,"transaction_id":"' + ("Z" * 49) + '"}',
       "Hợp lệ — transaction_id len=49 (max-1)", "BVA_ORD_T",
       "Hợp lệ", "txn max-1", "POST", "/api/orders/",
       '{"users":[{"username":"ob8","password":"Passw0rd!"}]}', 201, "{}"),
]

# OrderItem BVA — id existence edges + quantity extremes stored (8)
BVA_CASES += [
    tc("BVA_OI_01", '{}', "Hợp lệ — list rỗng", "BVA_ORD_T",
       "Hợp lệ", "empty list", "GET", "/api/order-items/", "{}", 200, "[]"),
    tc("BVA_OI_02", '{}', "Hợp lệ — quantity=1 (min thực tế)", "BVA_ORD_T",
       "Hợp lệ", "qty=1", "GET", "/api/order-items/{order_item_id}/",
       '{"users":[{"username":"oib1","password":"Passw0rd!"}],"products":[{"name":"P","price":1}],"orders":[{"customer_username":"oib1"}],"order_items":[{"quantity":1}]}',
       200, '{"quantity":1}'),
    tc("BVA_OI_03", '{}', "Hợp lệ — quantity lớn", "BVA_ORD_T",
       "Hợp lệ", "qty=100", "GET", "/api/order-items/{order_item_id}/",
       '{"users":[{"username":"oib2","password":"Passw0rd!"}],"products":[{"name":"P2","price":1}],"orders":[{"customer_username":"oib2"}],"order_items":[{"quantity":100}]}',
       200, '{"quantity":100}'),
    tc("BVA_OI_04", '{}', "Không hợp lệ — id 99999", "BVA_ORD_T",
       "Không hợp lệ", "not found", "GET", "/api/order-items/99999/", "{}", 404,
       '{"error":"OrderItem not found"}'),
    tc("BVA_OI_05", '{}', "Không hợp lệ — id 0", "BVA_ORD_T",
       "Không hợp lệ", "id 0", "GET", "/api/order-items/0/", "{}", 404, "{}"),
    tc("BVA_OI_06", '{}', "Hợp lệ — quantity=2", "BVA_ORD_T",
       "Hợp lệ", "qty=2", "GET", "/api/order-items/{order_item_id}/",
       '{"users":[{"username":"oib3","password":"Passw0rd!"}],"products":[{"name":"P3","price":1}],"orders":[{"customer_username":"oib3"}],"order_items":[{"quantity":2}]}',
       200, '{"quantity":2}'),
    tc("BVA_OI_07", '{}', "Hợp lệ — list non-empty", "BVA_ORD_T",
       "Hợp lệ", "list", "GET", "/api/order-items/",
       '{"users":[{"username":"oib4","password":"Passw0rd!"}],"products":[{"name":"P4","price":1}],"orders":[{"customer_username":"oib4"}],"order_items":[{"quantity":3}]}',
       200, '[{"quantity":3}]'),
    tc("BVA_OI_08", '{}', "Không hợp lệ — id 88888", "BVA_ORD_T",
       "Không hợp lệ", "not found 2", "GET", "/api/order-items/88888/", "{}", 404,
       '{"error":"OrderItem not found"}'),
]

# Shipping BVA (8+)
BVA_CASES += [
    tc("BVA_SHIP_01", '{"customer":"{user_id}","order":"{order_id}","address":"A1","city":"HN","mobile":"0123456789"}',
       "Hợp lệ — mobile đúng 10 số", "BVA_SHIP_M",
       "Hợp lệ", "mobile exact", "POST", "/api/shipping-addresses/",
       '{"users":[{"username":"sb1","password":"Passw0rd!"}],"orders":[{"customer_username":"sb1"}]}',
       201, '{"mobile":"0123456789"}'),
    tc("BVA_SHIP_02", '{"customer":"{user_id}","order":"{order_id}","address":"A1","city":"HN","mobile":"012345678"}',
       "Không hợp lệ — mobile len=9", "BVA_SHIP_M",
       "Không hợp lệ", "mobile min-1", "POST", "/api/shipping-addresses/",
       '{"users":[{"username":"sb2","password":"Passw0rd!"}],"orders":[{"customer_username":"sb2"}]}',
       400, "{}"),
    tc("BVA_SHIP_03", '{"customer":"{user_id}","order":"{order_id}","address":"A1","city":"HN","mobile":"01234567890"}',
       "Không hợp lệ — mobile len=11", "BVA_SHIP_M",
       "Không hợp lệ", "mobile max+1", "POST", "/api/shipping-addresses/",
       '{"users":[{"username":"sb3","password":"Passw0rd!"}],"orders":[{"customer_username":"sb3"}]}',
       400, "{}"),
    tc("BVA_SHIP_04", '{"customer":"{user_id}","order":"{order_id}","address":"A","city":"HN","mobile":"0912345678"}',
       "Hợp lệ — address len=1 (min)", "BVA_SHIP_A",
       "Hợp lệ", "address min", "POST", "/api/shipping-addresses/",
       '{"users":[{"username":"sb4","password":"Passw0rd!"}],"orders":[{"customer_username":"sb4"}]}',
       201, "{}"),
    tc("BVA_SHIP_05", '{"customer":"{user_id}","order":"{order_id}","address":"","city":"HN","mobile":"0912345678"}',
       "Không hợp lệ — address len=0", "BVA_SHIP_A",
       "Không hợp lệ", "address min-1", "POST", "/api/shipping-addresses/",
       '{"users":[{"username":"sb5","password":"Passw0rd!"}],"orders":[{"customer_username":"sb5"}]}',
       400, "{}"),
    tc("BVA_SHIP_06", '{"customer":"{user_id}","order":"{order_id}","address":"' + ("A" * 200) + '","city":"HN","mobile":"0912345678"}',
       "Hợp lệ — address len=200 (max)", "BVA_SHIP_A",
       "Hợp lệ", "address max", "POST", "/api/shipping-addresses/",
       '{"users":[{"username":"sb6","password":"Passw0rd!"}],"orders":[{"customer_username":"sb6"}]}',
       201, "{}"),
    tc("BVA_SHIP_07", '{"customer":"{user_id}","order":"{order_id}","address":"' + ("A" * 201) + '","city":"HN","mobile":"0912345678"}',
       "Không hợp lệ — address len=201", "BVA_SHIP_A",
       "Không hợp lệ", "address max+1", "POST", "/api/shipping-addresses/",
       '{"users":[{"username":"sb7","password":"Passw0rd!"}],"orders":[{"customer_username":"sb7"}]}',
       400, "{}"),
    tc("BVA_SHIP_08", '{"customer":"{user_id}","order":"{order_id}","address":"City1","city":"H","mobile":"0912345678"}',
       "Hợp lệ — city len=1 (min)", "BVA_SHIP_A",
       "Hợp lệ", "city min", "POST", "/api/shipping-addresses/",
       '{"users":[{"username":"sb8","password":"Passw0rd!"}],"orders":[{"customer_username":"sb8"}]}',
       201, "{}"),
]

# Cart BVA-ish (8) — action/productId edges
BVA_CASES += [
    tc("BVA_CART_01", '{"productId":"{product_id}","action":"add"}',
       "Hợp lệ — action=add", "BVA_SHIP_M",
       "Hợp lệ", "add", "POST", "/update_item/",
       '{"users":[{"username":"cb1","password":"Passw0rd!"}],"products":[{"name":"X","price":1}],"login_as":"cb1"}',
       200, '{"message":"Item updated successfully"}'),
    tc("BVA_CART_02", '{"productId":"{product_id}","action":"remove"}',
       "Hợp lệ — action=remove", "BVA_SHIP_M",
       "Hợp lệ", "remove", "POST", "/update_item/",
       '{"users":[{"username":"cb2","password":"Passw0rd!"}],"products":[{"name":"Y","price":1}],"orders":[{"customer_username":"cb2"}],"order_items":[{"quantity":1}],"login_as":"cb2"}',
       200, '{"message":"Item updated successfully"}'),
    tc("BVA_CART_03", '{"productId":"{product_id}","action":"noop"}',
       "Không hợp lệ — action ngoài miền", "BVA_SHIP_M",
       "Không hợp lệ", "bad action", "POST", "/update_item/",
       '{"users":[{"username":"cb3","password":"Passw0rd!"}],"products":[{"name":"Z","price":1}],"login_as":"cb3"}',
       400, '{"error":"action must be add or remove"}'),
    tc("BVA_CART_04", '{"productId":99999,"action":"add"}',
       "Không hợp lệ — productId biên ngoài", "BVA_SHIP_M",
       "Không hợp lệ", "missing product", "POST", "/update_item/",
       '{"users":[{"username":"cb4","password":"Passw0rd!"}],"login_as":"cb4"}',
       404, '{"error":"Product not found"}'),
    tc("BVA_CART_05", '{"productId":0,"action":"add"}',
       "Không hợp lệ — productId=0", "BVA_SHIP_M",
       "Không hợp lệ", "id 0", "POST", "/update_item/",
       '{"users":[{"username":"cb5","password":"Passw0rd!"}],"login_as":"cb5"}',
       404, "{}"),
    tc("BVA_CART_06", '{"productId":"{product_id}","action":""}',
       "Không hợp lệ — action rỗng", "BVA_SHIP_M",
       "Không hợp lệ", "empty action", "POST", "/update_item/",
       '{"users":[{"username":"cb6","password":"Passw0rd!"}],"products":[{"name":"Q","price":1}],"login_as":"cb6"}',
       400, "{}"),
    tc("BVA_CART_07", '{"productId":"{product_id}","action":"add"}',
       "Không hợp lệ — anonymous", "BVA_SHIP_M",
       "Không hợp lệ", "auth boundary", "POST", "/update_item/",
       '{"products":[{"name":"R","price":1}]}', 401, '{"error":"Authentication required"}'),
    tc("BVA_CART_08", '{"action":"add"}',
       "Không hợp lệ — thiếu productId", "BVA_SHIP_M",
       "Không hợp lệ", "missing productId", "POST", "/update_item/",
       '{"users":[{"username":"cb8","password":"Passw0rd!"}],"login_as":"cb8"}',
       400, "{}"),
]


def write_book(path: Path, title: str, conditions: list, cases: list) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    ws["A1"] = title
    ws["A2"] = "Sheet Conditions: mau phan vung / bien + Tag"
    ws["A3"] = "Sheet TestCases: Test Case | Input | Expected Outcome | New Tags Covered (+ cot chay tu dong)"
    ws["A4"] = f"So testcase: {len(cases)}"
    ws["A5"] = "Moi chuc nang >= 8 TC; co hop le + khong hop le; co tag; expected ghi ro ly do"

    ws = wb.create_sheet("Conditions")
    for r in conditions:
        ws.append(r)
    bold(ws)

    ws = wb.create_sheet("TestCases")
    ws.append(TC_HEADERS)
    bold(ws)
    for r in cases:
        ws.append(r)

    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    print(f"Wrote {path} cases={len(cases)}")


def main() -> None:
    write_book(EP_OUT, "Equivalence Partitioning (EP) Test Design", EP_CONDITIONS, EP_CASES)
    write_book(BVA_OUT, "Boundary Value Analysis (BVA) Test Design", BVA_CONDITIONS, BVA_CASES)


if __name__ == "__main__":
    main()
