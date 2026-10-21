import type { Config } from 'tailwindcss'

export default {
  content: [
    './app.vue',
    './pages/**/*.vue',
    './components/**/*.vue',
  ],
  theme: {
    extend: {
      colors: {
        paper: '#f3efe4',
        mist: '#e3ebe7',
        ink: '#14120e',
        night: '#10131c',
        mute: '#3c3832',
        lime: '#d6f26a',
        iris: '#c4b5fd',
        clay: '#ffb088',
        'night-soft': '#c9c2b6',
      },
      fontFamily: {
        sans: ['"Source Sans 3"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        serif: ['"Source Serif 4"', 'Georgia', 'serif'],
      },
    },
  },
} satisfies Config
