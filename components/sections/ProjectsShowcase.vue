<script setup lang="ts">
import { desktopMotion, useScrollScene } from "~/composables/useScrollScene";
import { useLocale } from "~/composables/useLocale";
import {
  ACTIVE_RATIO,
  selectActiveProjectId,
} from "~/utils/selectActiveProject";

const { copy } = useLocale();
const root = ref<HTMLElement | null>(null);
const track = ref<HTMLElement | null>(null);
const activeId = ref<string | null>(null);
const frameShown = ref(false);
const failed = ref<Record<string, boolean>>({});
const activeVideo = ref<HTMLVideoElement | null>(null);

const stages = new Map<string, HTMLElement>();
const stageRefs = new Map<string, (el: unknown) => void>();
const ratios = new Map<string, number>();

let stageObserver: IntersectionObserver | undefined;
let reduceMotion = false;

function stageRef(id: string) {
  const existing = stageRefs.get(id);
  if (existing) return existing;
  const register = (el: unknown) => {
    const node = el instanceof HTMLElement ? el : null;
    const current = stages.get(id) ?? null;
    if (current === node) return;
    if (current) stageObserver?.unobserve(current);
    if (node) {
      stages.set(id, node);
      stageObserver?.observe(node);
    } else {
      stages.delete(id);
      ratios.delete(id);
      pickActive();
    }
  };
  stageRefs.set(id, register);
  return register;
}

// GSAP moves stages via parent transform; IO ratios go stale on reverse scroll.
function measureRatios() {
  const viewW = window.innerWidth;
  const viewH = window.innerHeight;

  stages.forEach((el, id) => {
    const rect = el.getBoundingClientRect();
    const area = rect.width * rect.height;
    if (area <= 0) {
      ratios.set(id, 0);
      return;
    }
    const visibleW = Math.max(
      0,
      Math.min(rect.right, viewW) - Math.max(rect.left, 0),
    );
    const visibleH = Math.max(
      0,
      Math.min(rect.bottom, viewH) - Math.max(rect.top, 0),
    );
    ratios.set(id, (visibleW * visibleH) / area);
  });
}

function ensurePlaying() {
  const video = activeVideo.value;
  if (!video || reduceMotion) return;
  video.muted = true;
  video.defaultMuted = true;
  video.playsInline = true;
  if (video.readyState >= 2) frameShown.value = true;
  if (video.paused) void video.play().catch(() => {});
}

function pickActive() {
  measureRatios();
  const next = reduceMotion
    ? null
    : selectActiveProjectId(ratios, failed.value, activeId.value);

  if (next === activeId.value) {
    ensurePlaying();
    return;
  }
  frameShown.value = false;
  activeId.value = next;
}

function bindStages() {
  if (stageObserver) return;
  stageObserver = new IntersectionObserver(
    () => {
      pickActive();
    },
    { threshold: [0, 0.05, 0.15, ACTIVE_RATIO, 0.6, 0.75, 1] },
  );
  stages.forEach((stage) => stageObserver?.observe(stage));
}

// Ref callback only tracks the element. Do not pause/clear src on null —
// Vue can fire unmount null after the replacement mount, which froze playback.
function setActiveVideo(el: unknown) {
  activeVideo.value = el instanceof HTMLVideoElement ? el : null;
}

async function startActiveVideo() {
  await nextTick();
  const video = activeVideo.value;
  if (!video || !activeId.value || reduceMotion) return;
  video.muted = true;
  video.defaultMuted = true;
  video.playsInline = true;
  try {
    video.currentTime = 0;
  } catch {
    /* ignore seek before metadata */
  }
  if (video.readyState >= 2) frameShown.value = true;
  void video.play().catch(() => {});
}

watch(activeId, () => {
  void startActiveVideo();
});

function onFrameReady() {
  frameShown.value = true;
  ensurePlaying();
}

function onFrameError(id: string) {
  failed.value = { ...failed.value, [id]: true };
  pickActive();
}

onMounted(() => {
  reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  bindStages();
  pickActive();
});

onUnmounted(() => {
  stageObserver?.disconnect();
  activeVideo.value?.pause();
  activeVideo.value = null;
});

useScrollScene(root, ({ gsap, mm }) => {
  mm.add(desktopMotion, () => {
    const section = root.value;
    const row = track.value;
    if (!section || !row) return;

    const distance = () => Math.max(0, row.scrollWidth - section.offsetWidth);

    gsap.to(row, {
      x: () => -distance(),
      ease: "none",
      scrollTrigger: {
        trigger: section,
        start: "top top",
        end: () => `+=${distance()}`,
        pin: true,
        scrub: 1,
        invalidateOnRefresh: true,
        anticipatePin: 1,
        onUpdate: () => {
          pickActive();
        },
      },
    });
  });
});
</script>

