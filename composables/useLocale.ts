import { copies, type Locale } from '~/content/site'

export function useLocale() {
  const stored = useCookie<Locale>('locale', {
    default: () => 'el',
    maxAge: 60 * 60 * 24 * 365,
    sameSite: 'lax',
  })

  const locale = computed<Locale>(() => (stored.value === 'en' ? 'en' : 'el'))
  const copy = computed(() => copies[locale.value])

  function setLocale(next: Locale) {
    stored.value = next
  }

  return { locale, copy, setLocale }
}
