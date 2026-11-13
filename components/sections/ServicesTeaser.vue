<script setup lang="ts">
import { desktopMotion, useScrollScene } from '~/composables/useScrollScene'
import { useLocale } from '~/composables/useLocale'
import { offeringsByLocale } from '~/content/offerings'

const { locale, localePath } = useLocale()
const offerings = computed(() => offeringsByLocale[locale.value])
const root = ref<HTMLElement | null>(null)

useScrollScene(root, ({ gsap, mm }) => {
  mm.add(desktopMotion, () => {
    const items = root.value?.querySelectorAll('.js-rise')
    if (!items?.length || !root.value) return

    gsap.from(items, {
      y: 28,
      duration: 0.9,
      ease: 'power3.out',
      stagger: 0.06,
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
    id="services"
    ref="root"
    class="border-b border-ink/15 bg-paper px-6 py-20 md:px-10 md:py-28 lg:px-16"
  >
    <div class="mx-auto max-w-3xl">
      <p class="js-rise text-xs uppercase tracking-[0.22em]">
        {{ offerings.servicesKicker }}
      </p>
      <h2
        class="js-rise mt-3 font-serif text-[clamp(1.75rem,4vw,3rem)] leading-[0.95] tracking-tight"
      >
        {{ offerings.servicesTitle }}
      </h2>
      <p class="js-rise mt-5 max-w-2xl text-lg leading-relaxed text-mute">
        {{ offerings.servicesIntro }}
      </p>

      <ul class="mt-10 space-y-5">
        <li
          v-for="item in offerings.offerings"
          :key="item.id"
          class="js-rise border-t border-ink/10 pt-5"
        >
          <p class="font-serif text-xl tracking-tight md:text-2xl">
            {{ item.title }}
          </p>
          <p class="mt-2 text-base leading-relaxed text-mute md:text-lg">
            {{ item.summary }}
          </p>
        </li>
      </ul>

      <NuxtLink
        :to="localePath('/services')"
        class="js-rise mt-10 inline-flex border border-ink px-4 py-2 text-sm hover:bg-ink hover:text-paper"
      >
        {{ offerings.servicesCta }}
      </NuxtLink>
    </div>
  </section>
</template>
