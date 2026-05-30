import { createRouter, createWebHashHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    path: '/',
    component: () => import('@/layouts/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/DashboardView.vue')
      },
      {
        path: 'projects',
        name: 'Projects',
        component: () => import('@/views/ProjectsView.vue')
      },
      {
        path: 'projects/:projectId',
        name: 'ProjectDetail',
        component: () => import('@/views/ProjectDetailView.vue'),
        children: [
          {
            path: 'apis',
            name: 'Apis',
            component: () => import('@/views/ApisView.vue')
          },
          {
            path: 'cases',
            name: 'Cases',
            component: () => import('@/views/CasesView.vue')
          },
          {
            path: 'scenes',
            name: 'Scenes',
            component: () => import('@/views/ScenesView.vue')
          },
          {
            path: 'reports',
            name: 'Reports',
            component: () => import('@/views/ReportsView.vue')
          },
          {
            path: 'environments',
            name: 'Environments',
            component: () => import('@/views/EnvironmentsView.vue')
          },
          {
            path: 'mock',
            name: 'Mock',
            component: () => import('@/views/MockView.vue')
          }
        ]
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router