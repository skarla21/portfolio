<script setup lang="ts">
import { desktopMotion, useScrollScene } from "~/composables/useScrollScene";
import { useLocale } from "~/composables/useLocale";

const { copy } = useLocale();
const root = ref<HTMLElement | null>(null);
const track = ref<HTMLElement | null>(null);
const mediaReady = ref<Record<string, boolean>>({});
const posterReady = ref<Record<string, boolean>>({});
const frameShown = ref<Record<string, boolean>>({});
const frames = new Map<string, HTMLVideoElement>();
let frameObserver: IntersectionObserver | undefined;
let reduceMotion = false;

const frameRefs = new Map<string, (el: unknown) => void>();

function frameRef(id: string) {
  const existing = frameRefs.get(id);
  if (existing) return existing;
  const register = (el: unknown) => {
    const node = el instanceof HTMLVideoElement ? el : null;
    const current = frames.get(id) ?? null;
    if (current === node) return;
    if (node) frames.set(id, node);
    else frames.delete(id);
    observeFrames();
  };
  frameRefs.set(id, register);
  return register;
}

function observeFrames() {
  if (!frameObserver) return;
  frameObserver.disconnect();
  frames.forEach((video) => frameObserver?.observe(video));
}

function arm(video: HTMLVideoElement) {
  const src = video.dataset.src;
  if (!src || video.dataset.armed === "1") return;
  video.dataset.armed = "1";
  video.muted = true;
  video.defaultMuted = true;
  video.playsInline = true;
  video.src = src;
  video.load();
}

function bindPlayback() {
  if (frameObserver) return;
  frameObserver = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        const video = entry.target;
        if (!(video instanceof HTMLVideoElement)) continue;
        if (entry.intersectionRatio >= 0.15) arm(video);
        if (reduceMotion || entry.intersectionRatio < 0.6) {
          video.pause();
        } else {
          void video.play().catch(() => {});
        }
      }
    },
    { threshold: [0, 0.15, 0.6] },
  );
  observeFrames();
}

async function fileExists(url: string) {
  try {
    const response = await fetch(url, { method: "HEAD", cache: "no-store" });
    return response.ok;
  } catch {
    return false;
  }
}

function posterLoads(url: string) {
  return new Promise<boolean>((resolve) => {
    const image = new Image();
    image.onload = () => resolve(true);
    image.onerror = () => resolve(false);
    image.src = url;
  });
}

function revealMedia() {
  for (const project of copy.value.projects) {
    if (mediaReady.value[project.id] || !project.video) continue;
    const videoUrl = project.video;
    const posterUrl = project.poster;
    void (async () => {
      const videoOk = await fileExists(videoUrl);
      if (!videoOk) return;
      if (posterUrl && (await posterLoads(posterUrl))) {
        posterReady.value = { ...posterReady.value, [project.id]: true };
      }
      mediaReady.value = { ...mediaReady.value, [project.id]: true };
      nextTick(observeFrames);
    })();
  }
}

function onFrameReady(id: string) {
  frameShown.value = { ...frameShown.value, [id]: true };
}

function onFrameError(id: string, event: Event) {
  const video = event.target;
  if (!(video instanceof HTMLVideoElement) || video.dataset.armed !== "1")
    return;
  video.pause();
  const next = { ...mediaReady.value };
  // eslint-disable-next-line @typescript-eslint/no-dynamic-delete
  delete next[id];
  mediaReady.value = next;
}

onMounted(() => {
  reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  revealMedia();
  bindPlayback();
});

onUnmounted(() => {
  frameObserver?.disconnect();
  frames.forEach((video) => video.pause());
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
  <section
    id="work"
    ref="root"
    class="bg-night text-paper md:motion-safe:h-dvh md:motion-safe:overflow-hidden"
  >
    <div
      ref="track"
      class="flex flex-col md:motion-safe:h-dvh md:motion-safe:w-max md:motion-safe:flex-row"
    >
      <article
        class="project-panel flex flex-col justify-center px-6 py-20 md:px-10 lg:px-16"
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
        <div class="project-stage" :style="{ backgroundColor: project.accent }">
          <video
            v-if="project.video && mediaReady[project.id]"
            :ref="frameRef(project.id)"
            class="project-frame"
            :class="{
              'is-pending': !posterReady[project.id] && !frameShown[project.id],
            }"
            :poster="posterReady[project.id] ? project.poster : undefined"
            :data-src="project.video"
            muted
            loop
            playsinline
            preload="none"
            tabindex="-1"
            aria-hidden="true"
            @loadeddata="onFrameReady(project.id)"
            @error="onFrameError(project.id, $event)"
          />
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.project-stage {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 22rem;
  min-width: 0;
  aspect-ratio: 4 / 5;
  padding: 1.25rem;
  overflow: hidden;
}

.project-frame {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  pointer-events: none;
  background: transparent;
}

.project-frame.is-pending {
  opacity: 0;
}

@media (min-width: 768px) and (prefers-reduced-motion: no-preference) {
  .project-stage {
    flex: 0 0 auto;
    width: min(26rem, calc((100dvh - var(--nav-h) - 5rem) * 4 / 5));
    max-width: 26rem;
    max-height: 100%;
  }

  .project-panel {
    --project-copy: 22rem;
    --project-media: min(26rem, calc((100dvh - var(--nav-h) - 5rem) * 4 / 5));
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
    align-items: stretch;
    padding-right: 4rem;
    padding-left: 4rem;
  }

  .project-panel:first-child > :first-child {
    flex: none;
  }

  .project-panel:nth-child(n + 3) {
    margin-left: var(--project-span);
  }

  .project-panel:last-child {
    padding-right: 4rem;
  }
}
</style>
