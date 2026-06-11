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
const mdContent = ref('')

function renderMarkdown(text) {
  if (!text) return ''
  // Handle code blocks first (fenced)
  let html = text.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
  // Headers
  html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>')
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>')
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>')
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>')
  // Bold
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  // List items
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>')
  // Wrap consecutive <li> in <ul>
  html = html.replace(/(<li>.*?<\/li>\n?)+/g, '<ul>$&</ul>')
  // Paragraphs (double newline)
  html = html.replace(/\n\n+/g, '</p><p>')
  html = '<p>' + html + '</p>'
  // Clean empty <p>
  html = html.replace(/<p>\s*<\/p>/g, '')
  // Single newline to br
  html = html.replace(/\n/g, '<br>')
  return html
}

const renderedContent = computed(() => {
  if (mdContent.value) return renderMarkdown(mdContent.value)
  if (item.value?.content) return renderMarkdown(item.value.content)
  return ''
})

onMounted(async () => {
  const res = await fetch(apiUrl(`/api/projects/${route.params.id}`))
  const data = await res.json()
  if (data.code === 200) {
    item.value = data.data
    if (data.data.file_path) {
      const mdRes = await fetch(apiUrl(`/api/projects/md/${data.data.file_path}`))
      const mdData = await mdRes.json()
      if (mdData.code === 200) mdContent.value = mdData.data
    }
  }
})
</script>
