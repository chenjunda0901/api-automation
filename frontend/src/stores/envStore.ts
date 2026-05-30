import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useEnvStore = defineStore('environment', () => {
  const variables = ref<Record<string, string>>({})
  const headers = ref<Record<string, string>>({})

  function loadFromEnvironment(env: { variables?: Record<string, string>; headers?: Record<string, string> } | null) {
    if (env) {
      variables.value = { ...env.variables }
      headers.value = { ...env.headers }
    } else {
      variables.value = {}
      headers.value = {}
    }
  }

  function renderValue(value: string): string {
    // 支持 {{variable}} 语法
    return value.replace(/\{\{(\w+)\}\}/g, (_, key) => variables.value[key] || '')
  }

  function setVariable(key: string, value: string) {
    variables.value[key] = value
  }

  function removeVariable(key: string) {
    delete variables.value[key]
  }

  return {
    variables,
    headers,
    loadFromEnvironment,
    renderValue,
    setVariable,
    removeVariable
  }
})