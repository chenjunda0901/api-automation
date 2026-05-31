<script setup lang="ts">
/**
 * Theme Switcher Component
 * 主题切换器 - 深色/浅色/跟随系统
 */
import { useTheme } from '@/composables/useTheme'

const { themeMode, setTheme, themeIcon, themeLabel } = useTheme()

const themes = [
  { value: 'dark', label: '深色', icon: 'moon' },
  { value: 'light', label: '浅色', icon: 'sun' },
  { value: 'system', label: '跟随系统', icon: 'settings' }
] as const

function handleSelect(mode: 'dark' | 'light' | 'system') {
  setTheme(mode)
}
</script>

<template>
  <el-dropdown trigger="click" @command="handleSelect">
    <div class="theme-switcher">
      <AppIcon :name="themeIcon" :size="18" class="theme-icon" />
      <span class="theme-label">{{ themeLabel }}</span>
      <AppIcon name="chevronDown" :size="14" class="chevron-icon" />
    </div>
    
    <template #dropdown>
      <el-dropdown-menu class="theme-menu">
        <el-dropdown-item 
          v-for="theme in themes" 
          :key="theme.value"
          :command="theme.value"
          class="theme-item"
          :class="{ active: themeMode === theme.value }"
        >
          <div class="theme-content">
            <AppIcon :name="theme.icon" :size="16" class="theme-icon" />
            <span class="theme-name">{{ theme.label }}</span>
            <AppIcon 
              v-if="themeMode === theme.value" 
              name="check" 
              :size="14" 
              class="check-icon" 
            />
          </div>
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<style scoped>
.theme-switcher {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
}

.theme-switcher:hover {
  background: var(--color-surface-hover);
  border-color: var(--color-border-hover);
}

.theme-icon {
  color: var(--color-text-secondary);
}

.theme-label {
  font-size: var(--text-sm);
  color: var(--color-text);
  font-weight: var(--font-medium);
}

.chevron-icon {
  color: var(--color-text-muted);
  margin-left: var(--space-1);
}

.theme-menu {
  min-width: 160px;
}

.theme-item {
  padding: var(--space-2) var(--space-3);
}

.theme-item.active {
  background: var(--color-surface-active);
}

.theme-content {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.theme-item .theme-icon {
  color: var(--color-text-secondary);
}

.theme-item.active .theme-icon {
  color: var(--color-primary);
}

.theme-name {
  flex: 1;
  font-size: var(--text-sm);
  color: var(--color-text);
}

.theme-item.active .theme-name {
  color: var(--color-primary);
  font-weight: var(--font-medium);
}

.check-icon {
  color: var(--color-primary);
}
</style>