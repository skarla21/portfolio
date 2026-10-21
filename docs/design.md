# Scroll page

The portfolio is one vertical page. Greek is the default. `content/site.ts` holds the same copy shape for `el` and `en`. Do not add a screenshot, a client name, a bank name, or a portrait.

## Sections

1. Hero. Name, Athens, the disciplines line, Physics · Data · Web. Paper.
2. Introduction. The profile, sentence by sentence. Paper.
3. Journey. One line and alternating milestones: Physics BSc, IASA research associate, Control and Computing MSc, IASA data research, Performance Technologies, FactSet. Languages and certificates after the line. Mist.
4. Skills. One icon marquee. Mist. Not its own chapter in the nav. Narrow screens and reduced motion wrap the icons and do not loop.
5. Selected work. A short freelance intro, then Mathe Paidi Mou Archaia, Figata Café, the accountant site, and Orderoo. Night. The only pinned section.
6. Beyond the screen. Music, cinema, football, travelling, chess, bouldering. Paper. A placeholder follows the cursor on a fine pointer.
7. Contact. Email, phone, LinkedIn, GitHub, CV. Ink.

Nav: the section links, an EL/EN switch, and CV. Changing language sets `<html lang>` and refreshes ScrollTrigger.

## Motion

GSAP ScrollTrigger, registered after mount. `gsap.matchMedia()` is the only context. The desktop query is `(min-width: 768px) and (prefers-reduced-motion: no-preference)`.

- Hero: the two name lines rise on load. The headline drifts a short distance with scroll.
- Introduction and journey cards: a short rise as they enter, once.
- Journey line: `scaleY` scrubbed from the top. Without that query the line is already full height.
- Projects: the section pins, the inner track moves on `x` with `ease: "none"`, and the distance is the measured overflow. Titles rise with `containerAnimation`. Opacity stays at 1.
- Hobbies: a slight scrubbed drift. The cursor image uses `translate3d` and does not run for a coarse pointer or reduced motion.
- Skills marquee: CSS transform, desktop motion only. It pauses while an icon is hovered or focused.

After fonts load, `ScrollTrigger.refresh()`. Revert the matchMedia on unmount. Do not add Lenis, and do not pin any other section.

## Type and colour

Source Serif 4 and Source Sans 3, from `@fontsource`, including the Greek subsets. Tokens live in `tailwind.config.ts`: paper `#f3efe4`, mist `#e3ebe7`, ink `#14120e`, night `#10131c`, lime `#d6f26a`, iris `#c4b5fd`, clay `#ffb088`. Orderoo's field is `#9fd0c8`.
