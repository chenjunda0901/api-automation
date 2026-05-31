/**
 * Dashboard Statistics Composable
 * 仪表盘统计数据管理
 */
import { ref } from 'vue'
import { dashboardApi, type DashboardStats, type TrendDataPoint, type HealthScore, type SceneStat, type FailedScene, type QuickAction } from '@/api/dashboard'

export function useDashboardStats() {
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  
  // 统计数据
  const stats = ref({
    totalProjects: 0,
    totalApis: 0,
    totalScenes: 0,
    totalRuns: 0,
    passRate: 0,
    avgDuration: 0
  })
  
  // 趋势数据
  const trendData = ref<TrendDataPoint[]>([])
  
  // 健康度评分
  const healthScore = ref<HealthScore>({
    score: 0,
    level: 'critical',
    trend: 0
  })
  
  // 热门场景（按执行次数）
  const topScenes = ref<SceneStat[]>([])
  
  // 失败场景
  const failedScenes = ref<FailedScene[]>([])
  
  // 快捷操作
  const quickActions = ref<QuickAction[]>([])
  
  // 获取统计数据
  async function fetchStats() {
    isLoading.value = true
    error.value = null
    
    try {
      const data = await dashboardApi.getStats() as unknown as DashboardStats
      
      stats.value = {
        totalProjects: data.total_projects,
        totalApis: data.total_apis,
        totalScenes: data.total_scenes,
        totalRuns: data.total_runs,
        passRate: data.pass_rate,
        avgDuration: data.avg_duration
      }
      
      trendData.value = data.trend_data
      healthScore.value = data.health_score
      topScenes.value = data.top_scenes
      failedScenes.value = data.failed_scenes
      quickActions.value = data.quick_actions
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
    quickActions,
    fetchStats
  }
}