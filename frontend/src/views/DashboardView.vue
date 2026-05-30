<template>
  <div class="dashboard">
    <div class="stats-grid stagger-enter">
      <div class="stat-card">
        <div class="stat-icon">📁</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.projects }}</div>
          <div class="stat-label">项目数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🔗</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.apis }}</div>
          <div class="stat-label">接口数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🧪</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.cases }}</div>
          <div class="stat-label">用例数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.scenes }}</div>
          <div class="stat-label">场景数</div>
        </div>
      </div>
    </div>

    <div class="dashboard-content">
      <div class="recent-projects">
        <h2 class="section-title">最近项目</h2>
        <div class="project-list" v-if="projectStore.projects.length">
          <div 
            v-for="project in projectStore.projects.slice(0, 5)" 
            :key="project.id"
            class="project-item"
            @click="goToProject(project.id)"
          >
            <div class="project-info">
              <div class="project-name">{{ project.name }}</div>
              <div class="project-desc">{{ project.description || '暂无描述' }}</div>
            </div>
            <div class="project-arrow">→</div>
          </div>
        </div>
        <div class="empty-state" v-else>
          <p>暂无项目</p>
          <el-button type="primary" @click="router.push('/projects')">创建项目</el-button>
        </div>
      </div>

      <div class="quick-actions">
        <h2 class="section-title">快捷操作</h2>
        <div class="action-grid">
          <div class="action-card" @click="router.push('/projects')">
            <div class="action-icon">➕</div>
            <div class="action-text">新建项目</div>
          </div>
          <div class="action-card" @click="router.push('/projects')">
            <div class="action-icon">🔗</div>
            <div class="action-text">导入接口</div>
          </div>
          <div class="action-card" @click="router.push('/projects')">
            <div class="action-icon">📤</div>
            <div class="action-text">导出数据</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectStore } from '@/stores/projectStore'

const router = useRouter()
const projectStore = useProjectStore()

const stats = reactive({
  projects: 0,
  apis: 0,
  cases: 0,
  scenes: 0
})

onMounted(async () => {
  await projectStore.fetchProjects()
  stats.projects = projectStore.projects.length
})

function goToProject(id: number) {
  router.push(`/projects/${id}/apis`)
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}

.stat-card {
  background: var(--surface-card);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  display: flex;
  align-items: center;
  gap: var(--space-4);
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: all 0.2s ease;
}

.stat-card:hover {
  box-shadow: var(--shadow-card-hover);
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 32px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-label {
  font-size: 14px;
  color: var(--text-muted);
}

.dashboard-content {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: var(--space-6);
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-4);
}

.recent-projects {
  background: var(--surface-card);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
}

.project-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.project-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
}

.project-item:hover {
  background: var(--surface-hover);
}

.project-name {
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.project-desc {
  font-size: 12px;
  color: var(--text-muted);
}

.project-arrow {
  color: var(--text-muted);
}

.empty-state {
  text-align: center;
  padding: var(--space-8);
  color: var(--text-muted);
}

.quick-actions {
  background: var(--surface-card);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
}

.action-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.action-card {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-card:hover {
  background: var(--surface-hover);
}

.action-icon {
  font-size: 20px;
}

.action-text {
  font-size: 14px;
  color: var(--text-primary);
}
</style>