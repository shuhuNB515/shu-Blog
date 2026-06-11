import { reactive } from 'vue'
import { apiUrl } from '../api.js'

export const auth = reactive({
  loggedIn: false,
  username: '',

  async check() {
    try {
      const res = await fetch(apiUrl('/api/check_login'), { credentials: 'include' })
      const data = await res.json()
      this.loggedIn = data.logged_in
      this.username = data.username || ''
    } catch {
      this.loggedIn = false
    }
  },

  async login(username, password) {
    const res = await fetch(apiUrl('/api/login'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
      credentials: 'include'
    })
    const data = await res.json()
    if (data.code === 200) {
      this.loggedIn = true
      this.username = username
      return true
    }
    return false
  },

  async logout() {
    await fetch(apiUrl('/api/logout'), { method: 'POST', credentials: 'include' })
    this.loggedIn = false
    this.username = ''
  }
})
