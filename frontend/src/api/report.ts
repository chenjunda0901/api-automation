import request from './request'

export interface TestReport {
  id: number
  scene_id: number
  status: string
  total_steps: number
  passed_steps: number
  failed_steps: number
  duration_ms?: number
  started_at: string
  finished_at?: string
}

export interface ReportStep {
  id: number
  report_id: number
  step_name: string
  step_type: string
  status: string
  request_data?: any
  response_data?: any
  assertions_result?: any[]
  error_message?: string
  duration_ms?: number
  created_at: string
}

export const reportApi = {
  list: (sceneId: number, limit = 50) => 
    request.get<TestReport[]>(`/reports/scene/${sceneId}?limit=${limit}`),
  get: (id: number) => request.get<TestReport>(`/reports/${id}`),
  getSteps: (reportId: number) => request.get<ReportStep[]>(`/reports/${reportId}/steps`),
  listAll: (projectId: number, limit = 100) =>
    request.get(`/reports?project_id=${projectId}&limit=${limit}`)
}