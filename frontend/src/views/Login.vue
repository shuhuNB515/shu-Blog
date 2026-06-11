<template>
  <div class="login-page">
    <div class="login-card">
      <h1>登录</h1>
      <p class="login-desc">请登录以管理博客内容</p>
      <input v-model="username" type="text" placeholder="账号" class="login-input" @keyup.enter="doLogin" />
      <input v-model="password" type="password" placeholder="密码" class="login-input" @keyup.enter="doLogin" />
      <p v-if="error" class="login-error">{{ error }}</p>
      <button class="login-btn" @click="doLogin">登 录</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../stores/auth.js'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')

async function doLogin() {
  error.value = ''
  if (!username.value || !password.value) {
    error.value = '请输入账号和密码'
    return
  }
  const ok = await auth.login(username.value, password.value)
  if (ok) {
    router.push('/admin')
  } else {
    error.value = '账号或密码错误'
  }
}
</script>
