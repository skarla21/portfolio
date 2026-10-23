<script setup lang="ts">
import { desktopMotion, useScrollScene } from '~/composables/useScrollScene'
import { useLocale } from '~/composables/useLocale'

const { copy } = useLocale()
const root = ref<HTMLElement | null>(null)

useScrollScene(root, ({ gsap, mm }) => {
  mm.add(desktopMotion, () => {
    const quotes = root.value?.querySelectorAll('.js-rise')
    if (!quotes?.length || !root.value) return

    gsap.from(quotes, {
      y: 28,
      duration: 0.9,
      ease: 'power3.out',
      stagger: 0.07,
      scrollTrigger: {
        trigger: root.value,
        start: 'top 75%',
        once: true,
      },
    })
  })
})
</script>

<template>
  <section id="recommendations" ref="root" class="bg-mist px-6 py-24 md:px-10 md:py-32 lg:px-16">
    <p class="text-xs uppercase tracking-[0.22em]">{{ copy.recommendationsKicker }}</p>
    <h2
      class="mt-3 max-w-4xl font-serif text-[clamp(2.35rem,4.8vw,4.25rem)] leading-[0.95] tracking-tight text-balance"
    >
      {{ copy.recommendationsTitle }}
    </h2>

    <div class="mt-14 grid gap-x-12 gap-y-16 md:mt-20 md:grid-cols-3">
      <figure
        v-for="recommendation in copy.recommendations"
        :key="recommendation.id"
        class="js-rise flex flex-col"
      >
        <blockquote class="font-serif text-[clamp(1.2rem,1.45vw,1.5rem)] italic leading-snug">
          {{ recommendation.quote }}
        </blockquote>
        <figcaption class="mt-auto flex items-center gap-3 pt-8">
          <img
            :src="recommendation.image"
            :alt="recommendation.name"
            width="48"
            height="48"
            class="h-12 w-12 shrink-0 rounded-full object-cover"
            :style="{ objectPosition: recommendation.imagePosition }"
          >
          <div>
            <p class="text-sm font-medium leading-snug">
              {{ recommendation.name }}
            </p>
            <p class="mt-0.5 text-sm leading-snug text-mute">
              {{ recommendation.role }}
            </p>
            <a
              :href="recommendation.href"
              target="_blank"
              rel="noopener noreferrer"
              class="mt-1 inline-block text-sm underline underline-offset-4"
            >
              LinkedIn
            </a>
          </div>
        </figcaption>
      </figure>
    </div>
  </section>
</template>
