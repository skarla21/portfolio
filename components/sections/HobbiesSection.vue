<script setup lang="ts">
import { desktopMotion, useScrollScene } from "~/composables/useScrollScene";
import { useLocale } from "~/composables/useLocale";
import type { Hobby, HobbyMedia } from "~/content/site";

const chaseQuery =
  "(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)";
/* Scroll Y drift, scaled ~0.7 with the tighter vertical scatter. */
const drift = [6, 3, -4, 4, -3, 4];
const maxSkew = 6;
const skewDecay = 0.82;
const skewGain = 0.18;

const { copy } = useLocale();
const root = ref<HTMLElement | null>(null);
const follow = ref<HTMLElement | null>(null);
const followImg = ref<HTMLImageElement | null>(null);
const followVideo = ref<HTMLVideoElement | null>(null);
const chase = ref(false);
const rolling = new Set<HTMLElement>();

let gsapApi: typeof import("gsap").gsap | null = null;
let hideTimer = 0;
let raf = 0;
let hovering = false;
let playToken = 0;
let videoSrc = "";
let pointerX = 0;
let pointerY = 0;
let pendingX = 0;
let pendingY = 0;
let skewX = 0;
let skewY = 0;
let originX = 0;
let originY = 0;
const lastPick = new Map<string, HobbyMedia>();
const edgePad = 12;
const cursorGap = 30;

function headerBottom() {
  const header = document.querySelector("header");
  return (header?.getBoundingClientRect().bottom ?? 0) + edgePad;
}

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

function hasMedia(hobby: Hobby) {
  return hobby.media.length > 0;
}

let mediaPrefetched = false;

function preloadImages() {
  if (mediaPrefetched) return;
  mediaPrefetched = true;
  const seen = new Set<string>();
  for (const hobby of copy.value.hobbies) {
    const sources = [
      hobby.still,
      ...hobby.media.flatMap((item) =>
        item.type === "image"
          ? [item.src]
          : item.poster
            ? [item.poster]
            : [],
      ),
    ].filter((src): src is string => Boolean(src));
    for (const src of sources) {
      if (seen.has(src)) continue;
      seen.add(src);
      const image = new Image();
      image.src = src;
    }
  }
}

function pick(hobby: Hobby) {
  const list = hobby.media;
  if (!list.length) return null;
  const previous = lastPick.get(hobby.id);
  let index = Math.floor(Math.random() * list.length);
  if (list.length > 1 && list[index] === previous)
    index = (index + 1) % list.length;
  const next = list[index];
  lastPick.set(hobby.id, next);
  return next;
}

function sizeCard(width: number, height: number, mediaScale = 1) {
  const card = follow.value;
  if (!card || width < 1 || height < 1) return;
  const maxW = Math.min(window.innerWidth * 0.5, 32 * 16);
  const maxH = window.innerHeight * 0.72;
  const scale = Math.min(1, maxW / width, maxH / height) * mediaScale;
  card.style.width = `${Math.round(width * scale)}px`;
  card.style.height = `${Math.round(height * scale)}px`;
  paint();
}

function paint() {
  const card = follow.value;
  if (!card) return;
  const width = card.offsetWidth;
  const height = card.offsetHeight;
  const top = headerBottom();
  const right = window.innerWidth - edgePad;
  const bottom = window.innerHeight - edgePad;

  if (width > 1 && height > 1) {
    const fitsRight = pointerX + cursorGap + width <= right;
    const fitsLeft = pointerX - cursorGap - width >= edgePad;
    if (originX === 0 && !fitsRight && fitsLeft) originX = 1;
    else if (originX === 1 && !fitsLeft && fitsRight) originX = 0;

    const fitsBelow = pointerY + cursorGap + height <= bottom;
    const fitsAbove = pointerY - cursorGap - height >= top;
    if (originY === 0 && !fitsBelow && fitsAbove) originY = 1;
    else if (originY === 1 && !fitsAbove && fitsBelow) originY = 0;
  }

  const x = clamp(
    originX ? pointerX - width - cursorGap : pointerX + cursorGap,
    edgePad,
    Math.max(edgePad, right - width),
  );
  const y = clamp(
    originY ? pointerY - height - cursorGap : pointerY + cursorGap,
    top,
    Math.max(top, bottom - height),
  );
  card.style.transformOrigin = `${originX * 100}% ${originY * 100}%`;
  card.style.transform = `translate3d(${x}px, ${y}px, 0) skewX(${skewX}deg) skewY(${skewY}deg)`;
}

