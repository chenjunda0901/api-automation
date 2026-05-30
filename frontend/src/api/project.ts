import request from './request'

export interface Project {
  id: number
  name: string
  description?: string
  owner_id: number
  created_at: string
  updated_at?: string
}

export interface Environment {
  id: number
  project_id: number
  name: string
  variables: Record<string, string>
  headers: Record<string, string>
  created_at: string
  updated_at?: string
}

export const projectApi = {
  list: () => request.get<Project[]>('/projects'),
  create: (data: { name: string; description?: string }) => 
    request.post<Project>('/projects', data),
  get: (id: number) => request.get<Project>(`/projects/${id}`),
  update: (id: number, data: Partial<Project>) => 
    request.put<Project>(`/projects/${id}`, data),
  delete: (id: number) => request.delete(`/projects/${id}`),
  
  // 环境管理
  listEnvironments: (projectId: number) => 
    request.get<Environment[]>(`/projects/${projectId}/environments`),
  createEnvironment: (projectId: number, data: { name: string; variables?: Record<string, string>; headers?: Record<string, string> }) =>
    request.post<Environment>(`/projects/${projectId}/environments`, data),
  updateEnvironment: (projectId: number, envId: number, data: Partial<Environment>) =>
    request.put<Environment>(`/projects/${projectId}/environments/${envId}`, data),
  deleteEnvironment: (projectId: number, envId: number) =>
    request.delete(`/projects/${projectId}/environments/${envId}`)
}