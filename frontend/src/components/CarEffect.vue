<template>
  <div class="car-line-container">
    <div class="car-line"></div>
    <canvas ref="smokeCanvas" class="smoke-canvas"></canvas>
    <img
      ref="car"
      :src="carUrl"
      class="car"
      :style="carStyle"
      @load="onLoad"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { apiUrl } from '../api.js'

const carUrl = apiUrl('/api/images/car2.png')
const car = ref(null)
const smokeCanvas = ref(null)
const carStyle = ref({})
const carWidth = ref(150)
let movingRight = true
let pos = 0
let animId = null
const speed = 1.2
let smokeParticles = []

function onLoad() {
  if (car.value) {
    const w = car.value.naturalWidth
    const h = car.value.naturalHeight
    carWidth.value = Math.round((w / h) * 100)
  }
}

function animate() {
  const screenW = window.innerWidth
  if (movingRight) {
    pos += speed
    if (pos > screenW + 20) movingRight = false
  } else {
    pos -= speed
    if (pos < -carWidth.value - 20) movingRight = true
  }
  carStyle.value = {
    transform: `translateX(${pos}px) scaleX(${movingRight ? -1 : 1})`,
    width: carWidth.value + 'px',
  }

  // Smoke particles (trailing behind the car)
  const ctx = smokeCanvas.value?.getContext('2d')
  if (ctx && smokeCanvas.value) {
    const canvas = smokeCanvas.value
    if (canvas.width !== window.innerWidth || canvas.height !== window.innerHeight) {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    const carCenterX = pos + carWidth.value / 2
    // Smoke emits from back of car (opposite to movement direction)
    const smokeX = movingRight ? carCenterX - carWidth.value * 0.3 : carCenterX + carWidth.value * 0.3
    const smokeY = 225

    // Add new smoke particles
    if (Math.random() < 0.4) {
      smokeParticles.push({
        x: smokeX + (Math.random() - 0.5) * 10,
        y: smokeY,
        r: 2 + Math.random() * 6,
        opacity: 0.3 + Math.random() * 0.3,
        vx: (movingRight ? -0.3 : 0.3) + (Math.random() - 0.5) * 0.5,
        vy: -(0.3 + Math.random() * 0.8),
      })
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height)
    for (let i = smokeParticles.length - 1; i >= 0; i--) {
      const p = smokeParticles[i]
      p.x += p.vx
      p.y += p.vy
      p.r += 0.05
      p.opacity -= 0.004
      if (p.opacity <= 0 || p.r > 25) {
        smokeParticles.splice(i, 1)
      } else {
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(180, 180, 190, ${p.opacity})`
        ctx.fill()
      }
    }
  }

  animId = requestAnimationFrame(animate)
}

onMounted(() => {
  pos = -carWidth.value
  animate()
})

onUnmounted(() => {
  cancelAnimationFrame(animId)
})
</script>

<style scoped>
.car-line-container {
  position: fixed;
  bottom: -10px;
  left: 0;
  width: 100%;
  height: 60px;
  z-index: 10;
  pointer-events: none;
}

.car-line {
  position: absolute;
  bottom: 24px;
  left: 0;
  width: 100%;
  height: 2px;
  background: rgba(255, 255, 255, 0.4);
}

.smoke-canvas {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.car {
  position: absolute;
  bottom: 0px;
  left: 0;
  height: 100px;
  width: auto;
}
</style>
