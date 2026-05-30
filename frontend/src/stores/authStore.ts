import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type User, type LoginRequest } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))

  const isAuthenticated = computed(() => !!token.value)

  async function login(credentials: LoginRequest) {
    const response = await authApi.login(credentials) as unknown as { access_token: string }
    token.value = response.access_token
    localStorage.setItem('access_token', response.access_token)
    await fetchCurrentUser()
    return response
  }

  async function fetchCurrentUser() {
    if (!token.value) return null
    try {
      user.value = await authApi.getCurrentUser() as unknown as User
      return user.value
    } catch {
      logout()
      return null
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    fetchCurrentUser,
    logout
  }
})