import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'
import { apiUrl } from './api.js'

document.documentElement.style.setProperty('--api-base', apiUrl(''))
document.documentElement.style.setProperty('--bg-image', `url(${apiUrl('/api/images/bg3.png')})`)

createApp(App).use(router).mount('#app')
