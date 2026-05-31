import request from './request'

export interface TrendDataPoint {
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

export interface SceneStat {
  id: number
  name: string
  runs: number
  pass_rate: number
  last_run?: string
  last_status?: string
}

export interface FailedScene {
  id: number
  name: string
  fail_count: number
  last_fail: string
}

export interface QuickAction {
  id: string
  name: string
  icon: string
  route: string
}

export interface DashboardStats {
  total_projects: number
  total_apis: number
  total_scenes: number
  total_runs: number
  pass_rate: number
  avg_duration: number
  trend_data: TrendDataPoint[]
  health_score: HealthScore
  top_scenes: SceneStat[]
  failed_scenes: FailedScene[]
  quick_actions: QuickAction[]
}

export const dashboardApi = {
  getStats: () => request.get<DashboardStats>('/dashboard/stats')
}
