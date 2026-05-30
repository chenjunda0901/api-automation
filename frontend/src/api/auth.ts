import request from './request'

export interface User {
  id: number
  username: string
  email?: string
  is_active: boolean
  is_superuser: boolean
  created_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export const authApi = {
  login: (data: LoginRequest) => request.post<TokenResponse>('/auth/login/json', data),
  register: (data: { username: string; password: string; email?: string }) => 
    request.post<User>('/auth/register', data),
  getCurrentUser: () => request.get<User>('/auth/me')
}