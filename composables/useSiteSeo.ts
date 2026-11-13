import { share, siteUrl, type Locale } from '~/content/site'
import { withLocale } from '~/utils/localePath'
import { useLocale } from '~/composables/useLocale'

type PageKey = 'home' | 'services' | 'faq'

const pagePaths: Record<PageKey, string> = {
  home: '/',
  services: '/services',
  faq: '/faq',
}

export function useSiteSeo(options: {
  page: PageKey
  title: MaybeRefOrGetter<string>
  description: MaybeRefOrGetter<string>
  jsonLd: MaybeRefOrGetter<Record<string, unknown>>
  ogType?: string
}) {
  const { locale } = useLocale()
  const path = pagePaths[options.page]

  const canonical = computed(
    () => `${siteUrl}${withLocale(path, locale.value)}`,
  )
  const elUrl = computed(() => `${siteUrl}${withLocale(path, 'el')}`)
  const enUrl = computed(() => `${siteUrl}${withLocale(path, 'en')}`)
  const title = computed(() => toValue(options.title))
  const description = computed(() => toValue(options.description))
  const ogLocale = computed(() =>
    locale.value === 'el' ? 'el_GR' : 'en_US',
  )
  const ogLocaleAlt = computed(() =>
    locale.value === 'el' ? 'en_US' : 'el_GR',
  )

  useSeoMeta({
    title,
    description,
    ogTitle: title,
    ogDescription: description,
    ogImage: share.image,
    ogImageAlt: title,
    ogImageWidth: 1200,
    ogImageHeight: 630,
    ogUrl: canonical,
    ogType: options.ogType ?? 'website',
    ogLocale,
    twitterCard: 'summary_large_image',
    twitterTitle: title,
    twitterDescription: description,
    twitterImage: share.image,
    twitterImageAlt: title,
  })

  useHead({
    link: () => [
      { rel: 'canonical', href: canonical.value },
      { rel: 'alternate', hreflang: 'el', href: elUrl.value },
      { rel: 'alternate', hreflang: 'en', href: enUrl.value },
      { rel: 'alternate', hreflang: 'x-default', href: elUrl.value },
    ],
    meta: () => [
      { property: 'og:locale:alternate', content: ogLocaleAlt.value },
    ],
    script: () => [
      {
        key: `ld-${options.page}`,
        type: 'application/ld+json',
        innerHTML: JSON.stringify(toValue(options.jsonLd)),
      },
    ],
  })
}

export function absoluteLocaleUrl(path: string, locale: Locale) {
  return `${siteUrl}${withLocale(path, locale)}`
}