function frame() {
  // The cursor's corner leads. The opposite edges lag, so the shear follows the spawn direction.
  const leadX = originY ? 1 : -1;
  const leadY = originX ? 1 : -1;
  skewX = clamp(
    skewX * skewDecay + leadX * pendingX * skewGain,
    -maxSkew,
    maxSkew,
  );
  skewY = clamp(
    skewY * skewDecay + leadY * pendingY * skewGain,
    -maxSkew,
    maxSkew,
  );
  pendingX = 0;
  pendingY = 0;
  if (Math.abs(skewX) < 0.05) skewX = 0;
  if (Math.abs(skewY) < 0.05) skewY = 0;
  paint();
  if (hovering || skewX !== 0 || skewY !== 0)
    raf = requestAnimationFrame(frame);
  else raf = 0;
}

function ensureLoop() {
  if (!raf) raf = requestAnimationFrame(frame);
}

function showPoster(src: string, scale: number | undefined, token: number) {
  const image = followImg.value;
  const video = followVideo.value;
  if (!image || !video) return;
  video.pause();
  video.hidden = true;
  image.hidden = false;
  const ready = () => {
    if (token !== playToken) return;
    sizeCard(image.naturalWidth, image.naturalHeight, scale);
  };
  image.onload = ready;
  if (image.getAttribute("src") !== src) image.src = src;
  if (image.complete && image.naturalWidth) ready();
}

function showMedia(item: HobbyMedia) {
  const image = followImg.value;
  const video = followVideo.value;
  if (!image || !video) return;
  playToken += 1;
  const token = playToken;

  if (item.type === "image") {
    showPoster(item.src, item.scale, token);
    return;
  }

  video.muted = true;
  video.pause();

  if (item.poster) showPoster(item.poster, item.scale, token);
  else {
    image.hidden = true;
    video.hidden = false;
  }

  const start = () => {
    if (token !== playToken) return;
    sizeCard(video.videoWidth, video.videoHeight, item.scale);
    image.hidden = true;
    video.hidden = false;
    const play = () => {
      if (token !== playToken) return;
      void video.play().catch(() => {});
    };
    if (video.currentTime < 0.05) {
      play();
      return;
    }
    video.addEventListener("seeked", play, { once: true });
    video.currentTime = 0;
  };
  if (videoSrc !== item.src) {
    videoSrc = item.src;
    video.src = item.src;
  }
  if (video.readyState >= 2 && video.videoWidth) start();
  else {
    video.addEventListener("loadeddata", start, { once: true });
    video.load();
  }
}

function lineHeight(track: HTMLElement) {
  return track.firstElementChild?.getBoundingClientRect().height ?? 0;
}

function playRoll(track: HTMLElement | null) {
  if (!track || !gsapApi || !chase.value) return;
  const height = lineHeight(track);
  if (!height) return;
  rolling.add(track);
  gsapApi.killTweensOf(track);
  gsapApi.fromTo(
    track,
    { y: 0 },
    {
      y: height,
      duration: 0.42,
      ease: "power4.out",
      onComplete() {
        gsapApi?.set(track, { y: 0 });
        rolling.delete(track);
      },
    },
  );
}

function resetRoll(track: HTMLElement | null) {
  if (!track || !gsapApi || !rolling.has(track)) return;
  gsapApi.killTweensOf(track);
  const y = Number(gsapApi.getProperty(track, "y"));
  if (!Number.isFinite(y) || y <= 1) {
    gsapApi.set(track, { y: 0 });
    rolling.delete(track);
    return;
  }
  gsapApi.to(track, {
    y: 0,
    duration: 0.18,
    ease: "power3.out",
    onComplete() {
      rolling.delete(track);
    },
  });
}

function trackFrom(event: Event) {
  return (
    (event.currentTarget as HTMLElement | null)?.querySelector<HTMLElement>(
      ".hobby-roll",
    ) ?? null
  );
}

function hideNow(immediate = false) {
  window.clearTimeout(hideTimer);
  hovering = false;
  pendingX = 0;
  pendingY = 0;
  follow.value?.classList.remove("is-on");
  followVideo.value?.pause();
  if (!immediate) return;
  skewX = 0;
  skewY = 0;
  cancelAnimationFrame(raf);
  raf = 0;
  originX = 0;
  originY = 0;
  if (follow.value) {
    follow.value.style.transform = "";
    follow.value.style.transformOrigin = "";
    follow.value.style.width = "";
    follow.value.style.height = "";
  }
}

