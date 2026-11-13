<script setup lang="ts">
import ServicesPage from '~/components/site/ServicesPage.vue'
import { useOfferingsPage } from '~/composables/useOfferingsPage'

definePageMeta({ layout: 'default' })
useOfferingsPage('services')
</script>

<template>
  <ServicesPage />
</template>
