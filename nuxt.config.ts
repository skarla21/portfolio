export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      htmlAttrs: { lang: 'el' },
      title: 'Αντώνης Σκαρλάτος',
      meta: [
        { name: 'description', content: 'Προγραμματιστής, αναλυτής δεδομένων και φυσικός στην Αθήνα.' },
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
      ],
    },
  },
})
