exports.config = {
  tests: "./tests/*_test.js",
  output: "./output",
  helpers: {
    Playwright: {
      url: "http://localhost:8000",
      show: true,
      browser: "chromium",
    },
  },
  include: {
    I: "./steps_file.js",
  },
  bootstrap: null,
  mocha: {},
  name: "web_trangsuc",
  dontFailOnEmptyRun: true, // <--- Thêm dòng này vào đây
};
