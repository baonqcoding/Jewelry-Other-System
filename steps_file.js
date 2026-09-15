module.exports = function () {
  return actor({
    loginAs(username, password) {
      this.amOnPage('/login/');
      this.fillField('input[name="username"]', username);
      this.fillField('input[name="password"]', password);
      this.click(locate('button[type="submit"]').withText('Login'));
      this.dontSeeInCurrentUrl('/login');
    },
  });
};
