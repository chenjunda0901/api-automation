<template>
  <div class="projects-view">
    <div class="page-header">
      <h2 class="page-title">项目管理</h2>
      <el-button type="primary" @click="showCreateDialog = true">
        新建项目
      </el-button>
    </div>

    <div class="projects-grid stagger-enter" v-if="projectStore.projects.length">
      <div 
        v-for="project in projectStore.projects" 
        :key="project.id"
        class="project-card"
        @click="goToProject(project.id)"
      >
        <div class="project-card-header">
          <div class="project-icon">📁</div>
          <div class="project-actions" @click.stop>
            <el-dropdown trigger="click">
              <span class="more-btn">⋮</span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleEdit(project)">编辑</el-dropdown-item>
                  <el-dropdown-item @click="handleDelete(project.id)" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
        <div class="project-card-body">
          <h3 class="project-name">{{ project.name }}</h3>
          <p class="project-desc">{{ project.description || '暂无描述' }}</p>
        </div>
        <div class="project-card-footer">
          <span class="project-date">{{ formatDate(project.created_at) }}</span>
        </div>
      </div>
    </div>

    <div class="empty-state" v-else>
      <div class="empty-icon">📁</div>
      <p class="empty-text">暂无项目</p>
      <el-button type="primary" @click="showCreateDialog = true">创建第一个项目</el-button>
    </div>

    <el-dialog v-model="showCreateDialog" title="创建项目" width="500px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" placeholder="请输入项目描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useProjectStore } from '@/stores/projectStore'
import type { Project } from '@/api/project'

const router = useRouter()
const projectStore = useProjectStore()

const showCreateDialog = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({
  name: '',
  description: ''
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }]
}

onMounted(() => {
  projectStore.fetchProjects()
})

async function handleCreate() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    try {
      const project = await projectStore.createProject(form) as unknown as Project
      ElMessage.success('创建成功')
      showCreateDialog.value = false
      form.name = ''
      form.description = ''
      router.push(`/projects/${project.id}/apis`)
    } catch {
      ElMessage.error('创建失败')
    }
  })
}

function handleEdit(_project: Project) {
  // 编辑功能
}

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除该项目吗？', '提示', { type: 'warning' })
    await projectStore.deleteProject(id)
    ElMessage.success('删除成功')
  } catch {
    // 用户取消
  }
}

function goToProject(id: number) {
  router.push(`/projects/${id}/apis`)
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.projects-view {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.page-title {
  font-size: 20px;
  font-weight: 600;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-4);
}

.project-card {
  background: var(--surface-card);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid var(--border-default);
}

.project-card:hover {
  box-shadow: var(--shadow-card-hover);
  transform: translateY(-2px);
}

.project-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.project-icon {
  font-size: 32px;
}

.more-btn {
  font-size: 20px;
  cursor: pointer;
  padding: var(--space-2);
}

.project-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.project-desc {
  font-size: 14px;
  color: var(--text-muted);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-card-footer {
  margin-top: var(--space-4);
  padding-top: var(--space-3);
  border-top: 1px solid var(--border-subtle);
}

.project-date {
  font-size: 12px;
  color: var(--text-muted);
}

.empty-state {
  text-align: center;
  padding: var(--space-12);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: var(--space-4);
}

.empty-text {
  font-size: 16px;
  color: var(--text-muted);
  margin-bottom: var(--space-6);
}
</style>