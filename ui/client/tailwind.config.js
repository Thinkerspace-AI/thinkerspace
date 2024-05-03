/** @type {import('tailwindcss').Config} */
export default {
  mode: 'jit',
  content: ["./src/**/*.{html,js,svelte,ts}"],
  theme: {
    extend: {
      fontFamily: { 
        domine: ['Domine'],
        inter: ['Inter'],
      },
      colors: {
        Tyellow: {
          100: '#fcc454',
        },
        Tpurple: {
          100: '#3c3748',
        },
      },
    },
  },
  plugins: [],
}

