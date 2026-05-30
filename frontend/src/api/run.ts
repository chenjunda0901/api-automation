import request from './request'

export interface RunSceneRequest {
  scene_id: number
  environment_id?: number
}

export interface RunResult {
  report_id: number
  status: string
  message: string
}

export interface RunResultSync extends RunResult {
  total_steps: number
  passed_steps: number
  failed_steps: number
  steps: any[]
}

export const runApi = {
  runScene: (data: RunSceneRequest) => request.post<RunResult>('/run/scene', data),
  runSceneSync: (data: RunSceneRequest) => request.post<RunResultSync>('/run/scene/sync', data)
}