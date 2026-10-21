# Product

## Platform

web

## Stack

Nuxt 3, Vue 3, Tailwind, GSAP, Vercel. One server-rendered page, hydrated on the client for scroll motion. No Auth.js, Stripe, Supabase, or shadcn-vue. Contact is a mailto and a tel link, so Resend is not part of this surface.

## Users

Someone deciding whether to talk to Antonis Skarlatos about web development work: a hiring manager, a collaborator, or a client. They arrive with little context and need his background, his freelance work, and a way to reach him.

## Product Purpose

A personal introduction. The page shows who he is, what he studied, where he has worked, the freelance projects he can talk about, and how to contact him or open his CV. Success is that a visitor can do those things by scrolling, or by using the nav, and that nothing on the page claims work the CV does not list.

## Positioning

One continuous page. The name is the opening. Studies and jobs share one timeline. Freelance projects are a pinned horizontal gallery. Contact and the CV file close the page.

## Operating Context

One page. Greek is the default; English is a nav switch, stored in a `locale` cookie. Vertical scroll, with a single pinned stretch for the projects on a wide screen that accepts motion. Each language has its own CV PDF. Thesis titles stay on the timeline; the thesis paragraphs stay in the file. The master's thesis title links to Pergamos.

## Capabilities and Constraints

- Readable at rest: Αντώνης Σκαρλάτος, web developer, Athens. English keeps Antonis Skarlatos.
- Introduction: the CV profile for the current language.
- Timeline: Physics BSc (2015–2020, NKUA) and Control and Computing MSc (2020–2022, NKUA), both thesis titles, FactSet, Performance Technologies, both IASA roles, languages, and four certificates. The MSc thesis and the certificates that have a URL are links. Advanced SQL stays text.
- Skills: one icon carousel of the kept technologies. Low-importance tools and the abstract skill phrases are not on the page.
- Projects, in order: Μάθε Παιδί μου Αρχαία, Figata Café, the accountant site, Orderoo. Mathe, Figata, and the accountant site link out. Orderoo does not. No project screenshots yet, so each panel keeps a flat colour field.
- Beyond the screen: music, cinema, football, travelling, chess, bouldering. A placeholder image follows a fine pointer; on a coarse pointer or reduced motion it sits with the word.
- Contact: email, phone, LinkedIn, GitHub, and the CV file.
- Driving licences stay in the PDF only. The German bank and the accountant stay unnamed.
- A skip link, a fixed nav, and a reduced-motion path are required. Reduced motion, and any viewport under 768px, drops the pin, the marquee, the drawing line, and the word movement. The projects stack vertically. The line is already drawn.

## Brand

Paper, mist, night, and ink, in that rhythm. Source Serif 4 for the large lines, Source Sans 3 for the rest, both with Greek. Lime, iris, clay, and a fourth field colour mark the four project panels. The page is type, those fields, and the skill marks. It is not a room, a pixel scene, or a frame sequence.

## Evidence on Hand

- CV files: `public/cv/antonis-skarlatos-el.pdf` and `public/cv/antonis-skarlatos-en.pdf`. The nav and the contact link open the file for the current language.
- Identity on the CV: Αντώνης Σκαρλάτος / Antonis Skarlatos, programmer, data analyst, and physicist, Athens 16232.
- Email antwnis_skarlatos@yahoo.com, phone +30 6983696885, LinkedIn antonis-skarlatos-a41781212, GitHub skarla21.
- Absent, and not to be invented: project screenshots, a named accounting client, the name of the German bank, and a portrait of Antonis. Orderoo has no public URL.

## Product Principles

- The CV is the only source of personal claims.
- The page is one scroll. Only the project gallery pins, and only when there is width and no reduced-motion preference.
- Text that must stay accurate is HTML.
- A visitor who does not scroll through every animation, or who prefers less motion, still reaches every section from the nav.

## Accessibility & Inclusion

Skip link. Visible focus. Anchor links to each chapter. `prefers-reduced-motion` removes pinning and scroll-scrubbed movement. The CV text is real text, not an image of text.
