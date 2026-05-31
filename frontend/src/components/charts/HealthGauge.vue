<script setup lang="ts">
/**
 * Health Gauge Component
 * 健康度仪表盘
 */
import { computed } from 'vue'
import type { HealthScore } from '@/composables/useDashboardStats'

interface Props {
  score: number
  level: HealthScore['level']
  size?: number
}

const props = withDefaults(defineProps<Props>(), {
  size: 180
})

const radius = computed(() => props.size / 2 - 20)
const circumference = computed(() => 2 * Math.PI * radius.value)
const dashOffset = computed(() => {
  const progress = props.score / 100
  return circumference.value * (1 - progress)
})

const strokeColor = computed(() => {
  const colors = {
    excellent: '#10B981',
    good: '#22D3EE',
    warning: '#F59E0B',
    critical: '#EF4444'
  }
  return colors[props.level]
})

const labelText = computed(() => {
  const labels = {
    excellent: '优秀',
    good: '良好',
    warning: '警告',
    critical: '危险'
  }
  return labels[props.level]
})
</script>

<template>
  <div class="health-gauge" :style="{ width: `${size}px`, height: `${size}px` }">
    <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`">
      <!-- 背景圆弧 -->
      <circle
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        fill="none"
        :stroke="`var(--color-border)`"
        :stroke-width="12"
        stroke-linecap="round"
        :stroke-dasharray="circumference"
        :transform="`rotate(-90 ${size / 2} ${size / 2})`"
      />
      
      <!-- 进度圆弧 -->
      <circle
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        fill="none"
        :stroke="strokeColor"
        :stroke-width="12"
        stroke-linecap="round"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="dashOffset"
        :transform="`rotate(-90 ${size / 2} ${size / 2})`"
        class="progress-arc"
      />
      
      <!-- 渐变定义 -->
      <defs>
        <linearGradient :id="`gauge-gradient-${level}`" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" :stop-color="strokeColor" stop-opacity="0.8"/>
          <stop offset="100%" :stop-color="strokeColor"/>
        </linearGradient>
      </defs>
    </svg>
    
    <!-- 中心内容 -->
    <div class="gauge-content">
      <div class="gauge-value" :style="{ color: strokeColor }">
        {{ score }}
      </div>
      <div class="gauge-label">{{ labelText }}</div>
    </div>
    
    <!-- 发光效果 -->
    <div 
      class="gauge-glow" 
      :style="{ backgroundColor: strokeColor }"
    ></div>
  </div>
</template>

<style scoped>
.health-gauge {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.health-gauge svg {
  position: absolute;
  top: 0;
  left: 0;
}

.progress-arc {
  transition: stroke-dashoffset 1s ease-out;
  filter: drop-shadow(0 0 6px currentColor);
}

.gauge-content {
  position: relative;
  z-index: 1;
  text-align: center;
}

.gauge-value {
  font-family: var(--font-display);
  font-size: 2.5rem;
  font-weight: var(--font-bold);
  line-height: 1;
}

.gauge-label {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-top: var(--space-1);
}

.gauge-glow {
  position: absolute;
  width: 60%;
  height: 60%;
  border-radius: 50%;
  filter: blur(40px);
  opacity: 0.15;
  z-index: 0;
}
</style>