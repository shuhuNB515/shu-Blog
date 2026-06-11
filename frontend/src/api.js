// 开发环境走 Vite 代理 /api，生产环境走 PythonAnywhere HTTPS 地址
const API_BASE = import.meta.env.DEV
  ? ''
  : 'https://shuhunb515.pythonanywhere.com'

export function apiUrl(path) {
  return API_BASE + path
}
