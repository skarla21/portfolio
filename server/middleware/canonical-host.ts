import { legacyProductionHost, siteUrl } from '../../content/site'

export default defineEventHandler((event) => {
  const forwarded = getRequestHeader(event, 'x-forwarded-host')
  const hostHeader = getRequestHeader(event, 'host')
  const host = (forwarded || hostHeader || '').split(',')[0].trim().split(':')[0]

  if (host !== legacyProductionHost) return

  const url = getRequestURL(event)
  return sendRedirect(event, `${siteUrl}${url.pathname}${url.search}`, 308)
})
