<script setup lang="ts">
import PortfolioHome from '~/components/site/PortfolioHome.vue'
import { useOfferingsPage } from '~/composables/useOfferingsPage'

definePageMeta({ layout: 'default' })
useOfferingsPage('home')
</script>

<template>
  <PortfolioHome />
</template>
