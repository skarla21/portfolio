export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  modules: ['@nuxtjs/tailwindcss', '@nuxt/eslint'],
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      htmlAttrs: { lang: 'el' },
      title: 'Αντώνης Σκαρλάτος (Antonis Skarlatos)',
      meta: [
        {
          name: 'description',
          content:
            'Αντώνης Σκαρλάτος (Antonis Skarlatos). Προγραμματιστής, αναλυτής δεδομένων και φυσικός στην Αθήνα.',
        },
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32.png' },
        { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' },
      ],
    },
  },
})
