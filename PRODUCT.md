# Product

## Platform

web

## Stack

Nuxt 3, Vue 3, Tailwind, GSAP, Vercel. Server-rendered pages, hydrated on the client for scroll motion. No Auth.js, Stripe, Supabase, or shadcn-vue. Contact is a mailto and a tel link, so Resend is not part of this surface.

## Users

Someone deciding whether to talk to Antonis Skarlatos about IT or web development work: a hiring manager, a collaborator, or a client. They arrive with little context and need his background, the services he offers, his freelance work, and a way to reach him.

## Product Purpose

A personal introduction plus crawlable service pages. The home page shows who he is, what he studied, where he has worked, a short services teaser, the freelance projects he can talk about, short quotes from three colleagues, and how to contact him or open his CV. Dedicated Services and FAQ pages support Greek and English commercial search. Success is that a visitor can do those things by scrolling or navigating, and that nothing on the site claims work the CV does not list.

## Positioning

Greek home at `/`; English under `/en`. Studies and jobs share one timeline on the home page. A Services teaser sits after Skills and before the pinned project gallery. Full service copy lives on `/services` (and `/en/services`). Common questions live on `/faq` (and `/en/faq`). Contact and the CV file close the home page.

## Operating Context

URL is the locale source of truth (`/` = Greek, `/en…` = English). A `locale` cookie mirrors preference after navigation; it must not change the language served at `/`. Vertical scroll on home, with a single pinned stretch for the projects on a wide screen that accepts motion. Both languages open the same English CV. Thesis titles stay on the timeline; the thesis paragraphs stay in the file. The master's thesis title links to Pergamos.

## Capabilities and Constraints

- Readable at rest: Αντώνης Σκαρλάτος, IT & software services, Athens. English keeps Antonis Skarlatos.
- Introduction: the CV profile for the current language, with `public/imgs/pfp.jpg` in a circle beside the sentences.
- Timeline: Physics BSc (2015–2020, NKUA) and Control and Computing MSc (2020–2022, NKUA), both thesis titles, FactSet, Performance Technologies, both IASA roles, languages, and four certificates. The MSc thesis and the certificates that have a URL are links. Advanced SQL stays text.
- Skills: one icon carousel of the kept technologies.
- Services teaser + `/services`: websites & e-shops, custom apps, systems & software consulting, smart QR & NFC cards, SEO & AEO — aligned with the business card.
- FAQ page: visible Q&A for process, timeline, stack, remote work, and SEO; no FAQ rich-result schema targeting.
- Projects, in order: Μάθε Παιδί μου Αρχαία, Figata Café, the accountant site, Orderoo. Mathe, Figata, and the accountant site link out. Orderoo does not.
- Recommendations: three short quotes from Nikos Dimitrakopoulos, Thodoris Delbederis, and Vasileios Varveroglou.
- Beyond the screen: music, cinema, football, travelling, chess, climbing.
- Contact: email, phone, LinkedIn, GitHub, CV, plus a link to FAQ.
- Driving licences stay in the PDF only. The German bank and the accountant stay unnamed.
- Skip link, fixed nav (home section anchors including Beyond, plus Services and FAQ), language toggle that changes the path, reduced-motion path. Cookie `locale` mirrors the URL; `localePrefer` remembers the last toggle so a Greek URL can offer a one-time English hint without changing what `/` serves. Reduced motion, and any viewport under 768px, drops the pin, the marquee, the drawing line, and the word movement.

## Brand

Paper, mist, night, and ink, in that rhythm. Source Serif 4 for the large lines, Source Sans 3 for the rest, both with Greek. Lime, iris, clay, and a fourth field colour mark the four project panels.

## Evidence on Hand

- CV file: `public/cv/Skarlatos_CV.pdf`.
- Business card services: `print/business-card/front.png`.
- Identity: Antonis Skarlatos, developer, data analyst, and physicist, Athens 16232.
- Email antwnis_skarlatos@yahoo.com, phone +30 6983696885, LinkedIn antonis-skarlatos-a41781212, GitHub skarla21.
- Portrait: `public/imgs/pfp.jpg`.
- Absent, and not to be invented: project screenshots, a named accounting client, and the name of the German bank.

## Product Principles

- The CV is the only source of Antonis's own claims; the recommendations are colleagues speaking; services match the business card.
- Home is one scroll. Only the project gallery pins, and only when there is width and no reduced-motion preference.
- Text that must stay accurate is HTML.
- A visitor who does not scroll through every animation, or who prefers less motion, still reaches every section from the nav.

## Accessibility & Inclusion

Skip link. Visible focus. Locale-aware nav links. `prefers-reduced-motion` removes pinning and scroll-scrubbed movement. The CV text is real text, not an image of text.

## SEO ops

See [docs/seo-gsc.md](docs/seo-gsc.md) for Search Console and indexing steps after deploy.
