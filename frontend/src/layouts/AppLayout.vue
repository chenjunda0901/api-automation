<template>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon">
            <AppIcon name="zap" :size="24" />
          </div>
          <span class="logo-text">API Pilot</span>
        </div>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item" :class="{ active: isActive('/') }">
          <AppIcon name="dashboard" :size="20" class="nav-icon" />
          <span class="nav-text">仪表盘</span>
        </router-link>
        <router-link to="/projects" class="nav-item" :class="{ active: isActive('/projects') }">
          <AppIcon name="folder" :size="20" class="nav-icon" />
          <span class="nav-text">项目管理</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="footer-actions">
          <ThemeSwitcher />
        </div>
        <div class="user-info">
          <span class="user-avatar">{{ userStore.user?.username?.[0]?.toUpperCase() || 'U' }}</span>
          <span class="user-name">{{ userStore.user?.username }}</span>
        </div>
        <button class="logout-btn" @click="handleLogout">
          <AppIcon name="arrowLeft" :size="16" />
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
  padding: var(--space-6);
  border-bottom: 1px solid var(--color-border);
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: var(--gradient-hero);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-accent);
  box-shadow: var(--shadow-glow);
}

.logo-text {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: var(--font-bold);
  color: var(--color-text);
}

/* 导航区域 */
.sidebar-nav {
  flex: 1;
  padding: var(--space-4);
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg);
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all var(--duration-normal) var(--ease-out);
  margin-bottom: var(--space-1);
  font-weight: var(--font-medium);
}

.nav-item:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
}

.nav-item.active {
  background: var(--color-surface-active);
  color: var(--color-primary);
}

.nav-item.active .nav-icon {
  color: var(--color-primary);
}

.nav-icon {
  color: var(--color-text-muted);
  transition: color var(--duration-fast) var(--ease-out);
}

.nav-text {
  font-size: var(--text-sm);
}

/* 底部区域 */
.sidebar-footer {
  padding: var(--space-4);
  border-top: 1px solid var(--color-border);
}

.footer-actions {
  margin-bottom: var(--space-4);
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-3);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-accent) 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-semibold);
  font-size: var(--text-sm);
  box-shadow: var(--shadow-sm);
}

.user-name {
  font-size: var(--text-sm);
  color: var(--color-text);
  font-weight: var(--font-medium);
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  transition: all var(--duration-normal) var(--ease-out);
}

.logout-btn:hover {
  background: var(--color-error-light);
  color: var(--color-error);
  border-color: var(--color-error);
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
  padding: 0 var(--space-8);
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
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.env-select {
  padding: var(--space-2) var(--space-4);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.env-select:hover {
  border-color: var(--color-border-hover);
}

.env-select:focus {
  border-color: var(--color-primary);
  outline: none;
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

.content-area {
  flex: 1;
  padding: var(--space-8);
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
  .user-name {
    display: none;
  }
  
  .nav-item {
    justify-content: center;
    padding: var(--space-3);
  }
}
</style>