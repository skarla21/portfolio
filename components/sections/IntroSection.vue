<script setup lang="ts">
import { desktopMotion, useScrollScene } from "~/composables/useScrollScene";
import { useLocale } from "~/composables/useLocale";

const { copy } = useLocale();
const root = ref<HTMLElement | null>(null);

const firstLine = computed(() => copy.value.profile[0] ?? "");
const restLines = computed(() => copy.value.profile.slice(1));

useScrollScene(root, ({ gsap, mm }) => {
  mm.add(desktopMotion, () => {
    const sentences = root.value?.querySelectorAll(".js-rise");
    if (!sentences?.length || !root.value) return;

    gsap.from(sentences, {
      y: 28,
      duration: 0.9,
      ease: "power3.out",
      stagger: 0.07,
      scrollTrigger: {
        trigger: root.value,
        start: "top 75%",
        once: true,
      },
    });
  });
});
</script>

<template>
  <section
    id="intro"
    ref="root"
    class="relative border-b border-ink/15 bg-paper px-6 pb-24 pt-[calc(var(--nav-h)+1.75rem)] md:px-10 md:pb-32 md:pt-[calc(var(--nav-h)+2.5rem)] lg:px-16"
  >
    <div
      class="pointer-events-none absolute inset-x-6 bottom-8 hidden items-baseline justify-between gap-6 text-xs uppercase tracking-[0.22em] lg:inset-x-16 lg:flex"
      aria-hidden="true"
    >
      <p>{{ copy.eyebrow }}</p>
      <p>{{ copy.place }}</p>
    </div>

    <header class="mb-10 max-w-3xl md:mx-auto md:mb-16">
      <h1
        class="js-rise intro-name font-display leading-[0.92] tracking-[-0.035em]"
      >
        {{ copy.name }}
      </h1>
      <p class="js-rise lede mt-4 font-display tracking-wide text-mute md:mt-5">
        {{ copy.lede }}
      </p>
      <p class="js-rise mt-3 text-sm uppercase tracking-[0.18em]">
        {{ copy.disciplines }}
      </p>
    </header>

    <div class="mx-auto max-w-3xl">
      <!-- Phone: 01 + label left, pfp right. md+: marker above copy; pfp beside first line. -->
      <div
        class="mb-8 flex items-center justify-between gap-8 md:mb-10 md:block"
      >
        <div>
          <p class="text-xs uppercase tracking-[0.22em]">01</p>
          <h2
            class="mt-3 font-serif text-[clamp(1.5rem,3vw,2.5rem)] leading-[0.95] tracking-tight"
          >
            {{ copy.introLabel }}
          </h2>
        </div>
        <div
          class="intro-pfp relative aspect-square shrink-0 overflow-hidden rounded-full ring-1 ring-ink/15 md:hidden"
        >
          <!-- 860px window at (634, 126) on the 1818×1228 photo. -->
          <img
            src="/imgs/pfp.jpg"
            :alt="copy.name"
            width="1818"
            height="1228"
            class="absolute left-[-73.721%] top-[-14.651%] h-auto w-[211.395%] max-w-none"
          />
        </div>
      </div>

      <div class="flex flex-col gap-8">
        <div
          class="intro-copy flex flex-col font-display leading-[1.45] md:flex-row md:items-start md:gap-5"
        >
          <div
            class="intro-pfp relative hidden aspect-square shrink-0 overflow-hidden rounded-full ring-1 ring-ink/15 md:block"
            aria-hidden="true"
          >
            <img
              src="/imgs/pfp.jpg"
              alt=""
              width="1818"
              height="1228"
              class="absolute left-[-73.721%] top-[-14.651%] h-auto w-[211.395%] max-w-none"
            />
          </div>
          <p class="js-rise w-full min-w-0 md:flex-1">
            {{ firstLine }}
          </p>
        </div>
        <p
          v-for="(line, index) in restLines"
          :key="index"
          class="js-rise intro-copy font-display leading-[1.45]"
        >
          {{ line }}
        </p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.intro-name {
  font-size: clamp(2.1rem, 6.5vw, 4.25rem);
}

.lede {
  font-size: clamp(1.05rem, 1.6vw, 1.35rem);
  line-height: 1.4;
}

.intro-copy {
  font-size: clamp(1.05rem, 1.55vw, 1.35rem);
}

.intro-pfp {
  width: 6.25rem;
  height: 6.25rem;
}

@media (min-width: 768px) {
  .intro-pfp {
    width: auto;
    height: calc(3 * 1.45 * 1em);
  }
}

/* ~20% larger type + em-sized pfp on very large displays */
@media (min-width: 85.625rem) {
  .intro-name {
    font-size: calc(4.25rem + (100vw - 85.625rem) * 0.02);
  }

  .lede {
    font-size: 1.62rem;
  }

  .intro-copy {
    font-size: 1.62rem;
  }
}
</style>
