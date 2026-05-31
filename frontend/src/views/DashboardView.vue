<template>
  <div class="dashboard">
    <!-- 统计卡片区域 -->
    <div class="stats-grid stagger-enter">
      <StatCard 
        title="项目数"
        :value="stats.totalProjects"
        icon="folder"
        color="primary"
        :trend="12"
      />
      <StatCard 
        title="接口数"
        :value="stats.totalApis"
        icon="api"
        color="info"
        :trend="8"
      />
      <StatCard 
        title="场景数"
        :value="stats.totalScenes"
        icon="play"
        color="success"
        :trend="-3"
      />
      <StatCard 
        title="通过率"
        :value="stats.passRate"
        suffix="%"
        icon="checkCircle"
        color="warning"
        :trend="5"
      />
    </div>

    <!-- 核心内容区域 -->
    <div class="dashboard-main">
      <!-- 左侧：趋势图表 -->
      <div class="main-content">
        <div class="chart-card">
          <div class="card-header">
            <h2 class="card-title">测试趋势</h2>
            <div class="period-selector">
              <button 
                v-for="p in periods" 
                :key="p.value"
                class="period-btn"
                :class="{ active: selectedPeriod === p.value }"
                @click="selectedPeriod = p.value"
              >
                {{ p.label }}
              </button>
            </div>
          </div>
          <TrendChart :data="trendData" :height="280" />
        </div>
      </div>

      <!-- 右侧：健康度仪表 -->
      <div class="sidebar-content">
        <div class="health-card">
          <h3 class="card-title">健康度</h3>
          <div class="health-gauge-wrapper">
            <HealthGauge 
              :score="healthScore.score"
              :level="healthScore.level"
              :size="140"
            />
          </div>
          <div class="health-trend" :class="healthScore.trend >= 0 ? 'up' : 'down'">
            <svg v-if="healthScore.trend >= 0" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="18 15 12 9 6 15"></polyline>
            </svg>
            <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
            <span>较上周 {{ healthScore.trend >= 0 ? '+' : '' }}{{ healthScore.trend }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部区域 -->
    <div class="dashboard-bottom">
      <!-- 热门场景 -->
      <div class="bottom-card">
        <div class="card-header-simple">
          <h3 class="card-title">热门场景</h3>
          <span class="card-badge">TOP 5</span>
        </div>
        <div class="scene-list">
          <div 
            v-for="(scene, index) in topScenes" 
            :key="scene.id"
            class="scene-item"
          >
            <div class="scene-rank">{{ index + 1 }}</div>
            <div class="scene-info">
              <span class="scene-name">{{ scene.name }}</span>
              <span class="scene-runs">{{ scene.runs }} 次执行</span>
            </div>
            <div class="scene-rate" :class="getRateClass(scene.passRate)">
              {{ scene.passRate }}%
            </div>
          </div>
        </div>
      </div>

      <!-- 失败场景 -->
      <div class="bottom-card">
        <div class="card-header-simple">
          <h3 class="card-title">需要关注</h3>
          <span class="card-badge warning">需处理</span>
        </div>
        <div class="scene-list">
          <div 
            v-for="scene in failedScenes" 
            :key="scene.id"
            class="scene-item"
          >
            <div class="scene-icon error">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
            </div>
            <div class="scene-info">
              <span class="scene-name">{{ scene.name }}</span>
              <span class="scene-time">{{ scene.lastFail }}</span>
            </div>
            <div class="scene-fails">
              {{ scene.failCount }} 次
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷操作 -->
      <div class="bottom-card">
        <h3 class="card-title">快捷操作</h3>
        <div class="action-grid">
          <div class="action-item" @click="router.push('/projects')">
            <div class="action-icon primary">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
            </div>
            <span>新建项目</span>
          </div>
          <div class="action-item" @click="router.push('/projects')">
            <div class="action-icon success">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
            </div>
            <span>导入接口</span>
          </div>
          <div class="action-item" @click="router.push('/projects')">
            <div class="action-icon info">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
            </div>
            <span>导出报告</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectStore } from '@/stores/projectStore'
import { useDashboardStats } from '@/composables/useDashboardStats'
import StatCard from '@/components/charts/StatCard.vue'
import TrendChart from '@/components/charts/TrendChart.vue'
import HealthGauge from '@/components/charts/HealthGauge.vue'

const router = useRouter()
const projectStore = useProjectStore()

// 仪表盘统计
const {
  stats,
  trendData,
  healthScore,
  topScenes,
  failedScenes,
  fetchStats
} = useDashboardStats()

