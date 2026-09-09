Feature("Kiểm tra giao diện hệ thống Jewelry");

Scenario("Kiểm tra truy cập trang chủ", ({ I }) => {
  I.amOnPage("/");
  I.see("KAIJEWELRY"); // Kiểm tra tên thương hiệu hiển thị trên trang chủ
});

Feature("Chức năng Đăng Nhập");

Scenario("Đăng nhập hệ thống", ({ I }) => {
  I.amOnPage("/login");
  I.fillField("User Name", "admin"); // Tên nhãn đúng trong HTML của bạn
  I.fillField("Password", "123456");
  I.click("Login"); // Tên nút đúng trên giao diện

  // Nếu đăng nhập đúng sẽ chuyển trang, nếu chưa tạo admin bạn kiểm tra nút Login hoạt động:
  I.dontSeeInCurrentUrl("/login");
});

Feature("Chức năng Sản phẩm");

Scenario("Xem danh mục sản phẩm", ({ I }) => {
  I.amOnPage("/");
  I.click("SẢN PHẨM"); // Bấm vào menu SẢN PHẨM có sẵn trên thanh Navigation
  I.seeInCurrentUrl("/product"); // Hoặc URL tương ứng trang sản phẩm
});
