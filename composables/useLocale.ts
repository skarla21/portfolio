import { copies, type Locale } from '~/content/site'
import {
  localeFromPath,
  switchLocalePath,
  withLocale,
} from '~/utils/localePath'

export function useLocale() {
  const route = useRoute()
  const stored = useCookie<Locale>('locale', {
    default: () => 'el',
    maxAge: 60 * 60 * 24 * 365,
    sameSite: 'lax',
  })
  /** Last language chosen via the toggle (survives URL-mirrored `locale` cookie). */
  const prefer = useCookie<Locale | ''>('localePrefer', {
    default: () => '',
    maxAge: 60 * 60 * 24 * 365,
    sameSite: 'lax',
  })

  const locale = computed<Locale>(() => localeFromPath(route.path))
  const copy = computed(() => copies[locale.value])

  // One-time: old cookie-only English preference while URL is Greek.
  if (!prefer.value && stored.value === 'en' && locale.value === 'el') {
    prefer.value = 'en'
  }

  watch(
    locale,
    (next) => {
      if (stored.value !== next) stored.value = next
    },
    { immediate: true },
  )

  function localePath(path: string) {
    return withLocale(path, locale.value)
  }

  function alternatePath() {
    return switchLocalePath(route.fullPath)
  }

  async function setLocale(next: Locale) {
    if (next === locale.value) return
    prefer.value = next
    stored.value = next
    const target = switchLocalePath(route.path)
    const hash = route.hash || ''
    await navigateTo(`${target}${hash}`)
  }

  return { locale, copy, localePath, alternatePath, setLocale, prefer }
}