// 时间段选择
const periods = [
  { label: '7天', value: '7d' },
  { label: '30天', value: '30d' },
  { label: '90天', value: '90d' }
]
const selectedPeriod = ref('7d')

// 评分颜色
function getRateClass(rate: number): string {
  if (rate >= 95) return 'excellent'
  if (rate >= 85) return 'good'
  if (rate >= 70) return 'warning'
  return 'critical'
}

// 初始化
onMounted(async () => {
  await projectStore.fetchProjects()
  await fetchStats()
})
</script>

<style scoped>
.dashboard {
  max-width: var(--content-max-width);
  margin: 0 auto;
}

/* 统计卡片网格 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-5);
}

/* 主内容区域 */
.dashboard-main {
  display: grid;
  grid-template-columns: 1fr 260px;
  gap: var(--space-5);
  margin-bottom: var(--space-5);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.card-header-simple {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.card-title {
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--color-text);
  margin: 0;
}

.card-badge {
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.card-badge.warning {
  background: var(--color-warning-light);
  color: var(--color-warning);
}

/* 图表卡片 */
.chart-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
}

.period-selector {
  display: flex;
  gap: var(--space-1);
  background: var(--color-surface-muted);
  padding: var(--space-1);
  border-radius: var(--radius-md);
}

.period-btn {
  padding: var(--space-1-5) var(--space-3);
  font-size: var(--text-sm);
  color: var(--color-text-tertiary);
  background: transparent;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  font-weight: var(--font-medium);
}

.period-btn:hover {
  color: var(--color-text-secondary);
}

.period-btn.active {
  color: var(--color-text);
  background: var(--color-surface);
  box-shadow: var(--shadow-xs);
}

/* 健康度卡片 */
.health-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  text-align: center;
}

.health-card .card-title {
  font-size: var(--text-sm);
}

.health-gauge-wrapper {
  margin: var(--space-4) 0;
}

.health-trend {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  padding: var(--space-1) var(--space-2);
  background: var(--color-surface-muted);
  border-radius: var(--radius-full);
}

.health-trend.up {
  color: var(--color-success);
  background: var(--color-success-subtle);
}

.health-trend.down {
  color: var(--color-error);
  background: var(--color-error-subtle);
}

/* 底部区域 */
.dashboard-bottom {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-5);
}

.bottom-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
}

/* 场景列表 */
.scene-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.scene-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2-5) var(--space-3);
  border-radius: var(--radius-md);
  transition: all var(--duration-fast) var(--ease-out);
}

.scene-item:hover {
  background: var(--color-surface-hover);
}

.scene-rank {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  color: var(--color-text-muted);
  background: var(--color-surface-muted);
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}

.scene-icon {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.scene-icon.error {
  background: var(--color-error-subtle);
  color: var(--color-error);
}

.scene-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.scene-name {
  font-size: var(--text-sm);
  color: var(--color-text);
  font-weight: var(--font-medium);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.scene-runs,
.scene-time {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

.scene-rate {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}

.scene-rate.excellent {
  color: var(--color-success);
  background: var(--color-success-subtle);
}

.scene-rate.good {
  color: var(--color-info);
  background: var(--color-info-subtle);
}

.scene-rate.warning {
  color: var(--color-warning);
  background: var(--color-warning-subtle);
}

.scene-rate.critical {
  color: var(--color-error);
  background: var(--color-error-subtle);
}

.scene-fails {
  font-size: var(--text-xs);
  color: var(--color-error);
  font-weight: var(--font-medium);
  flex-shrink: 0;
}

/* 快捷操作 */
.action-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.action-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  color: var(--color-text-secondary);
}

.action-item:hover {
  background: var(--color-surface-hover);
}

.action-item:hover span {
  color: var(--color-text);
}

.action-item span {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  transition: color var(--duration-fast) var(--ease-out);
}

.action-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  flex-shrink: 0;
  transition: all var(--duration-fast) var(--ease-out);
}

.action-icon.primary {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.action-icon.success {
  background: var(--color-success-subtle);
  color: var(--color-success);
}

.action-icon.info {
  background: var(--color-info-subtle);
  color: var(--color-info);
}

.action-item:hover .action-icon.primary {
  background: var(--color-primary);
  color: white;
}

.action-item:hover .action-icon.success {
  background: var(--color-success);
  color: white;
}

.action-item:hover .action-icon.info {
  background: var(--color-info);
  color: white;
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

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式 */
@media (max-width: 1280px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .dashboard-main {
    grid-template-columns: 1fr;
  }
  
  .dashboard-bottom {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>