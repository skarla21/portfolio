<script setup lang="ts">
import FaqPage from '~/components/site/FaqPage.vue'
import { useOfferingsPage } from '~/composables/useOfferingsPage'

definePageMeta({ layout: 'default' })
useOfferingsPage('faq')
</script>

<template>
  <FaqPage />
</template>
