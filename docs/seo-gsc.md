# Search Console & indexing checklist

Domain: `https://antonis-skarlatos.vercel.app` (Greek at `/`).

## After deploy

1. Confirm the Search Console property for this host (site verification meta is in `nuxt.config.ts`).
2. Submit `https://antonis-skarlatos.vercel.app/sitemap.xml`.
3. Request indexing for:
   - `/`
   - `/services`
   - `/faq`
   - `/en`
   - `/en/services`
   - `/en/faq`
4. Check **Enhancements** / structured data for `ProfessionalService` / `Person` where reported.
5. Open the **Generative AI performance** report when available and watch impressions for AI Overviews / AI Mode.
6. Spot-check view-source on `/` and `/en`: `hreflang`, canonical, `html lang`, and JSON-LD match the URL language.

## Optional (off-site)

- Google Business Profile with the same name, Athens locality, phone, and site URL.
- Consistent NAP on LinkedIn and other profiles.
- A custom `.gr` domain later would strengthen local trust; not required for this release.

## Contact in llms.txt

Email and phone stay in `/llms.txt` (and JSON-LD). They are already on the contact section; listing them helps assistants answer how to reach Antonis without inventing channels.
