<script setup lang="ts">
import { desktopMotion, useScrollScene } from '~/composables/useScrollScene'
import { useLocale } from '~/composables/useLocale'

const { copy } = useLocale()
const root = ref<HTMLElement | null>(null)
const track = ref<HTMLElement | null>(null)

useScrollScene(root, ({ gsap, ScrollTrigger, mm }) => {
  mm.add(desktopMotion, () => {
    const section = root.value
    const row = track.value
    if (!section || !row) return

    const panels = Array.from(row.querySelectorAll<HTMLElement>('.project-panel'))

    const sizePanels = () => {
      const width = section.offsetWidth
      if (!width) return
      panels.forEach((panel) => {
        panel.style.width = `${width}px`
      })
    }

    const distance = () => Math.max(0, row.scrollWidth - section.offsetWidth)

    sizePanels()
    ScrollTrigger.addEventListener('refreshInit', sizePanels)

    gsap.to(row, {
      x: () => -distance(),
      ease: 'none',
      scrollTrigger: {
        trigger: section,
        start: 'top top',
        end: () => `+=${distance()}`,
        pin: true,
        scrub: 1,
        invalidateOnRefresh: true,
        anticipatePin: 1,
      },
    })

    return () => {
      ScrollTrigger.removeEventListener('refreshInit', sizePanels)
      panels.forEach((panel) => {
        panel.style.width = ''
      })
    }
  })
})
</script>

<template>
  <section id="work" ref="root" class="bg-night text-paper md:motion-safe:h-dvh md:motion-safe:overflow-hidden">
    <div ref="track" class="flex flex-col md:motion-safe:h-dvh md:motion-safe:w-max md:motion-safe:flex-row">
      <article class="project-panel flex flex-col justify-center px-6 py-20 md:px-10 lg:px-16">
        <p class="text-xs uppercase tracking-[0.22em] text-night-soft">{{ copy.workKicker }}</p>
        <h2 class="mt-6 max-w-4xl font-serif text-[clamp(3rem,6.5vw,6.25rem)] leading-[0.92] tracking-tight">
          {{ copy.workTitle }}
        </h2>
        <p class="mt-6 max-w-md text-lg leading-relaxed">{{ copy.workIntro }}</p>
      </article>

      <article
        v-for="project in copy.projects"
        :key="project.id"
        class="project-panel grid gap-8 px-6 py-16 md:px-10 lg:px-16"
      >
        <div class="flex flex-col justify-center">
          <p class="text-sm uppercase tracking-[0.16em] text-night-soft">
            {{ project.stack }}<span v-if="project.dates"> / {{ project.dates }}</span>
          </p>
          <h3 class="mt-6 font-serif text-[clamp(2.5rem,4.6vw,4.6rem)] leading-[0.92] tracking-tight">
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
          <p class="mt-6 max-w-md text-lg leading-relaxed">{{ project.summary }}</p>
        </div>
        <div
          class="flex min-h-56 items-end p-6 md:motion-safe:my-8 md:motion-safe:min-h-0"
          :style="{ backgroundColor: project.accent }"
        />
      </article>
    </div>
  </section>
</template>

<style scoped>
@media (min-width: 768px) and (prefers-reduced-motion: no-preference) {
  .project-panel {
    display: grid;
    width: 100vw;
    height: 100dvh;
    flex-shrink: 0;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    align-items: stretch;
    column-gap: 3rem;
    padding: calc(var(--nav-h) + 1.5rem) 2.5rem 2.5rem;
  }

  .project-panel:first-child {
    display: flex;
  }
}

@media (min-width: 1024px) and (prefers-reduced-motion: no-preference) {
  .project-panel {
    padding-right: 4rem;
    padding-left: 4rem;
  }
}
</style>
