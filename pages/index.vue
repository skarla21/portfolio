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
import { profilePage, share } from '~/content/site'
import { useLocale } from '~/composables/useLocale'

const { copy } = useLocale()

useSeoMeta({
  title: computed(() => copy.value.seoTitle),
  description: computed(() => copy.value.seoDescription),
  ogTitle: share.title,
  ogDescription: share.description,
  ogImage: share.image,
  ogImageAlt: share.title,
  ogImageWidth: 1200,
  ogImageHeight: 630,
  ogUrl: profilePage.url,
  ogType: 'profile',
  ogLocale: 'el_GR',
  twitterCard: 'summary_large_image',
  twitterTitle: share.title,
  twitterDescription: share.description,
  twitterImage: share.image,
  twitterImageAlt: share.title,
})

useHead({
  link: [{ rel: 'canonical', href: profilePage.url }],
  meta: [{ property: 'og:locale:alternate', content: 'en_US' }],
  script: [
    {
      key: 'ld-profile',
      type: 'application/ld+json',
      innerHTML: JSON.stringify(profilePage),
    },
  ],
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
