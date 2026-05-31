<script setup lang="ts">
/**
 * Trend Chart Component
 * 趋势图表组件 - 使用 ECharts
 */
import { ref, computed, watch } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components'
import type { TrendDataPoint } from '@/api/dashboard'
import { useTheme } from '@/composables/useTheme'

// 注册 ECharts 组件
use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
])

interface Props {
  data: TrendDataPoint[]
  height?: number
}

const props = withDefaults(defineProps<Props>(), {
  height: 300
})

const { isDark } = useTheme()
const chartRef = ref<InstanceType<typeof VChart> | null>(null)

// 主题适配颜色
const colors = computed(() => {
  if (isDark.value) {
    return {
      passed: '#10B981',
      failed: '#EF4444',
      text: '#94A3B8',
      border: 'rgba(255, 255, 255, 0.1)',
      splitLine: 'rgba(255, 255, 255, 0.05)'
    }
  }
  return {
    passed: '#10B981',
    failed: '#EF4444',
    text: '#64748B',
    border: 'rgba(0, 0, 0, 0.1)',
    splitLine: 'rgba(0, 0, 0, 0.05)'
  }
})

const option = computed(() => ({
  backgroundColor: 'transparent',
  tooltip: {
    trigger: 'axis',
    backgroundColor: isDark.value ? 'rgba(26, 29, 46, 0.95)' : 'rgba(255, 255, 255, 0.95)',
    borderColor: colors.value.border,
    textStyle: {
      color: isDark.value ? '#F8FAFC' : '#0F172A',
      fontSize: 12
    },
    axisPointer: {
      type: 'cross',
      crossStyle: {
        color: colors.value.border
      }
    }
  },
  legend: {
    data: ['通过', '失败'],
    top: 0,
    right: 0,
    textStyle: {
      color: colors.value.text
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '40px',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: props.data.map(d => d.date.slice(5)),
    axisLine: {
      lineStyle: {
        color: colors.value.border
      }
    },
    axisLabel: {
      color: colors.value.text
    }
  },
  yAxis: {
    type: 'value',
    axisLine: {
      lineStyle: {
        color: colors.value.border
      }
    },
    axisLabel: {
      color: colors.value.text
    },
    splitLine: {
      lineStyle: {
        color: colors.value.splitLine
      }
    }
  },
  series: [
    {
      name: '通过',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: {
        width: 3,
        color: colors.value.passed
      },
      itemStyle: {
        color: colors.value.passed,
        borderWidth: 2,
        borderColor: isDark.value ? '#13151F' : '#FFFFFF'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: colors.value.passed + '40' },
            { offset: 1, color: colors.value.passed + '00' }
          ]
        }
      },
      data: props.data.map(d => d.passed)
    },
    {
      name: '失败',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: {
        width: 3,
        color: colors.value.failed
      },
      itemStyle: {
        color: colors.value.failed,
        borderWidth: 2,
        borderColor: isDark.value ? '#13151F' : '#FFFFFF'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: colors.value.failed + '30' },
            { offset: 1, color: colors.value.failed + '00' }
          ]
        }
      },
      data: props.data.map(d => d.failed)
    }
  ]
}))

// 监听主题变化
watch(isDark, () => {
  if (chartRef.value) {
    chartRef.value.setOption(option.value, true)
  }
})
</script>

<template>
  <div class="trend-chart" :style="{ height: `${height}px` }">
    <v-chart 
      ref="chartRef"
      :option="option" 
      autoresize 
      class="chart"
    />
  </div>
</template>

<style scoped>
.trend-chart {
  width: 100%;
  position: relative;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>