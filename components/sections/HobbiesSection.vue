<script setup lang="ts">
import { desktopMotion, useScrollScene } from '~/composables/useScrollScene'
import { useLocale } from '~/composables/useLocale'
import type { Hobby } from '~/content/site'

const chaseQuery = '(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)'
const drift = [28, -32, 18, -24, 30, -18]

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
    <p class="text-xs uppercase tracking-[0.22em]">04</p>
    <h2 class="mt-3 max-w-4xl font-serif text-[clamp(3rem,6vw,5.5rem)] leading-[0.95] tracking-tight">
      {{ copy.beyondTitle }}
    </h2>

    <div class="hobby-field mt-12 md:mt-16">
      <div
        v-for="(hobby, index) in copy.hobbies"
        :key="hobby.id"
        class="hobby js-drift"
        :class="`hobby-${index}`"
        :data-drift="drift[index]"
        @pointerenter="show(hobby, $event)"
        @pointermove="place"
        @pointerleave="hide"
      >
        <span>{{ hobby.label }}</span>
        <img v-if="!chase" class="hobby-still" :src="hobby.image" alt="" />
      </div>
    </div>

    <img
      v-show="chase"
      ref="follow"
      class="hobby-follow"
      :src="followSrc || undefined"
      alt=""
    />
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
  max-width: 100%;
  font-family: 'Source Serif 4', Georgia, serif;
  line-height: 0.9;
  letter-spacing: -0.03em;
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

.hobby-0 { font-size: clamp(2.6rem, 10vw, 4rem); }
.hobby-1 { font-size: clamp(2.3rem, 9vw, 3.4rem); font-style: italic; }
.hobby-2 { font-size: clamp(2.4rem, 9vw, 3.6rem); font-style: italic; }
.hobby-3 { font-size: clamp(2.5rem, 10vw, 3.8rem); }
.hobby-4 { font-size: clamp(2.5rem, 10vw, 3.8rem); }
.hobby-5 { font-size: clamp(2.15rem, 8vw, 3.1rem); font-style: italic; }

@media (min-width: 768px) {
  .hobby-field {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    column-gap: 1rem;
    row-gap: 0.5rem;
    min-height: 68vh;
    align-content: center;
  }

  .hobby-0 {
    grid-column: 1 / span 7;
    font-size: clamp(3.6rem, 5.4vw, 6.25rem);
  }

  .hobby-1 {
    grid-column: 8 / span 5;
    align-self: end;
    font-size: clamp(2.4rem, 3.2vw, 3.8rem);
  }

  .hobby-2 {
    grid-column: 1 / span 5;
    font-size: clamp(2.8rem, 4vw, 4.75rem);
  }

  .hobby-3 {
    grid-column: 6 / span 7;
    font-size: clamp(3rem, 4.4vw, 5.4rem);
  }

  .hobby-4 {
    grid-column: 1 / span 6;
    font-size: clamp(3rem, 4.2vw, 5.1rem);
  }

  .hobby-5 {
    grid-column: 7 / span 6;
    justify-self: end;
    font-size: clamp(2.3rem, 3.4vw, 4rem);
  }
}
</style>
