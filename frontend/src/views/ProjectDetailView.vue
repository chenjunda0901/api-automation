<template>
  <div class="project-detail">
    <div class="project-header">
      <button class="back-btn" @click="router.push('/projects')">← 返回</button>
      <div class="project-info">
        <h1 class="project-name">{{ projectStore.currentProject?.name || '加载中...' }}</h1>
        <p class="project-desc">{{ projectStore.currentProject?.description }}</p>
      </div>
    </div>

    <div class="project-tabs">
      <router-link 
        v-for="tab in tabs" 
        :key="tab.path"
        :to="tab.path"
        class="tab-item"
        :class="{ active: isActiveTab(tab.path) }"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-text">{{ tab.name }}</span>
      </router-link>
    </div>

    <div class="project-content">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProjectStore } from '@/stores/projectStore'

const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()

const tabs = [
  { name: '接口', path: '/apis', icon: '🔗' },
  { name: '用例', path: '/cases', icon: '🧪' },
  { name: '场景', path: '/scenes', icon: '🎬' },
  { name: '报告', path: '/reports', icon: '📊' },
  { name: '环境', path: '/environments', icon: '⚙️' },
  { name: 'Mock', path: '/mock', icon: '🎭' }
]

const projectId = computed(() => Number(route.params.projectId))

function isActiveTab(path: string): boolean {
  return route.path.includes(path)
}

onMounted(async () => {
  await projectStore.fetchProject(projectId.value)
})

watch(projectId, async (id) => {
  if (id) {
    await projectStore.fetchProject(id)
  }
})
</script>

<style scoped>
.project-detail {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.project-header {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.back-btn {
  padding: var(--space-2) var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: var(--surface-hover);
}

.project-info {
  flex: 1;
}

.project-name {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.project-desc {
  font-size: 14px;
  color: var(--text-muted);
}

.project-tabs {
  display: flex;
  gap: var(--space-1);
  background: var(--surface-card);
  padding: var(--space-1);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-6);
}

.tab-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  text-decoration: none;
  color: var(--text-secondary);
  font-size: 14px;
  transition: all 0.2s ease;
}

.tab-item:hover {
  color: var(--text-primary);
  background: var(--surface-hover);
}

.tab-item.active {
  color: var(--primary-500);
  background: var(--surface-selected);
}

.project-content {
  flex: 1;
  overflow: auto;
}
</style>