function enter(hobby: Hobby, event: PointerEvent) {
  if (!chase.value || !follow.value || !hasMedia(hobby)) return;
  const item = pick(hobby);
  if (!item) return;
  window.clearTimeout(hideTimer);
  const card = follow.value;
  if (!card.classList.contains("is-on")) {
    skewX = 0;
    skewY = 0;
    originX = 0;
    originY = 0;
  }
  hovering = true;
  pendingX = 0;
  pendingY = 0;
  pointerX = event.clientX;
  pointerY = event.clientY;
  originX = 0;
  originY = 0;
  showMedia(item);
  card.classList.add("is-on");
  paint();
  ensureLoop();
  playRoll(trackFrom(event));
}

function move(event: PointerEvent) {
  if (!hovering) return;
  pendingX += event.clientX - pointerX;
  pendingY += event.clientY - pointerY;
  pointerX = event.clientX;
  pointerY = event.clientY;
  paint();
  ensureLoop();
}

function leave(hobby: Hobby, event: PointerEvent) {
  if (hasMedia(hobby)) resetRoll(trackFrom(event));
  window.clearTimeout(hideTimer);
  hideTimer = window.setTimeout(() => hideNow(), 40);
}

onMounted(async () => {
  if (followVideo.value) followVideo.value.muted = true;

  const media = window.matchMedia(chaseQuery);
  const apply = () => {
    chase.value = media.matches;
    if (!media.matches) {
      hideNow(true);
      root.value
        ?.querySelectorAll<HTMLElement>(".hobby-roll")
        .forEach((track) => {
          gsapApi?.killTweensOf(track);
          gsapApi?.set(track, { y: 0 });
          rolling.delete(track);
        });
    }
  };
  apply();
  media.addEventListener("change", apply);

  let prefetchObserver: IntersectionObserver | null = null;
  if (root.value) {
    prefetchObserver = new IntersectionObserver(
      ([entry]) => {
        if (!entry?.isIntersecting) return;
        preloadImages();
        prefetchObserver?.disconnect();
        prefetchObserver = null;
      },
      { rootMargin: "300px 0px" },
    );
    prefetchObserver.observe(root.value);
  }

  onUnmounted(() => {
    media.removeEventListener("change", apply);
    prefetchObserver?.disconnect();
  });

  const { gsap } = await import("gsap");
  gsapApi = gsap;
});

watch(
  () => copy.value.hobbies,
  () => {
    if (!import.meta.client) return;
    if (mediaPrefetched) {
      mediaPrefetched = false;
      preloadImages();
    }
    hideNow(true);
  },
);

onUnmounted(() => {
  window.clearTimeout(hideTimer);
  cancelAnimationFrame(raf);
  followVideo.value?.pause();
});

useScrollScene(root, ({ gsap, mm }) => {
  mm.add(desktopMotion, () => {
    const words = root.value?.querySelectorAll<HTMLElement>(".js-drift");
    if (!words?.length || !root.value) return;

    words.forEach((word) => {
      const y = Number(word.dataset.drift ?? 0);
      gsap.to(word, {
        y,
        ease: "none",
        scrollTrigger: {
          trigger: root.value,
          start: "top bottom",
          end: "bottom top",
          scrub: true,
        },
      });
    });
  });
});
</script>

<template>
  <section
    id="beyond"
    ref="root"
    class="bg-paper px-6 py-24 md:px-10 md:py-32 lg:px-16"
  >
    <p class="text-xs uppercase tracking-[0.22em]">05</p>
    <h2
      class="mt-3 max-w-4xl font-serif text-[clamp(3rem,6vw,5.5rem)] leading-[0.95] tracking-tight"
    >
      {{ copy.beyondTitle }}
    </h2>

    <div class="hobby-field mt-10 md:mt-14">
      <div
        v-for="(hobby, index) in copy.hobbies"
        :key="hobby.id"
        class="hobby js-drift"
        :class="`hobby-${index}`"
        :data-drift="drift[index]"
      >
        <span
          class="hobby-label"
          :class="{ 'has-media': hasMedia(hobby) }"
          @pointerenter="enter(hobby, $event)"
          @pointermove="move"
          @pointerleave="leave(hobby, $event)"
        >
          <span class="hobby-mask">
            <span class="hobby-roll">
              <span class="hobby-line" aria-hidden="true">{{
                hobby.label
              }}</span>
              <span class="hobby-line">{{ hobby.label }}</span>
            </span>
          </span>
        </span>
        <img
          v-if="!chase && hobby.still"
          class="hobby-still"
          :src="hobby.still"
          alt=""
        />
      </div>
    </div>

    <div v-show="chase" ref="follow" class="hobby-follow" aria-hidden="true">
      <img ref="followImg" alt="" hidden />
      <video ref="followVideo" muted playsinline loop preload="none" hidden />
    </div>
  </section>
