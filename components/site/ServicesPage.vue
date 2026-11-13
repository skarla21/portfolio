<script setup lang="ts">
import { useLocale } from '~/composables/useLocale'
import { offeringsByLocale } from '~/content/offerings'

const { locale, localePath } = useLocale()
const offerings = computed(() => offeringsByLocale[locale.value])
</script>

<template>
  <main
    class="bg-paper px-6 pb-24 pt-[calc(var(--nav-h)+2rem)] md:px-10 md:pb-32 md:pt-[calc(var(--nav-h)+2.75rem)] lg:px-16"
  >
    <div class="mx-auto max-w-3xl">
      <NuxtLink
        :to="localePath('/')"
        class="text-sm underline underline-offset-4"
      >
        {{ offerings.servicesBackHome }}
      </NuxtLink>

      <p class="mt-10 text-xs uppercase tracking-[0.22em]">
        {{ offerings.servicesTagline }}
      </p>
      <h1
        class="mt-4 font-serif text-[clamp(2rem,5vw,3.5rem)] leading-[0.95] tracking-tight"
      >
        {{ offerings.servicesPageTitle }}
      </h1>
      <p class="mt-5 text-lg leading-relaxed text-mute md:text-xl">
        {{ offerings.servicesPageLede }}
      </p>

      <article
        v-for="item in offerings.offerings"
        :id="item.id"
        :key="item.id"
        class="mt-14 border-t border-ink/15 pt-10"
      >
        <h2 class="font-serif text-[clamp(1.5rem,3vw,2.25rem)] leading-[0.95] tracking-tight">
          {{ item.title }}
        </h2>
        <p class="mt-4 text-lg leading-relaxed">
          {{ item.body }}
        </p>
      </article>

      <div class="mt-16 flex flex-wrap gap-4">
        <NuxtLink
          :to="{ path: localePath('/'), hash: '#work' }"
          class="border border-ink px-4 py-2 text-sm hover:bg-ink hover:text-paper"
        >
          {{ offerings.servicesProofLabel }}
        </NuxtLink>
        <NuxtLink
          :to="{ path: localePath('/'), hash: '#contact' }"
          class="border border-ink bg-ink px-4 py-2 text-sm text-paper hover:bg-transparent hover:text-ink"
        >
          {{ offerings.servicesContactCta }}
        </NuxtLink>
      </div>
    </div>
  </main>
</template>
