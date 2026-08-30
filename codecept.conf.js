/** @type {CodeceptJS.MainConfig} */
export const config = {
  tests: "./tests/*_test.js",
  output: "./output",
  helpers: {
    Playwright: {
      browser: "chromium",
      url: "http://localhost:8000",
      show: true,
    },
  },
  include: {
    I: "./steps_file.js",
  },
  noGlobals: true,
  plugins: {},
  name: "website_django",
};
