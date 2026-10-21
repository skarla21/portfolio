<script setup lang="ts">
import { desktopMotion, useScrollScene } from '~/composables/useScrollScene'
import { useLocale } from '~/composables/useLocale'

const { copy } = useLocale()
const root = ref<HTMLElement | null>(null)

useScrollScene(root, ({ gsap, mm }) => {
  mm.add(desktopMotion, () => {
    const lines = root.value?.querySelectorAll('.js-rise')
    if (lines?.length) {
      gsap.from(lines, {
        y: 36,
        duration: 1.05,
        ease: 'power3.out',
        stagger: 0.08,
      })
    }

    const headline = root.value?.querySelector('.js-parallax')
    if (headline && root.value) {
      gsap.to(headline, {
        y: 40,
        ease: 'none',
        scrollTrigger: {
          trigger: root.value,
          start: 'top top',
          end: 'bottom top',
          scrub: true,
        },
      })
    }
  })
})
</script>

<template>
  <section
    id="top"
    ref="root"
    class="flex min-h-dvh flex-col justify-between bg-paper px-6 pb-8 pt-[calc(var(--nav-h)+1.75rem)] md:px-10 lg:px-16"
  >
    <div class="flex items-baseline justify-between gap-6 text-xs uppercase tracking-[0.22em]">
      <p>{{ copy.eyebrow }}</p>
      <p>{{ copy.place }}</p>
    </div>

    <div>
      <h1 class="js-parallax font-serif text-[clamp(2.75rem,12.5vw,10.5rem)] leading-[0.88] tracking-[-0.035em]">
        <span class="js-rise block">{{ copy.nameLines[0] }}</span>
        <span class="js-rise block">{{ copy.nameLines[1] }}</span>
      </h1>
      <div class="mt-8 flex flex-col gap-8 md:flex-row md:items-end md:justify-between">
        <p class="max-w-xl font-serif text-[clamp(1.7rem,3vw,2.45rem)] leading-snug">
          {{ copy.lede }}
        </p>
        <p class="text-sm uppercase tracking-[0.18em]">{{ copy.disciplines }}</p>
      </div>
    </div>

    <div class="flex items-end justify-between gap-6">
      <a href="#work" class="text-lg underline decoration-1 underline-offset-[6px]">
        {{ copy.viewProjects }}
      </a>
      <a href="#intro" class="inline-flex flex-col items-end gap-3 text-xs uppercase tracking-[0.18em]">
        {{ copy.scroll }}
        <span class="scroll-cue" aria-hidden="true" />
      </a>
    </div>
  </section>
</template>

<style scoped>
.scroll-cue {
  display: block;
  width: 1px;
  height: 3.25rem;
  background: currentColor;
  transform-origin: top center;
}

@media (prefers-reduced-motion: no-preference) {
  .scroll-cue {
    animation: cue 1.8s ease-in-out infinite;
  }
}

@keyframes cue {
  0%,
  100% {
    transform: scaleY(0.35);
  }

  50% {
    transform: scaleY(1);
  }
}
</style>
