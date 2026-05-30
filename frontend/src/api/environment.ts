import request from './request'

export interface EnvVar {
  key: string
  value: string
}

export const environmentApi = {
  list: (projectId: number) => request.get(`/projects/${projectId}/environments`),
  create: (projectId: number, data: { name: string; variables?: Record<string, string>; headers?: Record<string, string> }) =>
    request.post(`/projects/${projectId}/environments`, data),
  get: (projectId: number, envId: number) =>
    request.get(`/projects/${projectId}/environments/${envId}`),
  update: (projectId: number, envId: number, data: any) =>
    request.put(`/projects/${projectId}/environments/${envId}`, data),
  delete: (projectId: number, envId: number) =>
    request.delete(`/projects/${projectId}/environments/${envId}`)
}