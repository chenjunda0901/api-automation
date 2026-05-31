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
          <TrendChart :data="trendData" :height="320" />
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
              :size="160"
            />
          </div>
          <div class="health-trend" :class="healthScore.trend >= 0 ? 'up' : 'down'">
            <AppIcon :name="healthScore.trend >= 0 ? 'chevronUp' : 'chevronDown'" :size="16" />
            <span>较上周 {{ healthScore.trend >= 0 ? '+' : '' }}{{ healthScore.trend }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部区域 -->
    <div class="dashboard-bottom">
      <!-- 热门场景 -->
      <div class="bottom-card">
        <h3 class="card-title">热门场景</h3>
        <div class="scene-list">
          <div 
            v-for="scene in topScenes" 
            :key="scene.id"
            class="scene-item"
          >
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
        <h3 class="card-title">需要关注</h3>
        <div class="scene-list error">
          <div 
            v-for="scene in failedScenes" 
            :key="scene.id"
            class="scene-item"
          >
            <div class="scene-info">
              <span class="scene-name">{{ scene.name }}</span>
              <span class="scene-time">{{ scene.lastFail }}</span>
            </div>
            <div class="scene-fails">
              {{ scene.failCount }} 次失败
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷操作 -->
      <div class="bottom-card actions">
        <h3 class="card-title">快捷操作</h3>
        <div class="action-grid">
          <div class="action-item" @click="router.push('/projects')">
            <AppIcon name="plus" :size="20" />
            <span>新建项目</span>
          </div>
          <div class="action-item" @click="router.push('/projects')">
            <AppIcon name="upload" :size="20" />
            <span>导入接口</span>
          </div>
          <div class="action-item" @click="router.push('/projects')">
            <AppIcon name="download" :size="20" />
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
  margin-bottom: var(--space-6);
}

/* 主内容区域 */
.dashboard-main {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: var(--space-6);
  margin-bottom: var(--space-6);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.card-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--color-text);
  margin: 0;
}

/* 图表卡片 */
.chart-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
}

.period-selector {
  display: flex;
  gap: var(--space-1);
}

.period-btn {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.period-btn:hover {
  color: var(--color-text);
  background: var(--color-surface-hover);
}

.period-btn.active {
  color: var(--color-primary);
  background: var(--color-primary-light);
  font-weight: var(--font-medium);
}

/* 健康度卡片 */
.health-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  text-align: center;
}

.health-gauge-wrapper {
  margin: var(--space-6) 0;
}

.health-trend {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-1);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.health-trend.up {
  color: var(--color-success);
}

.health-trend.down {
  color: var(--color-error);
}

/* 底部区域 */
.dashboard-bottom {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-6);
}

.bottom-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
}

.bottom-card .card-title {
  font-size: var(--text-base);
  margin-bottom: var(--space-4);
}

/* 场景列表 */
.scene-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.scene-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-3);
  border-radius: var(--radius-md);
  transition: all var(--duration-fast) var(--ease-out);
}

.scene-item:hover {
  background: var(--color-surface-hover);
}

.scene-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.scene-name {
  font-size: var(--text-sm);
  color: var(--color-text);
  font-weight: var(--font-medium);
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
}

.scene-rate.excellent {
  color: var(--color-success);
  background: var(--color-success-light);
}

.scene-rate.good {
  color: var(--color-info);
  background: rgba(34, 211, 238, 0.1);
}

.scene-rate.warning {
  color: var(--color-warning);
  background: var(--color-warning-light);
}

.scene-rate.critical {
  color: var(--color-error);
  background: var(--color-error-light);
}

.scene-fails {
  font-size: var(--text-xs);
  color: var(--color-error);
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
  color: var(--color-primary);
}

.action-item span {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
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
    transform: translateY(16px);
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