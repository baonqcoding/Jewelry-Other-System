Feature("Kiểm tra giao diện hệ thống Jewelry");

Scenario("Kiểm tra truy cập trang chủ", ({ I }) => {
  I.amOnPage("/");
  I.seeInTitle(""); // Kiểm tra trang chủ load thành công
});

Feature("Chức năng Đăng Nhập");

Scenario("Đăng nhập thành công với tài khoản hợp lệ", ({ I }) => {
  I.amOnPage("/login"); // Hoặc URL trang login của bạn
  I.fillField("username", "admin");
  I.fillField("password", "123456");
  I.click("Đăng nhập");
  I.see("Xin chào"); // Kiểm tra thông báo hoặc giao diện sau đăng nhập
});

Feature("Chức năng Sản phẩm");

Scenario("Xem chi tiết một sản phẩm trang sức", ({ I }) => {
  I.amOnPage("/");
  I.click("Trang sức Kim Cương"); // Click vào tên sản phẩm/danh mục
  I.seeInCurrentUrl("/product");
  I.see("Thêm vào giỏ hàng");
});
