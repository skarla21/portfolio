import type { Locale } from '~/content/site'

export function localeFromPath(path: string): Locale {
  const clean = path.split('?')[0]?.split('#')[0] || '/'
  return clean === '/en' || clean.startsWith('/en/') ? 'en' : 'el'
}

export function stripLocalePrefix(path: string): string {
  const clean = path.split('?')[0]?.split('#')[0] || '/'
  if (clean === '/en') return '/'
  if (clean.startsWith('/en/')) {
    const rest = clean.slice(3)
    return rest.startsWith('/') ? rest : `/${rest}`
  }
  return clean || '/'
}

/** Prefix a locale-free path (`/` or `/services`) for `el` or `en`. */
export function withLocale(path: string, locale: Locale): string {
  const raw = path.startsWith('/') ? path : `/${path}`
  const bare = raw === '/' ? '/' : raw.replace(/\/+$/, '') || '/'
  if (locale === 'el') return bare
  if (bare === '/') return '/en'
  return `/en${bare}`
}

export function switchLocalePath(path: string): string {
  const locale = localeFromPath(path)
  return withLocale(stripLocalePrefix(path), locale === 'el' ? 'en' : 'el')
}

export const sitePaths = ['/', '/services', '/faq'] as const

export type SitePath = (typeof sitePaths)[number]
