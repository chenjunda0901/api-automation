<template>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
            </svg>
          </div>
          <span class="logo-text">API Pilot</span>
        </div>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item" :class="{ active: isActive('/') }">
          <div class="nav-icon-wrapper">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7"></rect>
              <rect x="14" y="3" width="7" height="7"></rect>
              <rect x="14" y="14" width="7" height="7"></rect>
              <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
          </div>
          <span class="nav-text">仪表盘</span>
          <div class="nav-indicator"></div>
        </router-link>
        <router-link to="/projects" class="nav-item" :class="{ active: isActive('/projects') }">
          <div class="nav-icon-wrapper">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
            </svg>
          </div>
          <span class="nav-text">项目管理</span>
          <div class="nav-indicator"></div>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="footer-actions">
          <ThemeSwitcher />
        </div>
        <div class="divider"></div>
        <div class="user-info">
          <div class="user-avatar">{{ userStore.user?.username?.[0]?.toUpperCase() || 'U' }}</div>
          <div class="user-details">
            <span class="user-name">{{ userStore.user?.username }}</span>
            <span class="user-role">开发者</span>
          </div>
        </div>
        <button class="logout-btn" @click="handleLogout">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
          <span>退出登录</span>
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
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useProjectStore } from '@/stores/projectStore'
import ThemeSwitcher from '@/components/ThemeSwitcher.vue'

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
  background: var(--color-bg);
}

.sidebar {
  width: var(--sidebar-width);
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  position: relative;
}

/* 侧边栏顶部 */
.sidebar-header {
  padding: var(--space-5) var(--space-4);
  border-bottom: 1px solid var(--color-border-subtle);
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, var(--color-primary) 0%, #818CF8 100%);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.logo-text {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--color-text);
  letter-spacing: -0.01em;
}

/* 导航区域 */
.sidebar-nav {
  flex: 1;
  padding: var(--space-3);
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2-5) var(--space-3);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all var(--duration-fast) var(--ease-out);
  margin-bottom: var(--space-1);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  position: relative;
  overflow: hidden;
}

.nav-item:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
}

.nav-item.active {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.nav-item.active .nav-icon-wrapper {
  color: var(--color-primary);
}

.nav-icon-wrapper {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  background: var(--color-surface-muted);
  color: var(--color-text-tertiary);
  flex-shrink: 0;
  transition: all var(--duration-fast) var(--ease-out);
}

.nav-item:hover .nav-icon-wrapper {
  background: var(--color-surface-hover);
  color: var(--color-text-secondary);
}

.nav-item.active .nav-icon-wrapper {
  background: var(--color-primary-light);
}

.nav-text {
  flex: 1;
  font-size: var(--text-sm);
}

.nav-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-primary);
  opacity: 0;
  transform: scale(0);
  transition: all var(--duration-fast) var(--ease-spring);
}

.nav-item.active .nav-indicator {
  opacity: 1;
  transform: scale(1);
}

/* 底部区域 */
.sidebar-footer {
  padding: var(--space-4);
  border-top: 1px solid var(--color-border-subtle);
  background: var(--color-surface-elevated);
}

.footer-actions {
  margin-bottom: var(--space-3);
}

.divider {
  height: 1px;
  background: var(--color-border-subtle);
  margin: var(--space-3) 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-3);
  padding: var(--space-2);
  border-radius: var(--radius-md);
  background: var(--color-surface-muted);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-primary) 0%, #818CF8 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-semibold);
  font-size: var(--text-sm);
  flex-shrink: 0;
}

.user-details {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.user-name {
  font-size: var(--text-sm);
  color: var(--color-text);
  font-weight: var(--font-medium);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  width: 100%;
  padding: var(--space-2-5) var(--space-3);
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-text-tertiary);
  cursor: pointer;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  transition: all var(--duration-fast) var(--ease-out);
  border: 1px solid transparent;
}

.logout-btn:hover {
  background: var(--color-error-subtle);
  color: var(--color-error);
  border-color: var(--color-error-light);
}

/* 主内容区 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--color-bg);
}

.topbar {
  height: var(--topbar-height);
  padding: 0 var(--space-6);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.topbar-left {
  display: flex;
  align-items: center;
}

.page-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--color-text);
  letter-spacing: -0.01em;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.env-select {
  padding: var(--space-2) var(--space-3);
  padding-right: var(--space-8);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2364748B' stroke-width='2' xmlns='http://www.w3.org/2000/svg'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right var(--space-3) center;
}

.env-select:hover {
  border-color: var(--color-border-hover);
  background-color: var(--color-surface-hover);
}

.env-select:focus {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-focus);
  outline: none;
}

.content-area {
  flex: 1;
  padding: var(--space-6);
  overflow-y: auto;
  background: var(--color-bg);
}

/* 入场动画 */
.stagger-enter > * {
  opacity: 0;
  animation: fadeInUp var(--duration-slow) var(--ease-out) forwards;
}

.stagger-enter > *:nth-child(1) { animation-delay: 0ms; }
.stagger-enter > *:nth-child(2) { animation-delay: 50ms; }
.stagger-enter > *:nth-child(3) { animation-delay: 100ms; }
.stagger-enter > *:nth-child(4) { animation-delay: 150ms; }
.stagger-enter > *:nth-child(5) { animation-delay: 200ms; }
.stagger-enter > *:nth-child(6) { animation-delay: 250ms; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式 */
@media (max-width: 1024px) {
  .sidebar {
    width: var(--sidebar-collapsed);
  }
  
  .logo-text,
  .nav-text,
  .user-details,
  .logout-btn span {
    display: none;
  }
  
  .nav-item {
    justify-content: center;
    padding: var(--space-2-5);
  }
  
  .sidebar-footer {
    padding: var(--space-3);
  }
  
  .user-info {
    justify-content: center;
    padding: var(--space-2);
  }
}
</style>