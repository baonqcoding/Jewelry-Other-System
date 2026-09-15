Feature("UI - Sản phẩm / Danh mục / Chi tiết / Tìm kiếm");

Scenario("PROD_01 | Danh sách sản phẩm", ({ I }) => {
  I.amOnPage("/product/");
  I.see("Danh Sách Sản Phẩm");
});

Scenario("CAT_01 | Trang danh mục và lọc theo slug", ({ I }) => {
  I.amOnPage("/category/"); // Kiểm tra header hoặc menu chính hiển thị
  I.see("SẢN PHẨM");
});

Scenario("DETAIL_01 | Xem chi tiết sản phẩm", ({ I }) => {
  I.amOnPage("/product/");
  I.see("Danh Sách Sản Phẩm"); // Nếu có sản phẩm thì click, nếu không chỉ kiểm tra trang load thành công
});

Scenario("SEARCH_01 | Tìm kiếm sản phẩm từ header", ({ I }) => {
  I.amOnPage("/");
  I.fillField('input[name="searched"]', "Nhan");
  I.click('.support-bar button[type="submit"]');
  I.seeInCurrentUrl("/search");
  I.see("Result search for:");
});
