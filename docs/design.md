# Scroll page

The portfolio is one vertical page. Greek is the default. `content/site.ts` holds the same copy shape for `el` and `en`. Do not add a project screenshot, the accountant's name, or the bank name. Antonis's only portrait is the introduction circle from `public/imgs/pfp.jpg`. Named recommenders and their portraits are allowed.

## Sections

1. Hero. Name, Athens, the disciplines line, Physics · Data · Web. Paper.
2. Introduction. A small circular portrait on the left of the profile, sentence by sentence. Paper.
3. Journey. One line and alternating milestones: Physics BSc, IASA research associate, Control and Computing MSc, IASA data research, Performance Technologies, FactSet. Languages and certificates after the line. Mist.
4. Skills. One icon marquee. Mist. Not its own chapter in the nav. Narrow screens and reduced motion wrap the icons and do not loop.
5. Selected work. A short freelance intro, then Mathe Paidi Mou Archaia, Figata Café, the accountant site, and Orderoo. Night. The only pinned section.
6. Recommendations. Kicker `04`. Greek: «Τι είπαν αυτοί που συνεργαστήκαμε». English: «From people I've worked with». Three short quotes: Nikos Dimitrakopoulos (Full Stack Developer, Orderoo), Thodoris Delbederis (Figata Cafe), Vasileios Varveroglou (Full Stack Developer, FactSet). Circular portraits and LinkedIn links. Mist.
7. Beyond the screen. Music, cinema, football, travelling, chess, climbing. Paper. Kicker `05`. A placeholder follows the cursor on a fine pointer.
8. Contact. Email, phone, LinkedIn, GitHub, CV. Ink. Kicker `06`.

Nav: the section links—including «Συστάσεις» / «Recommendations» between Work and Beyond, href `#recommendations`—the current language (one label, click switches), and CV. Changing language sets `<html lang>` and refreshes ScrollTrigger. The CV link always opens the English file.

## Motion

GSAP ScrollTrigger, registered after mount. `gsap.matchMedia()` is the only context. The desktop query is `(min-width: 768px) and (prefers-reduced-motion: no-preference)`.

- Hero: the two name lines rise on load. The headline drifts a short distance with scroll.
- Introduction and journey cards: a short rise as they enter, once.
- Recommendations quotes: the same rise as they enter, once. Desktop query only.
- Journey line: `scaleY` scrubbed from the top. Without that query the line is already full height.
- Projects: the section pins, the inner track moves on `x` with `ease: "none"`, and the distance is the measured overflow. Titles rise with `containerAnimation`. Opacity stays at 1.
- Hobbies: a slight scrubbed drift. On a fine pointer, a hobby with media rolls the word and shows a borderless image or video whose box matches the media's aspect ratio, top-left on the cursor. Empty hobbies (music, cinema) do not open a card. The card's far edges lag with skew, then it squares up. It does not run for a coarse pointer or reduced motion; those show a still beside the word when one exists.
- Skills marquee: CSS transform, desktop motion only. It pauses while an icon is hovered or focused.

After fonts load, `ScrollTrigger.refresh()`. Revert the matchMedia on unmount. Do not add Lenis, and do not pin any other section.

## Type and colour

Source Serif 4 and Source Sans 3, from `@fontsource`, including the Greek subsets. Tokens live in `tailwind.config.ts`: paper `#f3efe4`, mist `#e3ebe7`, ink `#14120e`, night `#10131c`, lime `#d6f26a`, iris `#c4b5fd`, clay `#ffb088`. Orderoo's field is `#9fd0c8`.
