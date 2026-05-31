<template>
  <div class="reports-view">
    <div class="view-header">
      <h2 class="view-title">测试报告</h2>
    </div>

    <div class="report-list" v-if="reports.length">
      <div v-for="report in reports" :key="report.id" class="report-item">
        <div class="report-status" :class="`status-${report.status}`">
          {{ report.status === 'passed' ? '✓' : report.status === 'failed' ? '✗' : '⟳' }}
        </div>
        <div class="report-info">
          <div class="report-id">#{{ report.id }}</div>
          <div class="report-time">{{ formatDate(report.started_at) }}</div>
        </div>
        <div class="report-stats">
          <span class="stat-item stat-passed">{{ report.passed_steps }} 通过</span>
          <span class="stat-item stat-failed" v-if="report.failed_steps">{{ report.failed_steps }} 失败</span>
        </div>
        <div class="report-duration">
          {{ report.duration_ms ? `${(report.duration_ms / 1000).toFixed(2)}s` : '-' }}
        </div>
      </div>
    </div>

    <div class="empty-state" v-else>
      <div class="empty-icon">📊</div>
      <p class="empty-text">暂无测试报告</p>
      <p class="empty-hint">请先运行测试场景</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { reportApi, type TestReport } from '@/api/report'

const route = useRoute()
const reports = ref<TestReport[]>([])

const projectId = computed(() => Number(route.params.projectId))

onMounted(async () => {
  await fetchReports()
})

async function fetchReports() {
  try {
    reports.value = await reportApi.listAll(projectId.value) as unknown as TestReport[]
  } catch {
    ElMessage.error('获取报告列表失败')
  }
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}
</script>

<style scoped>
.reports-view {
  max-width: 1000px;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.view-title {
  font-size: 16px;
  font-weight: 600;
}

.report-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.report-item {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.report-status {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.status-passed {
  background: var(--success-bg);
  color: var(--success);
}

.status-failed {
  background: var(--error-bg);
  color: var(--error);
}

.status-running {
  background: var(--info-bg);
  color: var(--info);
}

.report-info {
  flex: 1;
}

.report-id {
  font-weight: 500;
  color: var(--color-text);
}

.report-time {
  font-size: 12px;
  color: var(--color-text-muted);
}

.report-stats {
  display: flex;
  gap: var(--space-3);
}

.stat-item {
  font-size: 12px;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
}

.stat-passed {
  background: var(--success-bg);
  color: var(--success);
}

.stat-failed {
  background: var(--error-bg);
  color: var(--error);
}

.report-duration {
  font-size: 14px;
  color: var(--color-text-muted);
  min-width: 80px;
  text-align: right;
}

.empty-state {
  text-align: center;
  padding: var(--space-12);
  background: var(--color-surface);
  border-radius: var(--radius-lg);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: var(--space-4);
}

.empty-text {
  color: var(--color-text);
  font-size: 16px;
  margin-bottom: var(--space-2);
}

.empty-hint {
  color: var(--color-text-muted);
  font-size: 14px;
}
</style>