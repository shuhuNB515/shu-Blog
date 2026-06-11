<template>
  <div class="home">
    <div class="hero" :style="{ backgroundImage: `url(${bgUrl})` }">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <h1 class="hero-title">Shu Blog</h1>
        <p class="tagline">记录学习过程，分享项目经验</p>
        <router-link to="/learning" class="btn-start">开始阅读 →</router-link>
        <div class="features">
          <div class="feature-card">
            <h2>学习过程</h2>
            <p>记录 Web开发、Python、网络等方向的学习历程与笔记</p>
          </div>
          <div class="feature-card">
            <h2>CTF博客</h2>
            <p>记录CTF比赛中的解题思路与安全学习笔记</p>
          </div>
          <div class="feature-card">
            <h2>项目展示</h2>
            <p>展示我完成的各类项目，分享开发经验与心得</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const bgUrl = '/api/images/bg3.png'
</script>
