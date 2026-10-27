<script setup lang="ts">
import { siGithub } from 'simple-icons'
import ContactCv from '~/components/contact/ContactCv.vue'
import ContactMail from '~/components/contact/ContactMail.vue'
import ContactPhone from '~/components/contact/ContactPhone.vue'
import { desktopMotion, useScrollScene } from '~/composables/useScrollScene'
import { useLocale } from '~/composables/useLocale'

const { copy } = useLocale()
const root = ref<HTMLElement | null>(null)

const linkedinPath =
  'M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 114.126 0 2.063 2.063 0 01-2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z'

const links = computed(() => [
  {
    id: 'mail',
    href: `mailto:${copy.value.email}`,
    label: copy.value.emailLabel,
    external: false,
    icon: '',
  },
  {
    id: 'phone',
    href: copy.value.phoneHref,
    label: copy.value.phoneLabel,
    external: false,
    icon: '',
  },
  {
    id: 'linkedin',
    href: copy.value.linkedin,
    label: 'LinkedIn',
    external: true,
    icon: linkedinPath,
  },
  {
    id: 'github',
    href: copy.value.github,
    label: 'GitHub',
    external: true,
    icon: siGithub.path,
  },
  {
    id: 'cv',
    href: copy.value.cv,
    label: copy.value.cvLabel,
    external: false,
    icon: '',
  },
])

useScrollScene(root, ({ gsap, mm }) => {
  mm.add(desktopMotion, () => {
    const heading = root.value?.querySelector('.js-rise')
    if (!heading || !root.value) return

    gsap.from(heading, {
      y: 28,
      duration: 0.9,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: root.value,
        start: 'top 75%',
        once: true,
      },
    })
  })
})
</script>

<template>
  <section
    id="contact"
    ref="root"
    class="flex min-h-dvh flex-col justify-between bg-ink px-6 pb-10 pt-28 text-paper md:px-10 md:pt-36 lg:px-16"
  >
    <p class="text-xs uppercase tracking-[0.22em] text-night-soft">{{ copy.contactKicker }}</p>

    <div class="flex max-w-full flex-col gap-12">
      <h2 class="js-rise max-w-full font-serif text-[clamp(1.85rem,6.2vw,6.25rem)] leading-[0.92] tracking-tight">
        {{ copy.contactTitle }}
      </h2>
      <ul class="flex flex-wrap items-center gap-3 sm:gap-5 md:gap-8">
        <li v-for="link in links" :key="link.id">
          <a
            class="contact-link"
            :class="`is-${link.id}`"
            :href="link.href"
            :aria-label="link.label"
            :target="link.external ? '_blank' : undefined"
            :rel="link.external ? 'noopener noreferrer' : undefined"
          >
            <ContactMail v-if="link.id === 'mail'" />
            <ContactPhone v-else-if="link.id === 'phone'" />
            <ContactCv v-else-if="link.id === 'cv'" />
            <svg
              v-else
              class="contact-glyph contact-glyph-brand"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path fill="currentColor" fill-rule="evenodd" :d="link.icon" />
            </svg>
            <span class="tip" aria-hidden="true">{{ link.label }}</span>
          </a>
        </li>
      </ul>
    </div>

    <p class="text-sm text-night-soft">{{ copy.name }} · {{ copy.address }}</p>
  </section>
</template>

<style scoped>
.contact-link {
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
  position: relative;
  display: grid;
  width: 2.5rem;
  height: 2.5rem;
  place-items: center;
  color: #c9c2b6;
  text-decoration: none;
  -webkit-tap-highlight-color: transparent;
  transition: color 180ms ease;
}

@media (min-width: 640px) {
  .contact-link {
    width: 2.75rem;
    height: 2.75rem;
  }
}

@media (min-width: 768px) {
  .contact-link {
    width: 3.5rem;
    height: 3.5rem;
  }
}

.contact-link.is-mail:is(:hover, :focus-visible) {
  color: #ffb088;
}

.contact-link.is-phone:is(:hover, :focus-visible),
.contact-link.is-github:is(:hover, :focus-visible) {
  color: #f3efe4;
}

.contact-link.is-linkedin:is(:hover, :focus-visible) {
  color: #0a66c2;
}

.contact-link.is-cv:is(:hover, :focus-visible) {
  color: #d6f26a;
}

.contact-glyph-brand {
  display: block;
  width: 56%;
  height: 56%;
}

@media (prefers-reduced-motion: no-preference) {
  @media (hover: hover) and (pointer: fine) {
    .contact-link:hover :deep(.flap),
    .contact-link:focus-visible :deep(.flap) {
      transform: rotateX(180deg);
    }

    .contact-link:hover :deep(.handset),
    .contact-link:focus-visible :deep(.handset) {
      transform: translateY(-2px) rotate(-8deg);
    }

    .contact-link:hover :deep(.cover),
    .contact-link:focus-visible :deep(.cover) {
      transform: scaleY(0.75);
    }

    .contact-link:hover :deep(.face),
    .contact-link:focus-visible :deep(.face) {
      d: path("M3.6 9.2L15 9.2L17.7 6.8L26.5 6.8Q28.4 6.8 28.4 8.3L26.2 23.6Q26.2 25.2 24.6 25.2L7.4 25.2Q5.8 25.2 5.8 23.6Z");
    }
  }

  .contact-link:focus-visible :deep(.flap) {
    transform: rotateX(180deg);
  }

  .contact-link:focus-visible :deep(.handset) {
    transform: translateY(-2px) rotate(-8deg);
  }

  .contact-link:focus-visible :deep(.cover) {
    transform: scaleY(0.75);
  }

  .contact-link:focus-visible :deep(.face) {
    d: path("M3.6 9.2L15 9.2L17.7 6.8L26.5 6.8Q28.4 6.8 28.4 8.3L26.2 23.6Q26.2 25.2 24.6 25.2L7.4 25.2Q5.8 25.2 5.8 23.6Z");
  }
}

</style>
