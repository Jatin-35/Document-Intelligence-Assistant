/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "oklch(0.922 0 0)",
        ring: "oklch(0.708 0 0)",
        background: "oklch(1 0 0)",
        foreground: "oklch(0.145 0 0)",
      },
    },
  },
  plugins: [
    require("tailwindcss-animate"),
  ],
};
