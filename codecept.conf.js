const showBrowser = process.env.SHOW_BROWSER !== 'false' && process.env.CI !== 'true';

exports.config = {
  tests: './tests/*_test.js',
  output: './output',
  helpers: {
    Playwright: {
      url: process.env.BASE_URL || 'http://127.0.0.1:8000',
      show: showBrowser,
      browser: 'chromium',
      waitForTimeout: 15000,
      waitForNavigation: 'load',
      chromium: {
        args: ['--no-sandbox', '--disable-dev-shm-usage'],
      },
    },
  },
  include: {
    I: './steps_file.js',
  },
  name: 'Jewelry UI E2E',
};
