Feature("Kiểm tra giao diện hệ thống Jewelry");

Scenario("Kiểm tra truy cập trang chủ", ({ I }) => {
  I.amOnPage("/");
  I.seeInTitle(""); // Kiểm tra trang chủ load thành công
});
