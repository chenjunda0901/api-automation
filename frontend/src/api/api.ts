import request from './request'

export interface ApiHeader {
  key: string
  value: string
  enabled: boolean
}

export interface ApiParam {
  key: string
  value: string
  enabled: boolean
}

export interface ApiDefinition {
  id: number
  project_id: number
  name: string
  method: string
  path: string
  description?: string
  headers: ApiHeader[]
  params: ApiParam[]
  body?: any
  body_type: string
  response?: any
  created_at: string
  updated_at?: string
}

export interface TestCase {
  id: number
  project_id: number
  name: string
  description?: string
  api_id?: number
  headers: ApiHeader[]
  params: ApiParam[]
  body?: any
  body_type: string
  pre_script?: string
  post_script?: string
  assertions: any[]
  created_at: string
  updated_at?: string
}

export interface TestScene {
  id: number
  project_id: number
  name: string
  description?: string
  global_variables: Record<string, string>
  created_at: string
  updated_at?: string
}

export interface SceneStep {
  id: number
  scene_id: number
  name: string
  step_type: string
  ref_id: number
  order: number
  enabled: boolean
  created_at: string
  updated_at?: string
}

export const apiApi = {
  list: (projectId: number) => request.get<ApiDefinition[]>(`/apis/project/${projectId}`),
  create: (projectId: number, data: Partial<ApiDefinition>) => 
    request.post<ApiDefinition>(`/apis?project_id=${projectId}`, data),
  get: (id: number) => request.get<ApiDefinition>(`/apis/${id}`),
  update: (id: number, data: Partial<ApiDefinition>) => 
    request.put<ApiDefinition>(`/apis/${id}`, data),
  delete: (id: number) => request.delete(`/apis/${id}`)
}

export const caseApi = {
  list: (projectId: number) => request.get<TestCase[]>(`/cases/project/${projectId}`),
  create: (projectId: number, data: Partial<TestCase>) => 
    request.post<TestCase>(`/cases?project_id=${projectId}`, data),
  get: (id: number) => request.get<TestCase>(`/cases/${id}`),
  update: (id: number, data: Partial<TestCase>) => 
    request.put<TestCase>(`/cases/${id}`, data),
  delete: (id: number) => request.delete(`/cases/${id}`)
}

export const sceneApi = {
  list: (projectId: number) => request.get<TestScene[]>(`/scenes/project/${projectId}`),
  create: (projectId: number, data: Partial<TestScene>) => 
    request.post<TestScene>(`/scenes?project_id=${projectId}`, data),
  get: (id: number) => request.get<TestScene>(`/scenes/${id}`),
  update: (id: number, data: Partial<TestScene>) => 
    request.put<TestScene>(`/scenes/${id}`, data),
  delete: (id: number) => request.delete(`/scenes/${id}`),
  
  // 步骤管理
  listSteps: (sceneId: number) => request.get<SceneStep[]>(`/scenes/${sceneId}/steps`),
  createStep: (sceneId: number, data: Partial<SceneStep>) => 
    request.post<SceneStep>(`/scenes/${sceneId}/steps`, data),
  updateStep: (sceneId: number, stepId: number, data: Partial<SceneStep>) => 
    request.put<SceneStep>(`/scenes/${sceneId}/steps/${stepId}`, data),
  deleteStep: (sceneId: number, stepId: number) => 
    request.delete(`/scenes/${sceneId}/steps/${stepId}`),
  reorderSteps: (sceneId: number, orders: { id: number; order: number }[]) =>
    request.post(`/scenes/${sceneId}/steps/reorder`, orders)
}