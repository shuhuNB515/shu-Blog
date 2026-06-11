<template>
  <div class="page-wrapper">
    <RainEffect />
    <div class="page">
      <h1>我的项目</h1>
      <p class="page-desc">这里展示我完成的各类项目。</p>
      <div class="card-grid">
        <div class="card card-large" v-for="(item, idx) in list" :key="item.id" @click="$router.push('/project/' + item.id)">
          <img v-if="idx < 8" :src="apiUrl('/api/images/' + (8 - idx) + '.gif')" class="card-img" />
          <h2>{{ item.title }}</h2>
          <p>{{ item.description }}</p>
          <button class="detail-btn" @click.stop="$router.push('/project/' + item.id)">查看详情 →</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import RainEffect from '../components/RainEffect.vue'
import { apiUrl } from '../api.js'

const list = ref([])

onMounted(async () => {
  const res = await fetch(apiUrl('/api/projects'), { credentials: 'include' })
  const data = await res.json()
  if (data.code === 200) list.value = data.data
})
</script>
