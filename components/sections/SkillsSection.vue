<script setup lang="ts">
import SkillMark from '~/components/sections/SkillMark.vue'
import { skills } from '~/content/skills'
import { useLocale } from '~/composables/useLocale'

const { copy } = useLocale()
const loopCopies = 6
</script>

<template>
  <section class="bg-mist px-6 py-16 md:px-10 md:py-20 lg:px-16" aria-labelledby="skills-heading">
    <h2 id="skills-heading" class="sr-only">{{ copy.skillsLabel }}</h2>
    <div class="skill-viewport">
      <div class="skill-run" :style="{ '--copies': loopCopies }">
        <ul
          v-for="copyIndex in loopCopies"
          :key="copyIndex"
          class="skill-row"
          :class="{ 'skill-extra': copyIndex > 1 }"
          :aria-hidden="copyIndex > 1 ? 'true' : undefined"
        >
          <li v-for="skill in skills" :key="`${skill.title}-${copyIndex}`">
            <SkillMark :skill="skill" :labelled="copyIndex === 1" />
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.skill-viewport {
  overflow: hidden;
  margin-inline: -1.5rem;
  padding-top: 2.4rem;
}

.skill-run {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem 1.15rem;
}

.skill-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem 1.15rem;
}

.skill-extra {
  display: none;
}

@media (min-width: 768px) {
  .skill-viewport {
    margin-inline: -2.5rem;
  }
}

@media (min-width: 1024px) {
  .skill-viewport {
    margin-inline: -4rem;
  }
}

@media (min-width: 768px) and (prefers-reduced-motion: no-preference) {
  .skill-run {
    flex-wrap: nowrap;
    gap: 0;
    width: max-content;
    animation: marquee 45s linear infinite;
  }

  .skill-run:hover,
  .skill-run:focus-within {
    animation-play-state: paused;
  }

  .skill-row,
  .skill-extra {
    display: flex;
    flex-wrap: nowrap;
    gap: 1.15rem;
    padding-right: 1.15rem;
  }
}

@keyframes marquee {
  from {
    transform: translateX(0);
  }

  to {
    transform: translateX(calc(-100% / var(--copies)));
  }
}
</style>
