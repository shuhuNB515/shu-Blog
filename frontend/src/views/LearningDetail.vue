<template>
  <div class="page-wrapper">
    <RainEffect />
    <div class="detail-page" v-if="item">
      <button class="back-btn" @click="$router.back()">← 返回</button>
      <h1>{{ item.title }}</h1>
      <p class="detail-desc">{{ item.description }}</p>
      <div class="detail-content" v-html="renderedContent"></div>
    </div>
    <div class="detail-page" v-else>
      <p>加载中...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import RainEffect from '../components/RainEffect.vue'
import { apiUrl } from '../api.js'

const route = useRoute()
const item = ref(null)

function renderMarkdown(text) {
  if (!text) return ''
  let html = text.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
  html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>')
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>')
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>')
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>')
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>')
  html = html.replace(/(<li>.*?<\/li>\n?)+/g, '<ul>$&</ul>')
  html = html.replace(/\n\n+/g, '</p><p>')
  html = '<p>' + html + '</p>'
  html = html.replace(/<p>\s*<\/p>/g, '')
  html = html.replace(/\n/g, '<br>')
  return html
}

const renderedContent = computed(() => {
  return renderMarkdown(item.value?.content)
})

onMounted(async () => {
  const res = await fetch(apiUrl(`/api/learning/${route.params.id}`))
  const data = await res.json()
  if (data.code === 200) item.value = data.data
})
</script>
