<script setup lang="ts">
import { desktopMotion, useScrollScene } from '~/composables/useScrollScene'
import { useLocale } from '~/composables/useLocale'

const { copy } = useLocale()
const root = ref<HTMLElement | null>(null)

useScrollScene(root, ({ gsap, mm }) => {
  mm.add(desktopMotion, () => {
    const sentences = root.value?.querySelectorAll('.js-rise')
    if (!sentences?.length || !root.value) return

    gsap.from(sentences, {
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
  <section id="intro" ref="root" class="border-t border-ink/15 bg-paper px-6 py-24 md:px-10 md:py-32 lg:px-16">
    <div class="grid items-start gap-10 md:grid-cols-12">
      <div class="md:col-span-4">
        <h2 class="font-serif text-[clamp(4.5rem,8vw,7.5rem)] leading-none tracking-tight">01</h2>
        <p class="mt-4 text-xs uppercase tracking-[0.22em]">{{ copy.introLabel }}</p>
      </div>
      <div class="flex items-start gap-5 md:col-span-8 md:gap-8">
        <div class="relative size-[7.5rem] shrink-0 overflow-hidden rounded-full ring-1 ring-ink/15 md:size-[10.5rem]">
          <!-- 860px window at (634, 126) on the 1818×1228 photo. -->
          <img
            src="/imgs/pfp.jpg"
            :alt="copy.name"
            width="1818"
            height="1228"
            class="absolute left-[-73.721%] top-[-14.651%] h-auto w-[211.395%] max-w-none"
          >
        </div>
        <div class="flex min-w-0 flex-col gap-8">
          <p
            v-for="(line, index) in copy.profile"
            :key="index"
            class="js-rise max-w-3xl font-serif text-[clamp(1.7rem,2.7vw,2.45rem)] leading-[1.28]"
          >
            {{ line }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