<template>
  <!-- Hash target must sit outside the pinned section or in-page nav lands at the pin end. -->
  <div id="work" class="h-0 w-full" aria-hidden="true" />
  <section
    ref="root"
    class="bg-night text-paper md:motion-safe:h-dvh md:motion-safe:overflow-hidden"
  >
    <div
      ref="track"
      class="project-track flex flex-col md:motion-safe:h-dvh md:motion-safe:w-max md:motion-safe:flex-row"
    >
      <article
        class="project-panel flex min-h-dvh flex-col items-center justify-center px-6 py-28 text-center md:px-10 lg:px-16"
      >
        <p class="text-xs uppercase tracking-[0.22em] text-night-soft">
          {{ copy.workKicker }}
        </p>
        <h2
          class="project-title mt-10 max-w-4xl font-serif leading-[0.92] tracking-tight"
        >
          {{ copy.workTitle }}
        </h2>
        <p class="project-body mt-8 max-w-md text-lg leading-relaxed">
          {{ copy.workIntro }}
        </p>
      </article>

      <article
        v-for="project in copy.projects"
        :key="project.id"
        class="project-panel grid gap-8 px-6 py-16 md:px-10 lg:px-16"
      >
        <div class="flex flex-col justify-center">
          <p class="text-sm uppercase tracking-[0.16em] text-night-soft">
            {{ project.stack
            }}<span v-if="project.dates"> / {{ project.dates }}</span>
          </p>
          <h3
            class="project-name mt-6 font-serif leading-[0.92] tracking-tight"
          >
            <a
              v-if="project.href"
              :href="project.href"
              class="underline decoration-1 underline-offset-[8px]"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ project.name }}
            </a>
            <template v-else>{{ project.name }}</template>
          </h3>
          <p class="project-body mt-6 max-w-md text-lg leading-relaxed">
            {{ project.summary }}
          </p>
        </div>
        <div
          :ref="stageRef(project.id)"
          class="project-stage"
          :data-project-id="project.id"
          :style="{ backgroundColor: project.accent }"
        >
          <img
            v-if="project.poster"
            class="project-frame"
            :src="project.poster"
            :alt="`${project.name} preview`"
            loading="lazy"
            decoding="async"
            draggable="false"
          />
          <video
            v-if="
              project.video && activeId === project.id && !failed[project.id]
            "
            :ref="setActiveVideo"
            class="project-frame project-video"
            :class="{ 'is-pending': !frameShown }"
            :src="project.video"
            muted
            loop
            playsinline
            preload="auto"
            tabindex="-1"
            aria-hidden="true"
            @loadeddata="onFrameReady"
            @error="onFrameError(project.id)"
          />
        </div>
      </article>
      <div class="project-trail" aria-hidden="true" />
    </div>
  </section>
</template>

<style scoped>
.project-title {
  font-size: clamp(3rem, 6.5vw, 6.25rem);
}

.project-name {
  font-size: clamp(2.5rem, 4.6vw, 4.6rem);
}

.project-stage {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: calc(22rem * 1.33);
  min-width: 0;
  aspect-ratio: 4 / 5;
  padding: 1.25rem;
  overflow: hidden;
}

.project-frame {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  pointer-events: none;
  background: transparent;
}

.project-video {
  position: absolute;
  inset: 1.25rem;
  width: calc(100% - 2.5rem);
  height: calc(100% - 2.5rem);
}

.project-video.is-pending {
  opacity: 0;
}

@media (min-width: 768px) and (prefers-reduced-motion: no-preference) {
  .project-track {
    --project-trail: min(30vw, 18rem);
  }

  .project-trail {
    flex: 0 0 var(--project-trail);
    width: var(--project-trail);
    align-self: stretch;
  }

  .project-stage {
    flex: 0 0 auto;
    /* Width must stay height×(4/5). The old `* 1.33` made the box too wide once
       max-height clamped, so object-fit cropped the 720×900 recordings. */
    width: min(
      calc(26rem * 1.33),
      calc((100dvh - var(--nav-h) - 5rem) * 4 / 5)
    );
    max-width: calc(26rem * 1.33);
    max-height: calc(100dvh - var(--nav-h) - 5rem);
  }

  .project-panel {
    --project-copy: 22rem;
    --project-media: min(
      calc(26rem * 1.33),
      calc((100dvh - var(--nav-h) - 5rem) * 4 / 5)
    );
    --project-pair-gap: 3rem;
    --project-span: calc(
      var(--project-copy) + var(--project-pair-gap) + var(--project-media)
    );
    display: flex;
    width: max-content;
    max-width: 100vw;
    height: 100dvh;
    flex-shrink: 0;
    align-items: center;
    justify-content: center;
    gap: var(--project-pair-gap);
    padding: calc(var(--nav-h) + 1.5rem) 2.5rem 2.5rem;
  }

  .project-panel > :first-child {
    flex: 0 0 var(--project-copy);
    min-width: 0;
  }

  .project-panel:first-child {
    width: 100vw;
    max-width: none;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding-right: 4rem;
    padding-left: 4rem;
  }

  .project-panel:first-child > :first-child {
    flex: none;
  }

  .project-panel:nth-child(n + 3) {
    margin-left: var(--project-span);
  }
}

/* ~20% larger type + recording frame on very large displays */
@media (min-width: 85.625rem) {
  .project-title {
    font-size: calc(6.25rem * 1.2);
  }

  .project-name {
    font-size: calc(4.6rem * 1.2);
  }

  .project-body {
    font-size: calc(1.125rem * 1.2);
  }

  .project-stage {
    max-width: calc(22rem * 1.33 * 1.2);
  }
}

@media (min-width: 85.625rem) and (prefers-reduced-motion: no-preference) {
  .project-stage {
    width: min(
      calc(26rem * 1.33 * 1.2),
      calc((100dvh - var(--nav-h) - 5rem) * 4 / 5)
    );
    max-width: calc(26rem * 1.33 * 1.2);
  }

  .project-panel {
    --project-copy: calc(22rem * 1.2);
    --project-media: min(
      calc(26rem * 1.33 * 1.2),
      calc((100dvh - var(--nav-h) - 5rem) * 4 / 5)
    );
  }
}
</style>
