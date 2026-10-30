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

function pickActive() {
  const next = reduceMotion
    ? null
    : selectActiveProjectId(ratios, failed.value);

  if (next === activeId.value) return;
  frameShown.value = false;
  activeId.value = next;
}

function bindStages() {
  if (stageObserver) return;
  stageObserver = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        const el = entry.target;
        if (!(el instanceof HTMLElement)) continue;
        const id = el.dataset.projectId;
        if (!id) continue;
        ratios.set(id, entry.intersectionRatio);
      }
      pickActive();
    },
    { threshold: [0, 0.25, ACTIVE_RATIO, 0.6, 0.75, 1] },
  );
  stages.forEach((stage) => stageObserver?.observe(stage));
}

function unloadVideo(video: HTMLVideoElement | null) {
  if (!video) return;
  video.pause();
  video.removeAttribute("src");
  video.load();
}

function setActiveVideo(el: unknown) {
  const node = el instanceof HTMLVideoElement ? el : null;
  const prev = activeVideo.value;
  if (prev === node) return;
  unloadVideo(prev);
  activeVideo.value = node;
  if (!node || reduceMotion) return;
  node.muted = true;
  node.defaultMuted = true;
  node.playsInline = true;
  // preload="none" never fetches until play/load — kick off playback here
  // so loadeddata can fire and reveal the frame over the poster.
  void node.play().catch(() => {});
}

function onFrameReady() {
  frameShown.value = true;
  const video = activeVideo.value;
  if (!video || reduceMotion) return;
  video.muted = true;
  video.defaultMuted = true;
  void video.play().catch(() => {});
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
  unloadVideo(activeVideo.value);
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
        class="project-panel flex flex-col items-center justify-center px-6 py-20 text-center md:px-10 lg:px-16"
      >
        <p class="text-xs uppercase tracking-[0.22em] text-night-soft">
          {{ copy.workKicker }}
        </p>
        <h2
          class="mt-6 max-w-4xl font-serif text-[clamp(3rem,6.5vw,6.25rem)] leading-[0.92] tracking-tight"
        >
          {{ copy.workTitle }}
        </h2>
        <p class="mt-6 max-w-md text-lg leading-relaxed">
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
            class="mt-6 font-serif text-[clamp(2.5rem,4.6vw,4.6rem)] leading-[0.92] tracking-tight"
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
          <p class="mt-6 max-w-md text-lg leading-relaxed">
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
</style>
