<template>
  <span class="mail">
    <svg class="mail-svg" viewBox="0 0 32 32" aria-hidden="true">
      <rect class="body" x="4.5" y="9" width="23" height="14.5" rx="1.6" />
    </svg>
    <svg class="flap" viewBox="0 0 32 32" aria-hidden="true">
      <path class="flap-shape" d="M4.5 9.2 16 17.6 27.5 9.2Z" />
    </svg>
  </span>
</template>

<style scoped>
.mail {
  position: relative;
  display: block;
  width: 100%;
  height: 100%;
  perspective: 8rem;
}

.mail-svg,
.flap {
  display: block;
  width: 100%;
  height: 100%;
  overflow: visible;
  pointer-events: none;
}

.mail-svg {
  position: relative;
  z-index: 1;
}

.flap {
  position: absolute;
  inset: 0;
  z-index: 2;
  transform-origin: 50% 28.75%;
  transform: rotateX(0deg);
  backface-visibility: visible;
  transition: transform 420ms var(--ease-out, cubic-bezier(0.23, 1, 0.32, 1));
}

.body,
.flap-shape {
  fill: var(--ink);
  stroke: currentColor;
  stroke-width: 1.5;
  stroke-linejoin: round;
  stroke-linecap: round;
}
</style>
