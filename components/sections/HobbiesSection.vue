<script setup lang="ts">
import { desktopMotion, useScrollScene } from '~/composables/useScrollScene'
import { useLocale } from '~/composables/useLocale'
import type { Hobby } from '~/content/site'

const chaseQuery = '(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)'
const drift = [12, 6, -8, 10, -6, 8]

const { copy } = useLocale()
const root = ref<HTMLElement | null>(null)
const follow = ref<HTMLImageElement | null>(null)
const followSrc = ref('')
const chase = ref(false)

function place(event: PointerEvent) {
  const image = follow.value
  if (!image) return
  const width = 176
  const height = 128
  const x = event.clientX + (event.clientX + 22 + width > window.innerWidth ? -width - 16 : 22)
  const y = event.clientY + (event.clientY + 22 + height > window.innerHeight ? -height - 12 : 22)
  image.style.transform = `translate3d(${x}px, ${y}px, 0)`
}

function show(hobby: Hobby, event: PointerEvent) {
  if (!chase.value || !follow.value) return
  followSrc.value = hobby.image
  follow.value.style.opacity = '1'
  place(event)
}

function hide() {
  if (follow.value) follow.value.style.opacity = '0'
}

onMounted(() => {
  const media = window.matchMedia(chaseQuery)
  const apply = () => {
    chase.value = media.matches
    if (!media.matches) hide()
  }
  apply()
  media.addEventListener('change', apply)
  onUnmounted(() => media.removeEventListener('change', apply))
})

useScrollScene(root, ({ gsap, mm }) => {
  mm.add(desktopMotion, () => {
    const words = root.value?.querySelectorAll<HTMLElement>('.js-drift')
    if (!words?.length || !root.value) return

    words.forEach((word) => {
      const y = Number(word.dataset.drift ?? 0)
      gsap.to(word, {
        y,
        ease: 'none',
        scrollTrigger: {
          trigger: root.value,
          start: 'top bottom',
          end: 'bottom top',
          scrub: true,
        },
      })
    })
  })
})
</script>

<template>
  <section id="beyond" ref="root" class="bg-paper px-6 py-24 md:px-10 md:py-32 lg:px-16">
    <p class="text-xs uppercase tracking-[0.22em]">05</p>
    <h2 class="mt-3 max-w-4xl font-serif text-[clamp(3rem,6vw,5.5rem)] leading-[0.95] tracking-tight">
      {{ copy.beyondTitle }}
    </h2>

    <div class="hobby-field mt-10 md:mt-14">
      <div
        v-for="(hobby, index) in copy.hobbies"
        :key="hobby.id"
        class="hobby js-drift"
        :class="`hobby-${index}`"
        :data-drift="drift[index]"
      >
        <span
          class="hobby-label"
          @pointerenter="show(hobby, $event)"
          @pointermove="place"
          @pointerleave="hide"
        >{{ hobby.label }}</span>
        <img v-if="!chase" class="hobby-still" :src="hobby.image" alt="">
      </div>
    </div>

    <img
      v-show="chase"
      ref="follow"
      class="hobby-follow"
      :src="followSrc || undefined"
      alt=""
    >
  </section>
</template>

<style scoped>
.hobby-field {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.hobby {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem 1rem;
  width: max-content;
  max-width: 100%;
  pointer-events: none;
  font-family: 'Source Serif 4', Georgia, serif;
  line-height: 0.9;
  letter-spacing: -0.03em;
}

.hobby-label {
  pointer-events: auto;
}

.hobby-still {
  width: 8.5rem;
  height: 6rem;
  object-fit: cover;
  pointer-events: none;
}

.hobby-follow {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 40;
  width: 11rem;
  height: 8rem;
  object-fit: cover;
  opacity: 0;
  pointer-events: none;
  border: 1px solid #14120e;
}

.hobby-0 { font-size: clamp(1.85rem, 7.2vw, 2.25rem); }
.hobby-1 { font-size: clamp(1.4rem, 5.4vw, 1.7rem); font-style: italic; }
.hobby-2 { font-size: clamp(1.55rem, 6vw, 1.9rem); font-style: italic; }
.hobby-3 { font-size: clamp(1.75rem, 6.6vw, 2.1rem); }
.hobby-4 { font-size: clamp(1.65rem, 6.2vw, 2rem); }
.hobby-5 { font-size: clamp(1.45rem, 5.6vw, 1.75rem); font-style: italic; }

@media (min-width: 768px) {
  .hobby-field {
    position: relative;
    width: min(86%, 68rem);
    min-height: 34rem;
    margin-inline: auto;
  }

  .hobby {
    position: absolute;
  }

  .hobby-0 { left: 18%; top: 6%; font-size: clamp(2.15rem, 3vw, 2.75rem); }
  .hobby-1 { left: 68%; top: 14%; font-size: clamp(1.55rem, 2vw, 1.9rem); }
  .hobby-2 { left: 3%; top: 34%; font-size: clamp(1.75rem, 2.35vw, 2.15rem); }
  .hobby-3 { left: 34%; top: 48%; font-size: clamp(2rem, 2.7vw, 2.5rem); }
  .hobby-4 { left: 66%; top: 58%; font-size: clamp(1.9rem, 2.5vw, 2.35rem); }
  .hobby-5 { left: 12%; top: 76%; font-size: clamp(1.6rem, 2.1vw, 2rem); }
}

@media (min-width: 1200px) {
  section {
    display: flex;
    flex-direction: column;
    min-height: 100dvh;
    padding-top: 4.5rem;
    padding-bottom: 3.25rem;
  }

  .hobby-field {
    flex: 1;
    width: min(82%, 72rem);
    min-height: 0;
    margin-top: 0.25rem;
  }

  .hobby-0 { left: 16%; top: 14%; }
  .hobby-1 { left: 68%; top: 9%; }
  .hobby-2 { left: 27%; top: 48%; }
  .hobby-3 { left: 46%; top: 27%; }
  .hobby-4 { left: 5%; top: 71%; }
  .hobby-5 { left: 57%; top: 79%; }
}
</style>
