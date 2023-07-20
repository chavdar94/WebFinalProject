/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')

module.exports = {
  content: [
    "./src/**/*.{html,js}",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        ...colors,
      },
      width: {
        '11/13': '88.666667%',
      }
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}

