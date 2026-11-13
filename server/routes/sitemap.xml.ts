import { siteUrl } from '../../content/site'
import { sitePaths, withLocale } from '../../utils/localePath'

function escapeXml(value: string) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;')
}

function absolute(path: string) {
  return `${siteUrl}${path}`
}

export default defineEventHandler((event) => {
  setHeader(event, 'content-type', 'application/xml; charset=utf-8')

  const urls = sitePaths.flatMap((path) => {
    const el = withLocale(path, 'el')
    const en = withLocale(path, 'en')
    return [
      { loc: el, el, en },
      { loc: en, el, en },
    ]
  })

  const body = urls
    .map(({ loc, el, en }) => {
      const locAbs = escapeXml(absolute(loc))
      const elAbs = escapeXml(absolute(el))
      const enAbs = escapeXml(absolute(en))
      return `  <url>
    <loc>${locAbs}</loc>
    <xhtml:link rel="alternate" hreflang="el" href="${elAbs}" />
    <xhtml:link rel="alternate" hreflang="en" href="${enAbs}" />
    <xhtml:link rel="alternate" hreflang="x-default" href="${elAbs}" />
  </url>`
    })
    .join('\n')

  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
${body}
</urlset>
`
})
