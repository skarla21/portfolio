<script setup lang="ts">
import SkillMark from '~/components/sections/SkillMark.vue'
import { skills } from '~/content/skills'
import { useLocale } from '~/composables/useLocale'

const { copy } = useLocale()
</script>

<template>
  <section class="bg-mist px-6 py-16 md:px-10 md:py-20 lg:px-16" aria-labelledby="skills-heading">
    <h2 id="skills-heading" class="sr-only">{{ copy.skillsLabel }}</h2>
    <div class="skill-viewport">
      <div class="skill-run">
        <ul class="skill-row">
          <li v-for="skill in skills" :key="skill.title">
            <SkillMark :skill="skill" labelled />
          </li>
        </ul>
        <ul class="skill-row skill-clone" aria-hidden="true">
          <li v-for="skill in skills" :key="`${skill.title}-clone`">
            <SkillMark :skill="skill" />
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.skill-viewport {
  overflow: hidden;
  padding-top: 2.4rem;
}

.skill-run {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem 1.15rem;
}

.skill-row {
  display: contents;
}

.skill-clone {
  display: none;
}

@media (min-width: 768px) and (prefers-reduced-motion: no-preference) {
  .skill-run {
    flex-wrap: nowrap;
    gap: 0;
    width: max-content;
    animation: marquee 55s linear infinite;
  }

  .skill-run:hover,
  .skill-run:focus-within {
    animation-play-state: paused;
  }

  .skill-row {
    display: flex;
    gap: 1.15rem;
    padding-right: 1.15rem;
  }

  .skill-clone {
    display: flex;
  }
}

@keyframes marquee {
  from {
    transform: translateX(0);
  }

  to {
    transform: translateX(-50%);
  }
}
</style>
