<template>
  <div class="page">
    <h1>管理中心</h1>
    <p class="page-desc">欢迎，{{ auth.username }}</p>

    <div class="admin-grid">
      <div class="admin-card">
        <div class="admin-icon">👁</div>
        <div class="admin-value">{{ stats.total }}</div>
        <div class="admin-label">总浏览量</div>
      </div>
      <div class="admin-card" v-for="item in stats.byPage" :key="item.page">
        <div class="admin-icon">📄</div>
        <div class="admin-value">{{ item.count }}</div>
        <div class="admin-label">{{ item.page }}</div>
      </div>
    </div>

    <div class="admin-actions">
      <router-link to="/edit-learning" class="admin-link">修改学习过程</router-link>
      <router-link to="/edit-projects" class="admin-link">修改我的项目</router-link>
      <button class="logout-btn" @click="doLogout">退出登录</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../stores/auth.js'
import { apiUrl } from '../api.js'

const router = useRouter()
const stats = ref({ total: 0, byPage: [] })

onMounted(async () => {
  if (!auth.loggedIn) {
    router.push('/login')
    return
  }
  try {
    const res = await fetch(apiUrl('/api/stats'), { credentials: 'include' })
    const data = await res.json()
    if (data.code === 200) stats.value = data.data
  } catch {}
})

async function doLogout() {
  await auth.logout()
  router.push('/')
}
</script>
