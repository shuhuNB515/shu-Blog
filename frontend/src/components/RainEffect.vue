<template>
  <div class="rain-container">
    <canvas ref="canvas" class="rain-canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
let drops = []
let animId = null

onMounted(() => {
  const cvs = canvas.value
  const ctx = cvs.getContext('2d')

  function resize() {
    cvs.width = window.innerWidth
    cvs.height = window.innerHeight
  }
  resize()
  window.addEventListener('resize', resize)

  // Create raindrops
  for (let i = 0; i < 60; i++) {
    drops.push({
      x: Math.random() * cvs.width * 1.5 - cvs.width * 0.5,
      y: Math.random() * -cvs.height,
      len: 8 + Math.random() * 20,
      speed: 6 + Math.random() * 14,
      opacity: 0.2 + Math.random() * 0.5,
      thickness: 0.5 + Math.random() * 1.5,
    })
  }

  function draw() {
    ctx.clearRect(0, 0, cvs.width, cvs.height)
    for (const d of drops) {
      ctx.beginPath()
      ctx.moveTo(d.x, d.y)
      // diagonal from top-left to bottom-right
      ctx.lineTo(d.x - d.len * 0.7, d.y - d.len)
      ctx.strokeStyle = `rgba(180, 210, 255, ${d.opacity})`
      ctx.lineWidth = d.thickness
      ctx.stroke()

      d.x += d.speed * 0.7
      d.y += d.speed
      if (d.y > cvs.height + 40 || d.x > cvs.width + 100) {
        d.x = -40
        d.y = Math.random() * -cvs.height * 0.5
      }
    }
    animId = requestAnimationFrame(draw)
  }
  draw()

  onUnmounted(() => {
    cancelAnimationFrame(animId)
    window.removeEventListener('resize', resize)
  })
})
</script>

<style scoped>
.rain-container {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 10;
  overflow: hidden;
}

.rain-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}
</style>
