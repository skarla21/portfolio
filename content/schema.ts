import { contact, siteUrl } from './site'
import { offeringsByLocale } from './offerings'
import { withLocale } from '~/utils/localePath'
import type { Locale } from './site'

const orgId = `${siteUrl}/#business`
const personId = `${siteUrl}/#person`
const websiteId = `${siteUrl}/#website`
const employerId = `${siteUrl}/#employer-factset`

export function personEntity() {
  return {
    '@type': 'Person',
    '@id': personId,
    name: 'Antonis Skarlatos',
    alternateName: 'Αντώνης Σκαρλάτος',
    jobTitle: [
      'Web Developer',
      'Data analyst',
      'Physicist',
      'IT services provider',
    ],
    worksFor: {
      '@type': 'Organization',
      '@id': employerId,
      name: 'FactSet',
    },
    owns: { '@id': orgId },
    address: {
      '@type': 'PostalAddress',
      addressLocality: 'Athens',
      postalCode: '16232',
      addressCountry: 'GR',
    },
    email: contact.email,
    telephone: contact.phone,
    sameAs: [contact.linkedin, contact.github],
    url: siteUrl,
    knowsAbout: [
      'Website development',
      'Web applications',
      'SEO',
      'AEO',
      'Data analytics',
      'Vue.js',
      'Nuxt',
      'React',
      'Next.js',
    ],
  }
}

export function professionalServiceEntity(locale: Locale) {
  const offerings = offeringsByLocale[locale]
  return {
    '@type': 'ProfessionalService',
    '@id': orgId,
    name:
      locale === 'el'
        ? 'Αντώνης Σκαρλάτος — Υπηρεσίες πληροφορικής'
        : 'Antonis Skarlatos — IT & software services',
    alternateName: offerings.servicesTagline,
    description: offerings.servicesPageLede,
    url: `${siteUrl}${withLocale('/services', locale)}`,
    image: `${siteUrl}/og.png`,
    email: contact.email,
    telephone: contact.phone,
    address: {
      '@type': 'PostalAddress',
      addressLocality: 'Athens',
      postalCode: '16232',
      addressCountry: 'GR',
    },
    areaServed: {
      '@type': 'Country',
      name: 'Greece',
    },
    sameAs: [contact.linkedin, contact.github],
    founder: { '@id': personId },
    employee: { '@id': personId },
    knowsAbout: offerings.offerings.map((item) => item.title),
    makesOffer: offerings.offerings.map((item) => ({
      '@type': 'Offer',
      itemOffered: {
        '@type': 'Service',
        name: item.title,
        description: item.summary,
        provider: { '@id': orgId },
        areaServed: 'GR',
      },
    })),
  }
}

function websiteEntity(locale: Locale) {
  return {
    '@type': 'WebSite',
    '@id': websiteId,
    url: siteUrl,
    name: 'Antonis Skarlatos',
    inLanguage: ['el-GR', 'en-US'],
    publisher: { '@id': orgId },
    about: { '@id': personId },
    mainEntityOfPage: `${siteUrl}${withLocale('/', locale)}`,
  }
}

export function homeJsonLd(locale: Locale) {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'ProfilePage',
        '@id': `${siteUrl}${withLocale('/', locale)}#page`,
        url: `${siteUrl}${withLocale('/', locale)}`,
        inLanguage: locale === 'el' ? 'el-GR' : 'en-US',
        isPartOf: { '@id': websiteId },
        mainEntity: { '@id': personId },
        about: { '@id': orgId },
      },
      websiteEntity(locale),
      personEntity(),
      professionalServiceEntity(locale),
    ],
  }
}

export function servicesJsonLd(locale: Locale) {
  const offerings = offeringsByLocale[locale]
  const pageUrl = `${siteUrl}${withLocale('/services', locale)}`
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'CollectionPage',
        '@id': `${pageUrl}#page`,
        url: pageUrl,
        name: offerings.servicesPageTitle,
        description: offerings.pageSeo.services.description,
        inLanguage: locale === 'el' ? 'el-GR' : 'en-US',
        isPartOf: { '@id': websiteId },
        mainEntity: offerings.offerings.map((item) => ({
          '@type': 'Service',
          '@id': `${pageUrl}#${item.id}`,
          name: item.title,
          description: item.body,
          provider: { '@id': orgId },
          areaServed: 'GR',
        })),
      },
      websiteEntity(locale),
      personEntity(),
      professionalServiceEntity(locale),
    ],
  }
}

export function faqJsonLd(locale: Locale) {
  const offerings = offeringsByLocale[locale]
  const pageUrl = `${siteUrl}${withLocale('/faq', locale)}`
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebPage',
        '@id': `${pageUrl}#page`,
        url: pageUrl,
        name: offerings.faqTitle,
        description: offerings.pageSeo.faq.description,
        inLanguage: locale === 'el' ? 'el-GR' : 'en-US',
        isPartOf: { '@id': websiteId },
        about: { '@id': orgId },
      },
      websiteEntity(locale),
      personEntity(),
      professionalServiceEntity(locale),
    ],
  }
}

/** @deprecated Prefer homeJsonLd — kept for any legacy imports */
export const profilePage = {
  '@context': 'https://schema.org',
  '@type': 'ProfilePage',
  url: siteUrl,
  mainEntity: personEntity(),
}
