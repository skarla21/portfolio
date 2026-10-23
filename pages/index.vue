<script setup lang="ts">
import ContactSection from '~/components/sections/ContactSection.vue'
import HeroSection from '~/components/sections/HeroSection.vue'
import HobbiesSection from '~/components/sections/HobbiesSection.vue'
import IntroSection from '~/components/sections/IntroSection.vue'
import JourneySection from '~/components/sections/JourneySection.vue'
import ProjectsShowcase from '~/components/sections/ProjectsShowcase.vue'
import RecommendationsSection from '~/components/sections/RecommendationsSection.vue'
import SkillsSection from '~/components/sections/SkillsSection.vue'
import SiteNav from '~/components/site/SiteNav.vue'
import { useLocale } from '~/composables/useLocale'

const { copy } = useLocale()

useSeoMeta({
  title: computed(() => copy.value.name),
  description: computed(() => copy.value.seoDescription),
  ogTitle: computed(() => copy.value.name),
  ogDescription: computed(() => copy.value.profile[0]),
})
</script>

<template>
  <div>
    <a class="skip" href="#top">{{ copy.skip }}</a>
    <SiteNav />
    <main>
      <HeroSection />
      <IntroSection />
      <JourneySection />
      <SkillsSection />
      <ProjectsShowcase />
      <RecommendationsSection />
      <HobbiesSection />
      <ContactSection />
    </main>
  </div>
</template>
