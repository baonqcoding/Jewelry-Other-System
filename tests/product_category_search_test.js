Feature('UI - Sản phẩm / Danh mục / Chi tiết / Tìm kiếm');

Scenario('PROD_01 | Danh sách sản phẩm', ({ I }) => {
  I.amOnPage('/product/');
  I.see('Danh Sách Sản Phẩm');
  I.see('Nhan Bac Test');
  I.seeElement('.update-cart');
});

Scenario('CAT_01 | Trang danh mục và lọc theo slug', ({ I }) => {
  I.amOnPage('/category/');
  I.seeElement('.navbar-nav');
  I.seeElement(locate('.nav-link').withText('Nhan Bac'));
  I.click(locate('.nav-link').withText('Nhan Bac'));
  I.seeInCurrentUrl('/category/');
  I.seeInCurrentUrl('category=nhan-bac');
  I.see('Nhan Bac Test');
});

Scenario('DETAIL_01 | Xem chi tiết sản phẩm', ({ I }) => {
  I.amOnPage('/product/');
  I.click(locate('.card a[href*="/detail/"]').first());
  I.seeInCurrentUrl('/detail/');
  // detail.html dùng class text-uppercase cho tên SP và nút
  I.see('NHAN BAC TEST');
  I.see('THÊM VÀO GIỎ');
  I.see('Quay lại');
});

Scenario('SEARCH_01 | Tìm kiếm sản phẩm từ header', ({ I }) => {
  I.amOnPage('/');
  I.fillField('input[name="searched"]', 'Nhan');
  I.click('.support-bar button[type="submit"]');
  I.seeInCurrentUrl('/search');
  I.see('Nhan Bac Test');
});
