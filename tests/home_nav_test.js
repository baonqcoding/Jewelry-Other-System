Feature('UI - Trang chủ & Điều hướng');

Scenario('HOME_01 | Mở trang chủ và thấy brand', ({ I }) => {
  I.amOnPage('/');
  I.seeElement('.menu');
  I.see('TRANG CHỦ');
  I.see('KAIJEWELRY');
});

Scenario('NAV_01 | Menu sang Sản phẩm / Giỏ hàng / Liên hệ', ({ I }) => {
  I.amOnPage('/');
  I.click('SẢN PHẨM');
  I.seeInCurrentUrl('/product');
  I.amOnPage('/');
  I.click('GIỎ HÀNG');
  I.seeInCurrentUrl('/cart');
  I.amOnPage('/');
  I.click('LIÊN HỆ');
  I.seeInCurrentUrl('/contact');
});
