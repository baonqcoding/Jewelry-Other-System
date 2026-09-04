/** @type {CodeceptJS.MainConfig} */
export const config = {
  tests: "./tests/*_test.js",
  output: "./output",
  helpers: {
    Playwright: {
      browser: "chromium",
      url: "http://localhost:8000",
      show: false,
    },
  },
  include: {
    I: "./steps_file.js",
  },
  mocha: {
    reporterOptions: {
      reportDir: "output",
      reportFilename: "BVA_Test_Report",
      reportTitle: "BÁO CÁO KIỂM THỬ BVA VÀ ĐỘ PHỦ LỚP TƯƠNG ĐƯƠNG",
      inlineAssets: true,
    },
  },
  noGlobals: true,
  plugins: {},
  name: "website_django",
};
