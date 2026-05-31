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
  primary: { bg: 'rgba(99, 102, 241, 0.1)', color: '#6366F1' },
  success: { bg: 'rgba(16, 185, 129, 0.1)', color: '#10B981' },
  warning: { bg: 'rgba(245, 158, 11, 0.1)', color: '#F59E0B' },
  error: { bg: 'rgba(239, 68, 68, 0.1)', color: '#EF4444' },
  info: { bg: 'rgba(34, 211, 238, 0.1)', color: '#22D3EE' }
}

const themeColors = colorMap[props.color as keyof typeof colorMap] || colorMap.primary
</script>

<template>
  <div class="stat-card">
    <div class="stat-header">
      <span class="stat-title">{{ title }}</span>
      <div v-if="icon" class="stat-icon" :style="{ background: themeColors.bg }">
        <AppIcon :name="icon" :size="18" />
      </div>
    </div>
    <div class="stat-body">
      <span class="stat-value" :style="{ color: themeColors.color }">
        {{ value }}
      </span>
      <span v-if="suffix" class="stat-suffix">{{ suffix }}</span>
    </div>
    <div v-if="trend !== undefined" class="stat-trend" :class="{ positive: trend >= 0 }">
      <AppIcon :name="trend >= 0 ? 'chevronUp' : 'chevronDown'" :size="14" />
      <span>{{ trend >= 0 ? '+' : '' }}{{ trend }}%</span>
    </div>
  </div>
</template>

<style scoped>
.stat-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  transition: all var(--duration-normal) var(--ease-out);
}

.stat-card:hover {
  border-color: var(--color-border-hover);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
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
  color: inherit;
}

.stat-body {
  display: flex;
  align-items: baseline;
  gap: var(--space-1);
}

.stat-value {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  line-height: 1;
}

.stat-suffix {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  margin-top: var(--space-2);
  font-size: var(--text-sm);
  color: var(--color-error);
}

.stat-trend.positive {
  color: var(--color-success);
}
</style>