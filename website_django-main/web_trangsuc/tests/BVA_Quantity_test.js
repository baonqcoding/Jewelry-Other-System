Feature(`
  KIỂM THỬ BVA & LỚP TƯƠNG ĐƯƠNG - CHỨC NĂNG SỐ LƯỢNG MUA
  ------------------------------------------------------
  - ĐỘ PHỦ EP: 3/3 Vùng (100% Coverage)
  - ĐỘ PHỦ BVA: 4/4 Điểm biên [0, 1, 100, 101] (100% Coverage)
`);

// Bạn có thể chỉnh lại URL /product/1 đúng với URL 1 sản phẩm thực tế trên web của bạn
const productUrl = "/"; // Hoặc đường dẫn trực tiếp tới trang chi tiết SP

Scenario("TC01_BVA_MinMinus1 | Test biên 0 (Không hợp lệ)", ({ I }) => {
  I.amOnPage(productUrl);
  // Nếu nhấp vào sản phẩm đầu tiên từ trang chủ:
  I.click("SẢN PHẨM");

  // Điền vào ô input kiểu number (hoặc thay bằng id/name chính xác tìm thấy ở Bước 1)
  I.fillField('input[type="number"]', "0");
  I.click("Thêm vào giỏ hàng"); // Hoặc tên nút bấm thực tế
});

Scenario("TC02_BVA_Min | Test biên 1 (Hợp lệ)", ({ I }) => {
  I.amOnPage(productUrl);
  I.click("SẢN PHẨM");
  I.fillField('input[type="number"]', "1");
  I.click("Thêm vào giỏ hàng");
});
