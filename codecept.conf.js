const showBrowser = process.env.SHOW_BROWSER !== 'false' && process.env.CI !== 'true';

exports.config = {
  tests: './tests/*_test.js',
  output: './output',
  helpers: {
    Playwright: {
      url: process.env.BASE_URL || 'http://127.0.0.1:8000',
      show: showBrowser,
      browser: 'chromium',
      waitForTimeout: 10000,
      waitForNavigation: 'load',
    },
  },
  include: {
    I: './steps_file.js',
  },
  name: 'Jewelry UI E2E',
};
