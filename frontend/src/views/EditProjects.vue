<template>
  <div class="page">
    <h1>修改我的项目</h1>
    <p class="page-desc">管理项目内容</p>

    <div class="edit-bar">
      <button class="btn-add" @click="showAdd = true">+ 添加</button>
    </div>

    <div v-if="showAdd" class="modal-overlay" @click.self="showAdd = false">
      <div class="modal">
        <h2>添加项目</h2>
        <input v-model="form.title" placeholder="标题" class="edit-input" />
        <textarea v-model="form.description" placeholder="简短描述" class="edit-textarea"></textarea>
        <textarea v-model="form.content" placeholder="详细内容" class="edit-textarea" style="min-height:160px"></textarea>
        <input v-model="form.url" placeholder="项目链接（可选）" class="edit-input" />
        <input v-model="form.file_path" placeholder="Markdown文件名（可选，如 os-kernel.md）" class="edit-input" />
        <div class="modal-btns">
          <button class="btn-save" @click="doAdd">保存</button>
          <button class="btn-cancel" @click="showAdd = false">取消</button>
        </div>
      </div>
    </div>

    <div v-if="showEdit" class="modal-overlay" @click.self="showEdit = false">
      <div class="modal">
        <h2>编辑项目</h2>
        <input v-model="form.title" placeholder="标题" class="edit-input" />
        <textarea v-model="form.description" placeholder="简短描述" class="edit-textarea"></textarea>
        <textarea v-model="form.content" placeholder="详细内容" class="edit-textarea" style="min-height:160px"></textarea>
        <input v-model="form.url" placeholder="项目链接（可选）" class="edit-input" />
        <input v-model="form.file_path" placeholder="Markdown文件名（可选，如 os-kernel.md）" class="edit-input" />
        <div class="modal-btns">
          <button class="btn-save" @click="doEdit">保存</button>
          <button class="btn-cancel" @click="showEdit = false">取消</button>
        </div>
      </div>
    </div>

    <div class="card-grid">
      <div class="card" v-for="item in list" :key="item.id">
        <h2>{{ item.title }}</h2>
        <p>{{ item.description }}</p>
        <div class="card-actions">
          <button class="btn-edit" @click="openEdit(item)">编辑</button>
          <button class="btn-del" @click="doDelete(item.id)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../stores/auth.js'
import { apiUrl } from '../api.js'

const router = useRouter()
const list = ref([])
const showAdd = ref(false)
const showEdit = ref(false)
const form = ref({ id: null, title: '', description: '', content: '', url: '', file_path: '' })

async function load() {
  const res = await fetch(apiUrl('/api/projects'), { credentials: 'include' })
  const data = await res.json()
  if (data.code === 200) list.value = data.data
}

onMounted(() => {
  if (!auth.loggedIn) { router.push('/login'); return }
  load()
})

async function doAdd() {
  await fetch(apiUrl('/api/projects'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value),
    credentials: 'include'
  })
  showAdd.value = false
  form.value = { id: null, title: '', description: '', content: '', url: '', file_path: '' }
  load()
}

function openEdit(item) {
  form.value = { id: item.id, title: item.title, description: item.description, content: item.content || '', url: item.url || '', file_path: item.file_path || '' }
  showEdit.value = true
}

async function doEdit() {
  await fetch(apiUrl(`/api/projects/${form.value.id}`), {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value),
    credentials: 'include'
  })
  showEdit.value = false
  form.value = { id: null, title: '', description: '', content: '', url: '', file_path: '' }
  load()
}

async function doDelete(id) {
  if (!confirm('确定删除？')) return
  await fetch(apiUrl(`/api/projects/${id}`), { method: 'DELETE', credentials: 'include' })
  load()
}
</script>
