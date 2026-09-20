@type {import('tailwindcss').Config} 
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eef4ff", 100: "#d9e6ff", 300: "#93b4ff", 500: "#3b6bff",
          600: "#2451e0", 700: "#1d3fb3", 900: "#0f1f5c",
        },
      },
    },
  },
  plugins: [],
};
