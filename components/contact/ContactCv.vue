<template>
  <span class="folder">
    <svg class="back" viewBox="0 0 32 32" aria-hidden="true">
      <path
        class="shell"
        d="M5.8 9.2L15.2 9.2L17.4 6.8L24.6 6.8Q26.2 6.8 26.2 8.3L26.2 23.6Q26.2 25.2 24.6 25.2L7.4 25.2Q5.8 25.2 5.8 23.6Z"
      />
    </svg>
    <svg class="cover" viewBox="0 0 32 32" aria-hidden="true">
      <path
        class="face"
        d="M5.8 9.2L15.2 9.2L17.4 6.8L24.6 6.8Q26.2 6.8 26.2 8.3L26.2 23.6Q26.2 25.2 24.6 25.2L7.4 25.2Q5.8 25.2 5.8 23.6Z"
      />
    </svg>
  </span>
</template>

<style scoped>
.folder {
  position: relative;
  display: block;
  width: 100%;
  height: 100%;
  overflow: visible;
}

.back,
.cover {
  display: block;
  width: 100%;
  height: 100%;
  overflow: visible;
  pointer-events: none;
}

.back {
  position: relative;
  z-index: 0;
}

.cover {
  position: absolute;
  inset: 0;
  z-index: 1;
  transform-origin: 50% 78.75%;
  transform: scaleY(1);
  transition: transform 260ms var(--ease-out, cubic-bezier(0.23, 1, 0.32, 1));
}

.shell,
.face {
  stroke: currentColor;
  stroke-width: 1.5;
  stroke-linejoin: round;
  stroke-linecap: round;
}

.shell {
  fill: none;
}

.face {
  fill: var(--ink);
  paint-order: fill stroke;
  d: path("M5.8 9.2L15.2 9.2L17.4 6.8L24.6 6.8Q26.2 6.8 26.2 8.3L26.2 23.6Q26.2 25.2 24.6 25.2L7.4 25.2Q5.8 25.2 5.8 23.6Z");
  transition: d 260ms var(--ease-out, cubic-bezier(0.23, 1, 0.32, 1));
}
</style>
