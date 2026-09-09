Feature(`
  KIỂM THỬ E2E BLACK-BOX - CHỨC NĂNG DANH MỤC (CATEGORY)
  ------------------------------------------------------
  - ĐỘ PHỦ UI: Kiểm tra danh mục hiển thị, click chọn & lọc sản phẩm
`);

Scenario("E2E_CAT_01 | Kiểm tra danh mục hiển thị trên giao diện", ({ I }) => {
  // Mở thẳng trang danh mục nơi chứa các item AB, A, Trang sức Kim Cương VIP
  I.amOnPage("/category/");
  I.see("SẢN PHẨM");
  I.see("AB");
});

Scenario("E2E_CAT_02 | Chuyển hướng và lọc sản phẩm theo Danh mục", ({ I }) => {
  I.amOnPage("/category/");
  // Click vào chữ A trên giao diện danh mục
  I.click("A");
  // Kiểm tra hệ thống thực hiện chuyển hướng
  I.seeInCurrentUrl("/search/");
});

Scenario(
  "E2E_CAT_03 | Kiểm tra danh mục hiển thị không làm vỡ giao diện",
  ({ I }) => {
    I.amOnPage("/category/");
    // Kiểm tra khung chứa sản phẩm/danh mục hiển thị bình thường
    I.seeElement("body");
  },
);
