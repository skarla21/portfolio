<script setup lang="ts">
import { useLocale } from '~/composables/useLocale'

const { locale } = useLocale()

useHead({
  htmlAttrs: {
    lang: () => locale.value,
  },
})

watch(locale, async () => {
  if (!import.meta.client) return
  await nextTick()
  const { gsap } = await import('gsap')
  const { ScrollTrigger } = await import('gsap/ScrollTrigger')
  gsap.registerPlugin(ScrollTrigger)
  ScrollTrigger.refresh()
})
</script>

<template>
  <NuxtPage />
</template>
