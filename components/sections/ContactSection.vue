<script setup lang="ts">
import { desktopMotion, useScrollScene } from '~/composables/useScrollScene'
import { useLocale } from '~/composables/useLocale'

const { copy } = useLocale()
const root = ref<HTMLElement | null>(null)

useScrollScene(root, ({ gsap, mm }) => {
  mm.add(desktopMotion, () => {
    const heading = root.value?.querySelector('.js-rise')
    if (!heading || !root.value) return

    gsap.from(heading, {
      y: 28,
      duration: 0.9,
      ease: 'power3.out',
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
  <section
    id="contact"
    ref="root"
    class="flex min-h-dvh flex-col justify-between bg-ink px-6 pb-10 pt-28 text-paper md:px-10 md:pt-36 lg:px-16"
  >
    <p class="text-xs uppercase tracking-[0.22em] text-night-soft">{{ copy.contactKicker }}</p>

    <div class="flex max-w-full flex-col gap-10">
      <h2 class="js-rise max-w-full font-serif text-[clamp(2rem,7.5vw,7.5rem)] leading-[0.9] tracking-tight">
        {{ copy.contactTitle }}
      </h2>
      <ul class="max-w-xl space-y-4 font-serif text-[clamp(1.6rem,2.4vw,2.15rem)] leading-snug">
        <li>
          <a class="underline decoration-1 underline-offset-[6px]" :href="`mailto:${copy.email}`">
            {{ copy.email }}
          </a>
        </li>
        <li>
          <a class="underline decoration-1 underline-offset-[6px]" :href="copy.phoneHref">
            {{ copy.phone }}
          </a>
        </li>
        <li>
          <a
            class="underline decoration-1 underline-offset-[6px]"
            :href="copy.linkedin"
            target="_blank"
            rel="noopener noreferrer"
          >
            LinkedIn
          </a>
        </li>
        <li>
          <a
            class="underline decoration-1 underline-offset-[6px]"
            :href="copy.github"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
        </li>
        <li>
          <a class="underline decoration-1 underline-offset-[6px]" :href="copy.cv">
            {{ copy.cvLabel }}
          </a>
        </li>
      </ul>
    </div>

    <p class="text-sm text-night-soft">{{ copy.name }} · {{ copy.address }}</p>
  </section>
</template>
