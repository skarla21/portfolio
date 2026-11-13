# Scroll page

The portfolio home is one vertical page per language. Greek is the default at `/`; English is `/en`. `content/site.ts` holds shared copy; `content/offerings.ts` holds services and FAQ. Do not add a project screenshot, the accountant's name, or the bank name. Antonis's only portrait is the introduction circle from `public/imgs/pfp.jpg`. Named recommenders and their portraits are allowed.

## Locales

- `/`, `/services`, `/faq` — Greek
- `/en`, `/en/services`, `/en/faq` — English
- Language toggle navigates to the paired path. Cookie mirrors preference; URL wins.
- Every page sets reciprocal `hreflang` (`el`, `en`, `x-default` → Greek URL).

## Home sections

1. Introduction. Name, lede, disciplines, then profile with portrait. Paper. Marker `01`.
2. Journey. One line and alternating milestones. Mist. Marker `02`.
3. Skills. One icon marquee. Mist. Not its own chapter in the nav.
4. Services teaser. Five offerings from the business card + CTA to `/services`. Paper. Kicker `03`.
5. Selected work. Freelance intro, then Mathe, Figata, accountant site, Orderoo. Night. The only pinned section. Kicker `04`.
6. Recommendations. Kicker `05`. Three short quotes with circular portraits. Mist.
7. Beyond the screen. Music, cinema, football, travelling, chess, climbing. Paper. Kicker `06`.
8. Contact. Email, phone, LinkedIn, GitHub, CV, link to FAQ. Ink. Kicker `07`.

## Inner pages

- Services: long-form articles for each offering, proof link to `#work`, contact CTA.
- FAQ: visible question then answer (no FAQ rich-result schema). Contact CTA.

## Nav

Locale home name link, section anchors (intro, journey, work, recommendations, beyond, contact), route links for Services and FAQ, language toggle, CV. Desktop nav may scroll horizontally on mid-width screens. Mobile uses the hamburger menu. A one-time “Continue in English?” hint appears on Greek URLs when `localePrefer` is `en` (from the language toggle or a migrated old `locale=en` cookie).

## Motion

GSAP ScrollTrigger, registered after mount. `gsap.matchMedia()` is the only context. The desktop query is `(min-width: 768px) and (prefers-reduced-motion: no-preference)`.

- Introduction, journey, services teaser, recommendations: a short rise as they enter, once.
- Journey line: `scaleY` scrubbed from the top. Without that query the line is already full height.
- Projects: the section pins, the inner track moves on `x` with `ease: "none"`.
- Hobbies: slight scrubbed drift and cursor media on fine pointers.
- Skills marquee: CSS transform, desktop motion only.

After fonts load, `ScrollTrigger.refresh()`. Revert the matchMedia on unmount. Do not add Lenis, and do not pin any other section.

## Type and colour

Source Serif 4 and Source Sans 3, from `@fontsource`, including the Greek subsets. Tokens live in `tailwind.config.ts`: paper `#f3efe4`, mist `#e3ebe7`, ink `#14120e`, night `#10131c`, lime `#d6f26a`, iris `#c4b5fd`, clay `#ffb088`. Orderoo's field is `#9fd0c8`.
