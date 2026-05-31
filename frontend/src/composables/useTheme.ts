/**
 * API Pilot Theme System
 * 深色/浅色/跟随系统 三模式切换
 */
import { ref, watch, computed } from 'vue'
import { useLocalStorage } from '@vueuse/core'

export type ThemeMode = 'dark' | 'light' | 'system'
export type ResolvedTheme = 'dark' | 'light'

const STORAGE_KEY = 'api-pilot-theme'
const mediaQuery = '(prefers-color-scheme: dark)'

export function useTheme() {
  // 从本地存储读取主题设置
  const themeMode = useLocalStorage<ThemeMode>(STORAGE_KEY, 'dark')
  
  // 解析后的实际主题
  const resolvedTheme = ref<ResolvedTheme>('dark')
  
  // 计算实际主题
  const updateResolvedTheme = () => {
    if (themeMode.value === 'system') {
      resolvedTheme.value = window.matchMedia(mediaQuery).matches ? 'dark' : 'light'
    } else {
      resolvedTheme.value = themeMode.value
    }
    
    // 应用到 document
    document.documentElement.setAttribute('data-theme', resolvedTheme.value)
    
    // 更新 CSS 变量
    applyThemeVariables(resolvedTheme.value)
  }
  
  // 应用主题变量
  const applyThemeVariables = (theme: ResolvedTheme) => {
    const root = document.documentElement
    
    if (theme === 'dark') {
      root.style.setProperty('--color-bg', '#0B0D17')
      root.style.setProperty('--color-surface', '#13151F')
      root.style.setProperty('--color-surface-elevated', '#1A1D2E')
      root.style.setProperty('--color-surface-hover', 'rgba(255, 255, 255, 0.03)')
      root.style.setProperty('--color-surface-active', 'rgba(99, 102, 241, 0.08)')
      root.style.setProperty('--color-border', 'rgba(255, 255, 255, 0.06)')
      root.style.setProperty('--color-border-hover', 'rgba(255, 255, 255, 0.1)')
      root.style.setProperty('--color-text', '#F8FAFC')
      root.style.setProperty('--color-text-secondary', '#94A3B8')
      root.style.setProperty('--color-text-muted', '#64748B')
    } else {
      root.style.setProperty('--color-bg', '#F8FAFC')
      root.style.setProperty('--color-surface', '#FFFFFF')
      root.style.setProperty('--color-surface-elevated', '#F1F5F9')
      root.style.setProperty('--color-surface-hover', 'rgba(0, 0, 0, 0.03)')
      root.style.setProperty('--color-surface-active', 'rgba(99, 102, 241, 0.05)')
      root.style.setProperty('--color-border', 'rgba(0, 0, 0, 0.08)')
      root.style.setProperty('--color-border-hover', 'rgba(0, 0, 0, 0.12)')
      root.style.setProperty('--color-text', '#0F172A')
      root.style.setProperty('--color-text-secondary', '#475569')
      root.style.setProperty('--color-text-muted', '#94A3B8')
    }
  }
  
  // 初始化
  updateResolvedTheme()
  
  // 监听系统主题变化
  window.matchMedia(mediaQuery).addEventListener('change', () => {
    if (themeMode.value === 'system') {
      updateResolvedTheme()
    }
  })
  
  // 监听主题模式变化
  watch(themeMode, () => {
    updateResolvedTheme()
  })
  
  // 设置主题
  const setTheme = (mode: ThemeMode) => {
    themeMode.value = mode
  }
  
  // 切换主题（循环切换）
  const toggleTheme = () => {
    const modes: ThemeMode[] = ['dark', 'light', 'system']
    const currentIndex = modes.indexOf(themeMode.value)
    const nextIndex = (currentIndex + 1) % modes.length
    themeMode.value = modes[nextIndex]
  }
  
  // 是否为深色模式
  const isDark = computed(() => resolvedTheme.value === 'dark')
  
  // 图标名称
  const themeIcon = computed(() => {
    if (themeMode.value === 'system') return 'settings'
    return themeMode.value === 'dark' ? 'moon' : 'sun'
  })
  
  // 主题标签
  const themeLabel = computed(() => {
    const labels: Record<ThemeMode, string> = {
      dark: '深色',
      light: '浅色',
      system: '跟随系统'
    }
    return labels[themeMode.value]
  })
  
  return {
    themeMode,
    resolvedTheme,
    setTheme,
    toggleTheme,
    isDark,
    themeIcon,
    themeLabel
  }
}