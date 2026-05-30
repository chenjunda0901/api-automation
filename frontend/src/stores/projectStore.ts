import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { projectApi, type Project, type Environment } from '@/api/project'

export const useProjectStore = defineStore('project', () => {
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const environments = ref<Environment[]>([])
  const currentEnvironment = ref<Environment | null>(null)
  const loading = ref(false)

  const projectMap = computed(() => {
    const map: Record<number, Project> = {}
    projects.value.forEach(p => { map[p.id] = p })
    return map
  })

  async function fetchProjects() {
    loading.value = true
    try {
      projects.value = await projectApi.list() as unknown as Project[]
    } finally {
      loading.value = false
    }
  }

  async function fetchProject(id: number) {
    loading.value = true
    try {
      currentProject.value = await projectApi.get(id) as unknown as Project
    } finally {
      loading.value = false
    }
  }

  async function createProject(data: { name: string; description?: string }) {
    const project = await projectApi.create(data) as unknown as Project
    projects.value.unshift(project)
    return project
  }

  async function deleteProject(id: number) {
    await projectApi.delete(id)
    projects.value = projects.value.filter(p => p.id !== id)
    if (currentProject.value?.id === id) {
      currentProject.value = null
    }
  }

  async function fetchEnvironments(projectId: number) {
    environments.value = await projectApi.listEnvironments(projectId) as unknown as Environment[]
  }

  async function createEnvironment(projectId: number, data: { name: string; variables?: Record<string, string>; headers?: Record<string, string> }) {
    const env = await projectApi.createEnvironment(projectId, data) as unknown as Environment
    environments.value.push(env)
    return env
  }

  async function deleteEnvironment(projectId: number, envId: number) {
    await projectApi.deleteEnvironment(projectId, envId)
    environments.value = environments.value.filter(e => e.id !== envId)
  }

  function selectEnvironment(env: Environment | null) {
    currentEnvironment.value = env
  }

  return {
    projects,
    currentProject,
    environments,
    currentEnvironment,
    loading,
    projectMap,
    fetchProjects,
    fetchProject,
    createProject,
    deleteProject,
    fetchEnvironments,
    createEnvironment,
    deleteEnvironment,
    selectEnvironment
  }
})