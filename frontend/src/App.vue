<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="nav-brand">
          <img :src="apiUrl('/api/images/doro1.png')" class="nav-logo" alt="logo" />
          Shu Blog
        </router-link>
        <div class="nav-links">
          <router-link to="/">首页</router-link>
          <router-link to="/learning">学习过程</router-link>
          <router-link to="/projects">我的项目</router-link>
          <a href="http://shuhu.me/shu-CTF-blog/#/" target="_blank">我的CTF博客</a>
          <template v-if="auth.loggedIn">
            <router-link to="/edit-learning">修改学习过程</router-link>
            <router-link to="/edit-projects">修改我的项目</router-link>
            <router-link to="/admin">管理中心</router-link>
          </template>
          <template v-else>
            <router-link to="/login">登录</router-link>
          </template>
        </div>
      </div>
    </nav>
    <main>
      <router-view />
    </main>
    <CarEffect />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { auth } from './stores/auth.js'
import { apiUrl } from './api.js'
import CarEffect from './components/CarEffect.vue'

onMounted(() => {
  auth.check()
})
</script>
