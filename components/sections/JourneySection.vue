<script setup lang="ts">
import { desktopMotion, useScrollScene } from '~/composables/useScrollScene'
import { useLocale } from '~/composables/useLocale'
import type { Job, Study } from '~/content/site'

type Milestone =
  | { kind: 'study'; key: string; item: Study }
  | { kind: 'job'; key: string; item: Job }

const { copy } = useLocale()

const milestones = computed<Milestone[]>(() => [
  { kind: 'study', key: 'bsc', item: copy.value.education[0] },
  { kind: 'job', key: 'iasa-research', item: copy.value.work[3] },
  { kind: 'study', key: 'msc', item: copy.value.education[1] },
  { kind: 'job', key: 'iasa-data', item: copy.value.work[2] },
  { kind: 'job', key: 'performance', item: copy.value.work[1] },
  { kind: 'job', key: 'factset', item: copy.value.work[0] },
])

const root = ref<HTMLElement | null>(null)

useScrollScene(root, ({ gsap, mm }) => {
  mm.add(desktopMotion, () => {
    const line = root.value?.querySelector('.journey-line')
    if (line && root.value) {
      gsap.to(line, {
        scaleY: 1,
        ease: 'none',
        scrollTrigger: {
          trigger: root.value,
          start: 'top 70%',
          end: 'bottom 75%',
          scrub: true,
        },
      })
    }

    root.value?.querySelectorAll('.js-rise').forEach((card) => {
      gsap.from(card, {
        y: 32,
        duration: 0.8,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: card,
          start: 'top 88%',
          once: true,
        },
      })
    })
  })
})
</script>

<template>
  <section id="journey" ref="root" class="bg-mist px-6 pb-20 pt-24 md:px-10 md:pb-24 md:pt-32 lg:px-16">
    <div class="max-w-3xl">
      <p class="text-xs uppercase tracking-[0.22em]">02</p>
      <h2 class="mt-3 font-serif text-[clamp(3rem,6vw,5.5rem)] leading-[0.95] tracking-tight">
        {{ copy.journeyTitle }}
      </h2>
      <p class="mt-6 max-w-xl text-lg">{{ copy.journeyLede }}</p>
    </div>

    <div class="relative mt-16 md:mt-24">
      <div class="journey-line" aria-hidden="true" />
      <ol class="relative space-y-16 md:space-y-24">
        <li v-for="(milestone, index) in milestones" :key="milestone.key" class="md:grid md:grid-cols-2">
          <article
            class="js-rise max-w-xl pl-8"
            :class="index % 2 === 0 ? 'md:ml-auto md:pl-0 md:pr-14' : 'md:col-start-2 md:pl-14'"
          >
            <template v-if="milestone.kind === 'study'">
              <p class="text-sm uppercase tracking-[0.16em] text-mute">{{ milestone.item.dates }}</p>
              <h3 class="mt-3 font-serif text-[clamp(2rem,3vw,2.75rem)] leading-tight">
                {{ milestone.item.credential }}
              </h3>
              <p class="mt-3 text-lg">{{ milestone.item.school }}</p>
              <p class="mt-1 text-lg">{{ milestone.item.detail }}</p>
              <p class="mt-5 text-lg">
                <a
                  v-if="milestone.item.thesisHref"
                  :href="milestone.item.thesisHref"
                  class="underline decoration-1 underline-offset-[5px]"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {{ milestone.item.thesisLabel }}: {{ milestone.item.thesis }}
                </a>
                <template v-else>{{ milestone.item.thesisLabel }}: {{ milestone.item.thesis }}</template>
              </p>
              <p class="mt-2 text-base text-mute">
                {{ copy.supervisorsLabel }}: {{ milestone.item.supervisors }}
              </p>
            </template>
            <template v-else>
              <p class="text-sm uppercase tracking-[0.16em] text-mute">{{ milestone.item.dates }}</p>
              <h3 class="mt-3 font-serif text-[clamp(2rem,3vw,2.75rem)] leading-tight">
                {{ milestone.item.role }}
              </h3>
              <p class="mt-3 text-lg">{{ milestone.item.place }}</p>
              <ul class="mt-5 list-disc space-y-2 pl-5 text-lg">
                <li v-for="point in milestone.item.points" :key="point">{{ point }}</li>
              </ul>
            </template>
          </article>
        </li>
      </ol>
    </div>

    <div class="mt-20 grid gap-12 border-t border-ink/15 pt-12 md:grid-cols-2">
      <div>
        <h3 class="text-xs uppercase tracking-[0.22em]">{{ copy.languagesLabel }}</h3>
        <ul class="mt-5 space-y-2 text-lg">
          <li v-for="language in copy.languages" :key="language">{{ language }}</li>
        </ul>
      </div>
      <div>
        <h3 class="text-xs uppercase tracking-[0.22em]">{{ copy.certificatesLabel }}</h3>
        <ul class="mt-5 space-y-2 text-lg">
          <li v-for="certificate in copy.certificates" :key="certificate.label">
            <a
              v-if="certificate.href"
              :href="certificate.href"
              class="underline decoration-1 underline-offset-[5px]"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ certificate.label }}
            </a>
            <template v-else>{{ certificate.label }}</template>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.journey-line {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0.35rem;
  width: 1px;
  background: currentColor;
  transform-origin: top center;
  pointer-events: none;
}

@media (min-width: 768px) {
  .journey-line {
    left: calc(50% - 0.5px);
  }
}

@media (min-width: 768px) and (prefers-reduced-motion: no-preference) {
  .journey-line {
    transform: scaleY(0);
  }
}
</style>
