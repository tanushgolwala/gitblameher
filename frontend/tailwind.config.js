/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      backgroundImage: {
        "text-gradient":
          "linear-gradient(90deg, rgba(249, 113, 135, 1) 0%, rgba(169, 138, 247, 1) 100%)",
      },
    },
  },
  plugins: [],
};
