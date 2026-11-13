<script setup lang="ts">
import { useLocale } from '~/composables/useLocale'
import type { Locale } from '~/content/site'

const { locale, copy, setLocale } = useLocale()
const header = ref<HTMLElement | null>(null)
const bar = ref<HTMLElement | null>(null)
const menuOpen = ref(false)

const menuId = 'site-nav-menu'
const menuLabel = computed(() =>
  locale.value === 'el' ? 'Ενότητες' : 'Sections',
)
const menuToggleLabel = computed(() => {
  if (locale.value === 'el') {
    return menuOpen.value ? 'Κλείσιμο μενού' : 'Άνοιγμα μενού'
  }
  return menuOpen.value ? 'Close menu' : 'Open menu'
})

function toggleLocale() {
  const next: Locale = locale.value === 'el' ? 'en' : 'el'
  setLocale(next)
}

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

function closeMenu() {
  menuOpen.value = false
}

function syncNavHeight() {
  const el = bar.value ?? header.value
  if (!el) return
  document.documentElement.style.setProperty('--nav-h', `${el.offsetHeight}px`)
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') closeMenu()
}

function onResize() {
  if (window.matchMedia('(min-width: 768px)').matches) closeMenu()
  syncNavHeight()
}

onMounted(() => {
  syncNavHeight()
  window.addEventListener('resize', onResize)
  window.addEventListener('keydown', onKeydown)
})

watch(locale, async () => {
  await nextTick()
  syncNavHeight()
})

watch(menuOpen, async () => {
  await nextTick()
  syncNavHeight()
})

onUnmounted(() => {
  window.removeEventListener('resize', onResize)
  window.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <header
    ref="header"
    class="fixed inset-x-0 top-0 z-50 border-b border-ink/10 bg-paper/95"
  >
    <div
      ref="bar"
      class="flex items-center gap-x-3 px-4 py-2.5 md:h-[var(--nav-h)] md:gap-x-5 md:px-10 md:py-0 lg:px-16"
    >
      <button
        type="button"
        class="menu-toggle inline-flex h-10 w-10 shrink-0 items-center justify-center md:hidden"
        :aria-expanded="menuOpen"
        :aria-controls="menuId"
        :aria-label="menuToggleLabel"
        @click="toggleMenu"
      >
        <span class="menu-toggle-icon" :data-open="menuOpen" aria-hidden="true" />
      </button>

      <a
        href="#intro"
        class="min-w-0 flex-1 truncate font-serif text-lg leading-none tracking-tight md:flex-none md:text-xl"
        @click="closeMenu"
      >
        {{ copy.name }}
      </a>

      <nav
        class="ml-auto hidden items-center gap-x-4 text-sm md:flex"
        :aria-label="menuLabel"
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

      <div class="flex shrink-0 items-center gap-2">
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
    </div>

    <div
      v-show="menuOpen"
      :id="menuId"
      class="border-t border-ink/10 bg-paper px-4 py-3 md:hidden"
    >
      <nav class="flex flex-col" :aria-label="menuLabel">
        <a
          v-for="link in copy.nav"
          :key="link.href"
          :href="link.href"
          class="border-b border-ink/10 px-1 py-3 text-base last:border-b-0 hover:underline"
          @click="closeMenu"
        >
          {{ link.label }}
        </a>
      </nav>
    </div>
  </header>

  <button
    v-if="menuOpen"
    type="button"
    class="fixed inset-0 z-40 bg-ink/20 md:hidden"
    :aria-label="locale === 'el' ? 'Κλείσιμο μενού' : 'Close menu'"
    @click="closeMenu"
  />
</template>

<style scoped>
.menu-toggle-icon {
  position: relative;
  display: block;
  width: 1.15rem;
  height: 1px;
  background: currentColor;
}

.menu-toggle-icon::before,
.menu-toggle-icon::after {
  content: '';
  position: absolute;
  left: 0;
  width: 100%;
  height: 1px;
  background: currentColor;
  transition: transform 160ms ease, top 160ms ease;
}

.menu-toggle-icon::before {
  top: -0.35rem;
}

.menu-toggle-icon::after {
  top: 0.35rem;
}

.menu-toggle-icon[data-open='true'] {
  background: transparent;
}

.menu-toggle-icon[data-open='true']::before {
  top: 0;
  transform: rotate(45deg);
}

.menu-toggle-icon[data-open='true']::after {
  top: 0;
  transform: rotate(-45deg);
}
</style>
