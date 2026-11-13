import type { RouterConfig } from '@nuxt/schema'
import type { RouteLocationNormalized, RouterScrollBehavior } from 'vue-router'
import { START_LOCATION } from 'vue-router'
import { useNuxtApp } from '#app/nuxt'
import { useRouter } from '#app/composables/router'
import { desktopMotion } from '~/composables/useScrollScene'

type ScrollPos = Awaited<ReturnType<RouterScrollBehavior>>

/**
 * After a path change with a hash (e.g. /services → /#contact), wait until the
 * target exists — home sections mount after the route resolves.
 *
 * Also wait for the projects ScrollTrigger pin: scrolling before the pin-spacer
 * exists uses a pre-pin offset and lands mid-showcase once the pin mounts.
 */
export default {
  async scrollBehavior(to, from, savedPosition) {
    const nuxtApp = useNuxtApp()
    // Nuxt supports this option at runtime; vue-router's RouterOptions omits it.
    const behavior =
      (
        useRouter().options as { scrollBehaviorType?: ScrollBehavior }
      ).scrollBehaviorType ?? 'auto'

    const samePath =
      to.path.replace(/\/$/, '') === from.path.replace(/\/$/, '')

    if (samePath) {
      if (from.hash && !to.hash) return { left: 0, top: 0 }
      if (to.hash) return await waitForHash(to.hash, behavior)
      return false
    }

    const allowTop =
      typeof to.meta.scrollToTop === 'function'
        ? to.meta.scrollToTop(to, from)
        : to.meta.scrollToTop
    if (allowTop === false) return false

    if (from !== START_LOCATION) {
      await afterPageReady(nuxtApp)
      if (useRouter().currentRoute.value.fullPath !== to.fullPath) return false
    }

    return resolvePosition(to, from, savedPosition, behavior)
  },
} satisfies RouterConfig

function afterPageReady(nuxtApp: ReturnType<typeof useNuxtApp>) {
  return new Promise<void>((resolve) => {
    nuxtApp.hooks.hookOnce('page:loading:end', () => {
      const transitionPromise = (
        nuxtApp as typeof nuxtApp & {
          '~transitionPromise'?: Promise<void>
        }
      )['~transitionPromise']
      requestAnimationFrame(() => {
        if (transitionPromise) transitionPromise.then(() => resolve())
        else resolve()
      })
    })
  })
}

function raf() {
  return new Promise<void>((r) => requestAnimationFrame(() => r()))
}

function hashMargin(selector: string) {
  try {
    const elem = document.querySelector(selector)
    if (!elem) return 0
    return (
      (Number.parseFloat(getComputedStyle(elem).scrollMarginTop) || 0) +
      (Number.parseFloat(
        getComputedStyle(document.documentElement).scrollPaddingTop,
      ) || 0)
    )
  } catch {
    return 0
  }
}

/** ProjectsShowcase is the only pin; spacer appears after useScrollScene setup. */
async function waitForPinnedLayout() {
  if (!window.matchMedia(desktopMotion).matches) return

  for (let i = 0; i < 90; i++) {
    if (document.querySelector('.pin-spacer')) break
    await raf()
  }

  await document.fonts.ready
  try {
    const { gsap } = await import('gsap')
    const { ScrollTrigger } = await import('gsap/ScrollTrigger')
    gsap.registerPlugin(ScrollTrigger)
    ScrollTrigger.refresh()
  } catch {
    /* gsap unavailable — scroll with current layout */
  }
  await raf()
  await raf()
}

async function waitForHash(
  hash: string,
  behavior: ScrollBehavior,
): Promise<ScrollPos> {
  if (import.meta.server) return { el: hash, top: 0, behavior }

  for (let i = 0; i < 60; i++) {
    if (document.querySelector(hash)) {
      await waitForPinnedLayout()
      if (!document.querySelector(hash)) break
      return { el: hash, top: hashMargin(hash), behavior }
    }
    await raf()
  }
  return { left: 0, top: 0 }
}

async function resolvePosition(
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  savedPosition: Parameters<RouterScrollBehavior>[2],
  defaultBehavior: ScrollBehavior,
): Promise<ScrollPos> {
  if (savedPosition) return savedPosition
  if (to.hash) {
    const changing =
      to.path !== from.path || to.name !== from.name || to.hash !== from.hash
    return await waitForHash(
      to.hash,
      changing ? defaultBehavior : 'instant',
    )
  }
  return { left: 0, top: 0 }
}
