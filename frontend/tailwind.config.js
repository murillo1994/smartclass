/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        gold: {
          50: '#fbf9f4',
          100: '#f4ede1',
          200: '#e5d7bc',
          300: '#d0b98f',
          400: '#bfa06b',
          500: '#a6824c', // primary premium gold
          600: '#8e693b',
          700: '#70502f',
          800: '#5c4128',
          900: '#4c3522',
        },
        luxury: {
          black: '#0a0d10',
          dark: '#12161b',
          card: '#1a1f26',
          border: '#2a323d',
          gold: '#c5a880',
          accent: '#eae3d2'
        }
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'sans-serif'],
        serif: ['Playfair Display', 'serif'],
      }
    },
  },
  plugins: [],
}
