<script setup lang="ts">
/**
 * Stat Card Component
 * 统计卡片组件
 */
interface Props {
  title: string
  value: string | number
  icon?: string
  trend?: number
  suffix?: string
  color?: string
}

const props = withDefaults(defineProps<Props>(), {
  color: 'primary'
})

const colorMap = {
  primary: { bg: 'var(--color-primary-light)', color: 'var(--color-primary)' },
  success: { bg: 'var(--color-success-subtle)', color: 'var(--color-success)' },
  warning: { bg: 'var(--color-warning-subtle)', color: 'var(--color-warning)' },
  error: { bg: 'var(--color-error-subtle)', color: 'var(--color-error)' },
  info: { bg: 'var(--color-info-subtle)', color: 'var(--color-info)' }
}

const themeColors = colorMap[props.color as keyof typeof colorMap] || colorMap.primary
</script>

<template>
  <div class="stat-card">
    <div class="stat-header">
      <span class="stat-title">{{ title }}</span>
      <div v-if="icon" class="stat-icon" :style="{ background: themeColors.bg, color: themeColors.color }">
        <svg v-if="icon === 'folder'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
        </svg>
        <svg v-else-if="icon === 'api'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
          <polyline points="22,6 12,13 2,6"></polyline>
        </svg>
        <svg v-else-if="icon === 'play'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="5 3 19 12 5 21 5 3"></polygon>
        </svg>
        <svg v-else-if="icon === 'checkCircle'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
      </div>
    </div>
    <div class="stat-body">
      <span class="stat-value" :style="{ color: themeColors.color }">
        {{ value }}
      </span>
      <span v-if="suffix" class="stat-suffix">{{ suffix }}</span>
    </div>
    <div v-if="trend !== undefined" class="stat-trend" :class="{ positive: trend >= 0 }">
      <svg v-if="trend >= 0" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <polyline points="18 15 12 9 6 15"></polyline>
      </svg>
      <svg v-else width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
      <span>{{ trend >= 0 ? '+' : '' }}{{ trend }}%</span>
    </div>
  </div>
</template>

<style scoped>
.stat-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  transition: all var(--duration-normal) var(--ease-out);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-subtle);
  opacity: 0;
  transition: opacity var(--duration-fast) var(--ease-out);
}

.stat-card:hover {
  border-color: var(--color-border-hover);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-3);
}

.stat-title {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  font-weight: var(--font-medium);
}

.stat-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-body {
  display: flex;
  align-items: baseline;
  gap: var(--space-1);
}

.stat-value {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  line-height: 1;
  letter-spacing: -0.02em;
}

.stat-suffix {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}

.stat-trend {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  margin-top: var(--space-3);
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  color: var(--color-error);
  padding: var(--space-1) var(--space-2);
  background: var(--color-error-subtle);
  border-radius: var(--radius-sm);
}

.stat-trend.positive {
  color: var(--color-success);
  background: var(--color-success-subtle);
}
</style>