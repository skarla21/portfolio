<script setup lang="ts">
import LocaleHint from '~/components/site/LocaleHint.vue'
import SiteNav from '~/components/site/SiteNav.vue'
import { useLocale } from '~/composables/useLocale'

const { copy, localePath } = useLocale()
</script>

<template>
  <div>
    <a class="skip" :href="`${localePath('/')}#intro`">{{ copy.skip }}</a>
    <SiteNav />
    <slot />
    <LocaleHint />
  </div>
</template>
