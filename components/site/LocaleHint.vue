<script setup lang="ts">
import { useLocale } from '~/composables/useLocale'

const { locale, alternatePath, prefer } = useLocale()
const dismissed = ref(true)

onMounted(() => {
  try {
    dismissed.value = sessionStorage.getItem('locale-hint-dismissed') === '1'
  } catch {
    dismissed.value = false
  }
})

const show = computed(
  () => !dismissed.value && locale.value === 'el' && prefer.value === 'en',
)

function dismiss() {
  dismissed.value = true
  try {
    sessionStorage.setItem('locale-hint-dismissed', '1')
  } catch {
    /* ignore */
  }
}
</script>

<template>
  <div
    v-if="show"
    class="fixed bottom-4 left-4 right-4 z-[60] mx-auto flex max-w-lg items-center justify-between gap-3 border border-ink bg-paper px-4 py-3 text-sm shadow-sm md:left-auto md:right-6 md:mx-0"
    role="status"
  >
    <p>
      Continue in
      <NuxtLink
        :to="alternatePath()"
        class="underline underline-offset-4"
        @click="dismiss"
      >
        English
      </NuxtLink>
      ?
    </p>
    <button
      type="button"
      class="shrink-0 px-2 py-1 text-mute underline-offset-4 hover:underline"
      aria-label="Dismiss language hint"
      @click="dismiss"
    >
      Dismiss
    </button>
  </div>
</template>