</template>

<style scoped>
.hobby-field {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.hobby {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem 1rem;
  width: max-content;
  max-width: 100%;
  pointer-events: none;
  font-family: "Source Serif 4", Georgia, serif;
  line-height: 0.9;
  letter-spacing: -0.03em;
}

.hobby-label {
  position: relative;
  pointer-events: auto;
  cursor: default;
  line-height: 1.35;
}

.hobby-label.has-media {
  cursor: pointer;
}

.hobby-mask {
  display: inline-block;
  overflow: hidden;
  height: 1lh;
  line-height: 1.35;
  padding-inline: 0.12em;
  margin-inline: -0.12em;
  vertical-align: top;
}

.hobby-roll {
  display: flex;
  flex-direction: column;
  margin-top: -1lh;
}

.hobby-line {
  display: block;
  height: 1lh;
  line-height: 1.35;
  white-space: nowrap;
}

.hobby-still {
  width: 8.5rem;
  height: 6rem;
  object-fit: cover;
  pointer-events: none;
}

.hobby-follow {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 40;
  width: 0;
  height: 0;
  overflow: hidden;
  opacity: 0;
  pointer-events: none;
  transform-origin: 0 0;
  transition: opacity 120ms cubic-bezier(0.23, 1, 0.32, 1);
}

.hobby-follow.is-on {
  opacity: 1;
  transition-duration: 160ms;
  will-change: transform;
}

.hobby-follow img,
.hobby-follow video {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: fill;
}

.hobby-follow [hidden] {
  display: none;
}

.hobby-0 {
  font-size: clamp(1.85rem, 7.2vw, 2.25rem);
}
.hobby-1 {
  font-size: clamp(1.4rem, 5.4vw, 1.7rem);
  font-style: italic;
}
.hobby-2 {
  font-size: clamp(1.55rem, 6vw, 1.9rem);
  font-style: italic;
}
.hobby-3 {
  font-size: clamp(1.75rem, 6.6vw, 2.1rem);
}
.hobby-4 {
  font-size: clamp(1.65rem, 6.2vw, 2rem);
}
.hobby-5 {
  font-size: clamp(1.45rem, 5.6vw, 1.75rem);
  font-style: italic;
}

@media (min-width: 768px) {
  .hobby-field {
    position: relative;
    width: min(78%, 58rem);
    min-height: 28rem;
    margin-inline: auto;
  }

  .hobby {
    position: absolute;
  }

  /* Scatter: same constellation, X ×1.25 / Y ×0.7 around the cloud center. */
  .hobby-0 {
    left: 19%;
    top: 18%;
    font-size: clamp(2.15rem, 3vw, 2.75rem);
  }
  .hobby-1 {
    left: 64%;
    top: 23%;
    font-size: clamp(1.55rem, 2vw, 1.9rem);
  }
  .hobby-2 {
    left: 6%;
    top: 37%;
    font-size: clamp(1.75rem, 2.35vw, 2.15rem);
  }
  .hobby-3 {
    left: 61%;
    top: 44%;
    font-size: clamp(2rem, 2.7vw, 2.5rem);
  }
  .hobby-4 {
    left: 60%;
    top: 49%;
    font-size: clamp(1.9rem, 2.5vw, 2.35rem);
  }
  .hobby-5 {
    left: 14%;
    top: 58%;
    font-size: clamp(1.6rem, 2.1vw, 2rem);
  }
}

@media (min-width: 1200px) {
  section {
    display: flex;
    flex-direction: column;
    min-height: 100dvh;
    padding-top: 4.5rem;
    padding-bottom: 3.25rem;
  }

  .hobby-field {
    flex: 1;
    width: min(70%, 56rem);
    min-height: 0;
    margin-top: 0.25rem;
  }

  .hobby-0 {
    left: 18%;
    top: 25%;
  }
  .hobby-1 {
    left: 61%;
    top: 23%;
  }
  .hobby-2 {
    left: 26%;
    top: 41%;
  }
  .hobby-3 {
    left: 68%;
    top: 36%;
  }
  .hobby-4 {
    left: 8%;
    top: 54%;
  }
  .hobby-5 {
    left: 53%;
    top: 57%;
  }
}
</style>
