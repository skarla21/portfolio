<script setup lang="ts">
import { markColor, type SkillMark } from '~/content/skills'

const props = defineProps<{
  skill: SkillMark
  labelled?: boolean
}>()

const color = computed(() => markColor(props.skill.hex))
</script>

<template>
  <button v-if="labelled" type="button" class="mark" :aria-label="skill.title">
    <svg v-if="skill.path" viewBox="0 0 24 24" aria-hidden="true">
      <path fill="currentColor" fill-rule="evenodd" :d="skill.path" />
    </svg>
    <span v-else class="letters" aria-hidden="true">{{ skill.letters }}</span>
    <span class="tip" aria-hidden="true">{{ skill.title }}</span>
  </button>
  <span v-else class="mark">
    <svg v-if="skill.path" viewBox="0 0 24 24" aria-hidden="true">
      <path fill="currentColor" fill-rule="evenodd" :d="skill.path" />
    </svg>
    <span v-else class="letters">{{ skill.letters }}</span>
    <span class="tip" aria-hidden="true">{{ skill.title }}</span>
  </span>
</template>

<style scoped>
.mark {
  position: relative;
  display: grid;
  width: 4.5rem;
  height: 4.5rem;
  min-width: 4.5rem;
  min-height: 4.5rem;
  max-width: 4.5rem;
  max-height: 4.5rem;
  place-items: center;
  border-radius: 999px;
  background: #14120e;
  color: v-bind(color);
}

.mark svg {
  width: 1.7rem;
  height: 1.7rem;
  min-width: 0;
  min-height: 0;
  max-width: 1.7rem;
  max-height: 1.7rem;
}

.letters {
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.04em;
}

.mark:hover,
.mark:focus-visible {
  z-index: 3;
}
</style>
