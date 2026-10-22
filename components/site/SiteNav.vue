<script setup lang="ts">
import { useLocale } from '~/composables/useLocale'
import type { Locale } from '~/content/site'

const { locale, copy, setLocale } = useLocale()

function toggleLocale() {
  const next: Locale = locale.value === 'el' ? 'en' : 'el'
  setLocale(next)
}
</script>

<template>
  <header class="fixed inset-x-0 top-0 z-50 border-b border-ink/10 bg-paper/95">
    <div class="grid h-[var(--nav-h)] grid-cols-[1fr_auto] items-center gap-x-4 gap-y-1 px-6 md:flex md:gap-x-5 md:px-10 lg:px-16">
      <a href="#top" class="min-w-0 truncate font-serif text-lg leading-none tracking-tight md:text-xl">
        {{ copy.name }}
      </a>
      <div class="flex items-center gap-2 md:order-last">
        <button
          type="button"
          class="px-1.5 py-1 text-sm underline underline-offset-4"
          :aria-label="locale === 'el' ? 'Γλώσσα, Ελληνικά' : 'Language, English'"
          @click="toggleLocale"
        >
          {{ locale === 'el' ? 'EL' : 'EN' }}
        </button>
        <a
          :href="copy.cv"
          class="border border-ink px-2.5 py-1 text-sm hover:bg-ink hover:text-paper"
        >
          CV
        </a>
      </div>
      <nav
        class="col-span-2 flex gap-x-4 overflow-x-auto text-sm md:col-auto md:ml-auto"
        :aria-label="locale === 'el' ? 'Ενότητες' : 'Sections'"
      >
        <a
          v-for="link in copy.nav"
          :key="link.href"
          :href="link.href"
          class="shrink-0 underline-offset-4 hover:underline"
        >
          {{ link.label }}
        </a>
      </nav>
    </div>
  </header>
</template>
