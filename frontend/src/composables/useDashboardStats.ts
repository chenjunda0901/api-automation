/**
 * Dashboard Statistics Composable
 * 仪表盘统计数据管理
 */
import { ref, computed } from 'vue'
import { useProjectStore } from '@/stores/projectStore'

export interface TrendData {
  date: string
  passed: number
  failed: number
  total: number
}

export interface HealthScore {
  score: number
  level: 'excellent' | 'good' | 'warning' | 'critical'
  trend: number
}

export function useDashboardStats() {
  const projectStore = useProjectStore()
  
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  
  // 模拟数据 - 实际应该从API获取
  const stats = ref({
    totalProjects: 0,
    totalApis: 0,
    totalScenes: 0,
    totalRuns: 0,
    passRate: 0,
    avgDuration: 0
  })
  
  // 趋势数据
  const trendData = computed<TrendData[]>(() => {
    const days = 7
    const data: TrendData[] = []
    const now = new Date()
    
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date(now)
      date.setDate(date.getDate() - i)
      
      // 模拟数据
      const passed = Math.floor(Math.random() * 50) + 30
      const failed = Math.floor(Math.random() * 10)
      
      data.push({
        date: date.toISOString().split('T')[0],
        passed,
        failed,
        total: passed + failed
      })
    }
    
    return data
  })
  
  // 健康度评分
  const healthScore = computed<HealthScore>(() => {
    const recentPassRate = stats.value.passRate
    
    let score = 0
    let level: HealthScore['level'] = 'critical'
    
    if (recentPassRate >= 95) {
      score = 95 + Math.floor(Math.random() * 5)
      level = 'excellent'
    } else if (recentPassRate >= 85) {
      score = 85 + Math.floor(Math.random() * 10)
      level = 'good'
    } else if (recentPassRate >= 70) {
      score = 70 + Math.floor(Math.random() * 15)
      level = 'warning'
    } else {
      score = Math.floor(recentPassRate)
      level = 'critical'
    }
    
    return {
      score: Math.min(score, 100),
      level,
      trend: Math.random() > 0.5 ? 1 : -1
    }
  })
  
  // 热门场景（按执行次数）
  const topScenes = computed(() => [
    { id: 1, name: '用户登录流程', runs: 156, passRate: 98 },
    { id: 2, name: '订单创建流程', runs: 132, passRate: 95 },
    { id: 3, name: '支付接口测试', runs: 128, passRate: 92 },
    { id: 4, name: '数据查询接口', runs: 110, passRate: 88 },
    { id: 5, name: '文件上传接口', runs: 98, passRate: 85 }
  ])
  
  // 失败场景
  const failedScenes = computed(() => [
    { id: 1, name: '批量导出接口', failCount: 12, lastFail: '2小时前' },
    { id: 2, name: '复杂查询接口', failCount: 8, lastFail: '5小时前' },
    { id: 3, name: '通知发送接口', failCount: 5, lastFail: '1天前' }
  ])
  
  // 健康度颜色
  const healthColor = computed(() => {
    const colors = {
      excellent: '#10B981',
      good: '#22D3EE',
      warning: '#F59E0B',
      critical: '#EF4444'
    }
    return colors[healthScore.value.level]
  })
  
  // 获取统计数据
  async function fetchStats() {
    isLoading.value = true
    error.value = null
    
    try {
      // TODO: 实际API调用
      // const response = await api.get('/analytics/dashboard')
      // stats.value = response.data
      
      // 模拟数据
      stats.value = {
        totalProjects: projectStore.projects.length || 5,
        totalApis: 128,
        totalScenes: 45,
        totalRuns: 2560,
        passRate: 91.5,
        avgDuration: 1250
      }
    } catch (e) {
      error.value = '获取统计数据失败'
      console.error(e)
    } finally {
      isLoading.value = false
    }
  }
  
  return {
    isLoading,
    error,
    stats,
    trendData,
    healthScore,
    topScenes,
    failedScenes,
    healthColor,
    fetchStats
  }
}