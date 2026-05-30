<template>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <span class="logo-icon">📡</span>
          <span class="logo-text">API Pilot</span>
        </div>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item" :class="{ active: isActive('/') }">
          <span class="nav-icon">📊</span>
          <span class="nav-text">仪表盘</span>
        </router-link>
        <router-link to="/projects" class="nav-item" :class="{ active: isActive('/projects') }">
          <span class="nav-icon">📁</span>
          <span class="nav-text">项目管理</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info">
          <span class="user-avatar">{{ userStore.user?.username?.[0]?.toUpperCase() || 'U' }}</span>
          <span class="user-name">{{ userStore.user?.username }}</span>
        </div>
        <button class="logout-btn" @click="handleLogout">
          <span>退出</span>
        </button>
      </div>
    </aside>
    <main class="main-content">
      <header class="topbar">
        <div class="topbar-left">
          <h1 class="page-title">{{ pageTitle }}</h1>
        </div>
        <div class="topbar-right">
          <div class="env-selector" v-if="projectStore.currentProject">
            <select v-model="selectedEnvId" @change="handleEnvChange" class="env-select">
              <option :value="null">选择环境</option>
              <option v-for="env in projectStore.environments" :key="env.id" :value="env.id">
                {{ env.name }}
              </option>
            </select>
          </div>
        </div>
      </header>
      <div class="content-area">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useProjectStore } from '@/stores/projectStore'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const projectStore = useProjectStore()

const userStore = authStore

const selectedEnvId = ref<number | null>(null)

const pageTitle = computed(() => {
  if (route.path === '/') return '仪表盘'
  if (route.path === '/projects') return '项目管理'
  if (route.path.includes('/apis')) return '接口管理'
  if (route.path.includes('/cases')) return '测试用例'
  if (route.path.includes('/scenes')) return '场景管理'
  if (route.path.includes('/reports')) return '测试报告'
  if (route.path.includes('/environments')) return '环境配置'
  if (route.path.includes('/mock')) return 'Mock服务'
  return 'API Pilot'
})

function isActive(path: string): boolean {
  return route.path === path
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}

async function handleEnvChange() {
  if (selectedEnvId.value) {
    const env = projectStore.environments.find(e => e.id === selectedEnvId.value)
    projectStore.selectEnvironment(env || null)
  } else {
    projectStore.selectEnvironment(null)
  }
}

watch(() => projectStore.currentProject, async (project) => {
  if (project) {
    await projectStore.fetchEnvironments(project.id)
  }
})
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.sidebar {
  width: 240px;
  background: var(--surface-card);
  border-right: 1px solid var(--border-default);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-header {
  padding: var(--space-4);
  border-bottom: 1px solid var(--border-default);
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.sidebar-nav {
  flex: 1;
  padding: var(--space-3);
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.2s ease;
  margin-bottom: var(--space-1);
}

.nav-item:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--surface-selected);
  color: var(--primary-500);
}

.nav-icon {
  font-size: 18px;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
}

.sidebar-footer {
  padding: var(--space-4);
  border-top: 1px solid var(--border-default);
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: var(--primary-500);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}

.user-name {
  font-size: 14px;
  color: var(--text-primary);
}

.logout-btn {
  width: 100%;
  padding: var(--space-2) var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: var(--error-bg);
  color: var(--error);
  border-color: var(--error);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.topbar {
  height: 56px;
  padding: 0 var(--space-6);
  background: var(--surface-card);
  border-bottom: 1px solid var(--border-default);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.topbar-left {
  display: flex;
  align-items: center;
}

.page-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.env-select {
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: white;
  font-size: 14px;
  cursor: pointer;
}

.content-area {
  flex: 1;
  padding: var(--space-6);
  overflow-y: auto;
  background: var(--surface-bg);
}
</style>