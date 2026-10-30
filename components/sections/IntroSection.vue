<script setup lang="ts">
import { desktopMotion, useScrollScene } from '~/composables/useScrollScene'
import { useLocale } from '~/composables/useLocale'

const { copy } = useLocale()
const root = ref<HTMLElement | null>(null)

const firstLine = computed(() => copy.value.profile[0] ?? '')
const restLines = computed(() => copy.value.profile.slice(1))

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
    <div class="relative">
      <div class="mb-10 md:absolute md:left-0 md:top-0 md:mb-0">
        <h2 class="font-serif text-[clamp(4.5rem,8vw,7.5rem)] leading-none tracking-tight">01</h2>
        <p class="mt-4 text-xs uppercase tracking-[0.22em]">{{ copy.introLabel }}</p>
      </div>

      <div class="mx-auto flex max-w-3xl flex-col gap-8">
        <div
          class="flex flex-col gap-5 font-display text-[clamp(1.05rem,1.55vw,1.35rem)] leading-[1.45] md:flex-row md:items-start md:gap-5"
        >
          <div
            class="relative mx-auto aspect-square h-[calc(3*1.45*1em)] shrink-0 overflow-hidden rounded-full ring-1 ring-ink/15 md:mx-0"
          >
            <!-- 860px window at (634, 126) on the 1818×1228 photo. -->
            <img
              src="/imgs/pfp.jpg"
              :alt="copy.name"
              width="1818"
              height="1228"
              class="absolute left-[-73.721%] top-[-14.651%] h-auto w-[211.395%] max-w-none"
            >
          </div>
          <p class="js-rise w-full min-w-0 md:flex-1">
            {{ firstLine }}
          </p>
        </div>
        <p
          v-for="(line, index) in restLines"
          :key="index"
          class="js-rise font-display text-[clamp(1.05rem,1.55vw,1.35rem)] leading-[1.45]"
        >
          {{ line }}
        </p>
      </div>
    </div>
  </section>
</template>
