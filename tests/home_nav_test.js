Feature('UI - Trang chủ & Điều hướng');

Scenario('HOME_01 | Mở trang chủ và thấy brand', ({ I }) => {
  I.amOnPage('/');
  I.seeElement('.menu');
  I.seeElement(locate('.menu-pages').withText('TRANG CHỦ'));
  I.seeElement('.footer');
  I.see('JEWELRY STORE IN SAIGON');
});

Scenario('NAV_01 | Menu sang Sản phẩm / Giỏ hàng / Liên hệ', ({ I }) => {
  I.amOnPage('/');
  I.click(locate('.menu a').withText('SẢN PHẨM'));
  I.seeInCurrentUrl('/product');
  I.amOnPage('/');
  I.click(locate('.menu a').withText('GIỎ HÀNG'));
  I.seeInCurrentUrl('/cart');
  I.amOnPage('/');
  I.click(locate('.menu a').withText('LIÊN HỆ'));
  I.seeInCurrentUrl('/contact');
});
