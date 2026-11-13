<script setup lang="ts">
import ContactSection from '~/components/sections/ContactSection.vue'
import HobbiesSection from '~/components/sections/HobbiesSection.vue'
import IntroSection from '~/components/sections/IntroSection.vue'
import JourneySection from '~/components/sections/JourneySection.vue'
import ProjectsShowcase from '~/components/sections/ProjectsShowcase.vue'
import RecommendationsSection from '~/components/sections/RecommendationsSection.vue'
import ServicesTeaser from '~/components/sections/ServicesTeaser.vue'
import SkillsSection from '~/components/sections/SkillsSection.vue'
</script>

<template>
  <main>
    <IntroSection />
    <JourneySection />
    <SkillsSection />
    <ServicesTeaser />
    <ProjectsShowcase />
    <RecommendationsSection />
    <HobbiesSection />
    <ContactSection />
  </main>
</template>
