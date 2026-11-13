export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: false },
  modules: ["@nuxtjs/tailwindcss", "@nuxt/eslint"],
  css: ["~/assets/css/main.css"],
  app: {
    head: {
      htmlAttrs: { lang: "el" },
      title:
        "Αντώνης Σκαρλάτος | Υπηρεσίες πληροφορικής & ανάπτυξη website Αθήνα",
      meta: [
        {
          name: "description",
          content:
            "Παροχή υπηρεσιών πληροφορικής και λογισμικού στην Αθήνα: ανάπτυξη ιστοσελίδων, e-shops, εφαρμογές, συμβουλές, QR/NFC και SEO & AEO.",
        },
        {
          name: "google-site-verification",
          content: "Wd7xFHb156XpM3AuDzsTmWJ9IxFTnssYqb0kULsb_EE",
        },
      ],
      link: [
        { rel: "icon", type: "image/svg+xml", href: "/favicon.svg" },
        {
          rel: "icon",
          type: "image/png",
          sizes: "32x32",
          href: "/favicon-32.png",
        },
        {
          rel: "apple-touch-icon",
          sizes: "180x180",
          href: "/apple-touch-icon.png",
        },
      ],
    },
  },
});
