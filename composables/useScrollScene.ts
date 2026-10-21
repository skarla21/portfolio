import type { Ref } from 'vue'

type GsapApi = typeof import('gsap').gsap
type ScrollTriggerApi = typeof import('gsap/ScrollTrigger').ScrollTrigger
type MatchMediaApi = ReturnType<GsapApi['matchMedia']>

export const desktopMotion =
  '(min-width: 768px) and (prefers-reduced-motion: no-preference)'

export function useScrollScene(
  root: Ref<HTMLElement | null>,
  setup: (tools: {
    gsap: GsapApi
    ScrollTrigger: ScrollTriggerApi
    mm: MatchMediaApi
    root: HTMLElement
  }) => void,
) {
  let mm: MatchMediaApi | undefined

  onMounted(async () => {
    const el = root.value
    if (!el) return

    const { gsap } = await import('gsap')
    const { ScrollTrigger } = await import('gsap/ScrollTrigger')
    gsap.registerPlugin(ScrollTrigger)

    mm = gsap.matchMedia()
    setup({ gsap, ScrollTrigger, mm, root: el })

    await document.fonts.ready
    ScrollTrigger.refresh()
  })

  onUnmounted(() => {
    mm?.revert()
  })
}
