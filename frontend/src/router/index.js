import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Learning from '../views/Learning.vue'
import LearningDetail from '../views/LearningDetail.vue'
import Projects from '../views/Projects.vue'
import ProjectDetail from '../views/ProjectDetail.vue'
import EditLearning from '../views/EditLearning.vue'
import EditProjects from '../views/EditProjects.vue'
import Login from '../views/Login.vue'
import Admin from '../views/Admin.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/learning', component: Learning },
  { path: '/learning/:id', component: LearningDetail },
  { path: '/projects', component: Projects },
  { path: '/project/:id', component: ProjectDetail },
  { path: '/edit-learning', component: EditLearning },
  { path: '/edit-projects', component: EditProjects },
  { path: '/login', component: Login },
  { path: '/admin', component: Admin },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
