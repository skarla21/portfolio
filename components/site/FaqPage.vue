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
        {{ offerings.faqBackHome }}
      </NuxtLink>

      <h1
        class="mt-10 font-serif text-[clamp(2rem,5vw,3.5rem)] leading-[0.95] tracking-tight"
      >
        {{ offerings.faqTitle }}
      </h1>
      <p class="mt-5 text-lg leading-relaxed text-mute md:text-xl">
        {{ offerings.faqLede }}
      </p>

      <div class="mt-12 space-y-10">
        <section
          v-for="item in offerings.faqs"
          :id="item.id"
          :key="item.id"
          class="border-t border-ink/15 pt-8"
        >
          <h2 class="font-serif text-xl tracking-tight md:text-2xl">
            {{ item.question }}
          </h2>
          <p class="mt-3 text-lg leading-relaxed">
            {{ item.answer }}
          </p>
        </section>
      </div>

      <NuxtLink
        :to="{ path: localePath('/'), hash: '#contact' }"
        class="mt-16 inline-flex border border-ink bg-ink px-4 py-2 text-sm text-paper hover:bg-transparent hover:text-ink"
      >
        {{ offerings.faqContactCta }}
      </NuxtLink>
    </div>
  </main>
</template>
