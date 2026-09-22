Feature('UI - Đăng ký / Đăng nhập / Đăng xuất');

Scenario('AUTH_01 | Trang đăng ký hiển thị form', ({ I }) => {
  I.amOnPage('/register/');
  I.see('Sign up');
  I.seeElement('input[name="username"]');
  I.seeElement('input[name="email"]');
  I.seeElement('input[name="password1"]');
  I.seeElement('input[name="password2"]');
  I.seeElement(locate('button[type="submit"]').withText('Register'));
});

Scenario('AUTH_02 | Đăng ký tài khoản mới thành công', ({ I }) => {
  const suffix = Date.now().toString().slice(-8);
  I.amOnPage('/register/');
  I.fillField('input[name="username"]', `u${suffix}`);
  I.fillField('input[name="email"]', `u${suffix}@example.com`);
  I.fillField('input[name="first_name"]', 'Ui');
  I.fillField('input[name="last_name"]', 'Test');
  I.fillField('input[name="password1"]', 'Passw0rd!23');
  I.fillField('input[name="password2"]', 'Passw0rd!23');
  I.click(locate('button[type="submit"]').withText('Register'));
  I.seeInCurrentUrl('/login');
});

Scenario('AUTH_03 | Đăng nhập sai giữ nguyên /login và báo lỗi', ({ I }) => {
  I.amOnPage('/login/');
  I.fillField('input[name="username"]', 'e2e_user');
  I.fillField('input[name="password"]', 'wrong-pass');
  I.click(locate('button[type="submit"]').withText('Login'));
  I.seeInCurrentUrl('/login');
  I.see('User or password not correct');
});

Scenario('AUTH_04 | Đăng nhập đúng bằng e2e_user', ({ I }) => {
  I.loginAs('e2e_user', 'Passw0rd!23');
  I.seeInCurrentUrl('/');
  I.see('hello!');
});

Scenario('AUTH_05 | Đăng xuất về trang login', ({ I }) => {
  I.loginAs('e2e_user', 'Passw0rd!23');
  I.click('a[href="/logout/"]');
  I.seeInCurrentUrl('/login');
});
