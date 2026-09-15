Feature('UI - Giỏ hàng / Thanh toán / Liên hệ');

Scenario('CART_01 | Trang giỏ hàng (chưa login) mở được', ({ I }) => {
  I.amOnPage('/cart/');
  I.see('Giỏ Hàng');
  I.see('Tiếp Tục Mua Sắm');
  I.seeElement(locate('a[href="/payment/"] button').withText('Thanh Toán'));
});

Scenario('CART_02 | Đăng nhập rồi thêm sản phẩm vào giỏ', ({ I }) => {
  I.loginAs('e2e_user', 'Passw0rd!23');
  I.amOnPage('/product/');
  I.click(locate('.update-cart').first());
  I.wait(2);
  I.amOnPage('/cart/');
  I.see('Nhan Bac Test');
  I.seeElement('.update-cart');
});

Scenario('PAY_01 | Form thanh toán hiển thị đủ field', ({ I }) => {
  I.amOnPage('/payment/');
  I.seeElement('#cardName');
  I.seeElement('#cardNumber');
  I.seeElement('#expirationDate');
  I.seeElement('#cvv');
  I.seeElement('#billingAddress');
  I.seeElement('#shippingAddress');
  I.seeElement('#phoneNumber');
  I.fillField('#cardName', 'E2E Tester');
  I.fillField('#cardNumber', '4111111111111111');
  I.fillField('#cvv', '123');
  I.fillField('#billingAddress', '1 Nguyen Hue');
  I.fillField('#shippingAddress', '1 Nguyen Hue');
  I.fillField('#phoneNumber', '0909123456');
  I.seeElement('button[type="submit"]');
});

Scenario('CONTACT_01 | Trang liên hệ', ({ I }) => {
  I.amOnPage('/contact/');
  I.see('Thông Tin Liên Hệ');
  I.see('Địa Chỉ Cửa Hàng');
  I.see('JEWELRY STORE IN SAIGON');
});

Scenario('FLOW_01 | Luồng mua: login -> product -> cart -> payment', ({ I }) => {
  I.loginAs('e2e_user', 'Passw0rd!23');
  I.amOnPage('/product/');
  I.see('Nhan Bac Test');
  I.click(locate('.card a[href="/cart/"] button').withText('Mua ngay').first());
  I.seeInCurrentUrl('/cart');
  I.click(locate('a[href="/payment/"] button').withText('Thanh Toán'));
  I.seeInCurrentUrl('/payment');
  I.seeElement('#cardName');
});
