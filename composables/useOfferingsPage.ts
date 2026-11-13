import { offeringsByLocale } from '~/content/offerings'
import {
  faqJsonLd,
  homeJsonLd,
  servicesJsonLd,
} from '~/content/schema'
import { useLocale } from '~/composables/useLocale'
import { useSiteSeo } from '~/composables/useSiteSeo'

type OfferingsPage = 'home' | 'services' | 'faq'

const jsonLdByPage = {
  home: homeJsonLd,
  services: servicesJsonLd,
  faq: faqJsonLd,
} as const

/** Shared SEO + JSON-LD wiring for locale page shells (EL and EN route files). */
export function useOfferingsPage(page: OfferingsPage) {
  const { locale } = useLocale()
  const seo = computed(() => offeringsByLocale[locale.value].pageSeo[page])

  useSiteSeo({
    page,
    title: () => seo.value.title,
    description: () => seo.value.description,
    jsonLd: () => jsonLdByPage[page](locale.value),
    ogType: page === 'home' ? 'profile' : undefined,
  })
}
