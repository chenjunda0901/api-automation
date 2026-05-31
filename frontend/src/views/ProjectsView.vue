<template>
  <div class="projects-view">
    <div class="page-header">
      <div class="header-left">
        <h2 class="page-title">项目管理</h2>
        <span class="project-count">{{ projectStore.projects.length }} 个项目</span>
      </div>
      <el-button type="primary" @click="showCreateDialog = true">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="margin-right: 6px;">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
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
          <div class="project-icon-wrapper">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
            </svg>
          </div>
          <div class="project-actions" @click.stop>
            <el-dropdown trigger="click">
              <span class="more-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="1"></circle>
                  <circle cx="19" cy="12" r="1"></circle>
                  <circle cx="5" cy="12" r="1"></circle>
                </svg>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleEdit(project)">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 6px;">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                    编辑
                  </el-dropdown-item>
                  <el-dropdown-item @click="handleDelete(project.id)" divided style="color: var(--color-error);">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 6px;">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                    删除
                  </el-dropdown-item>
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
          <div class="project-meta">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
            <span>{{ formatDate(project.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="empty-state" v-else>
      <div class="empty-illustration">
        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
        </svg>
      </div>
      <h3 class="empty-title">暂无项目</h3>
      <p class="empty-text">创建您的第一个项目，开始自动化测试之旅</p>
      <el-button type="primary" @click="showCreateDialog = true">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="margin-right: 6px;">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        创建第一个项目
      </el-button>
    </div>

    <el-dialog v-model="showCreateDialog" title="创建项目" width="480px" :close-on-click-modal="false">
      <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
        <el-form-item label="项目名称" prop="name">
          <el-input 
            v-model="form.name" 
            placeholder="请输入项目名称" 
            maxlength="50"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="描述">
          <el-input 
            v-model="form.description" 
            type="textarea" 
            :rows="3"
            placeholder="请输入项目描述（可选）"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false" size="large">取消</el-button>
        <el-button type="primary" @click="handleCreate" size="large">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
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

// Debug: 监听 projects 变化
console.log('[ProjectsView] Initial projects:', projectStore.projects.length)
watch(() => projectStore.projects.length, (newLen) => {
  console.log('[ProjectsView] watch - projects.length changed to:', newLen)
})

onMounted(async () => {
  console.log('[ProjectsView] onMounted')
  console.log('[ProjectsView] projects before fetch:', projectStore.projects.length)
  await projectStore.fetchProjects()
  console.log('[ProjectsView] projects after fetch:', projectStore.projects.length)
  // 强制触发响应式更新
  projectStore.projects = [...projectStore.projects]
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
    await ElMessageBox.confirm('确定要删除该项目吗？此操作不可恢复。', '删除确认', { 
      type: 'warning',
      confirmButtonText: '删除',
      cancelButtonText: '取消'
    })
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
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' })
}
</script>

<style scoped>
.projects-view {
  max-width: var(--content-max-width);
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-5);
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.page-title {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--color-text);
  margin: 0;
}

.project-count {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  background: var(--color-surface-muted);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-4);
}

.project-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  cursor: pointer;
  transition: all var(--duration-normal) var(--ease-out);
  position: relative;
  overflow: hidden;
}

.project-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradient-subtle);
  opacity: 0;
  transition: opacity var(--duration-fast) var(--ease-out);
}

.project-card:hover {
  border-color: var(--color-border-hover);
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.project-card:hover::before {
  opacity: 1;
}

.project-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-4);
}

.project-icon-wrapper {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-radius: var(--radius-lg);
  transition: all var(--duration-fast) var(--ease-out);
}

.project-card:hover .project-icon-wrapper {
  background: var(--color-primary);
  color: white;
}

.more-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: var(--radius-md);
  color: var(--color-text-muted);
  transition: all var(--duration-fast) var(--ease-out);
}

.more-btn:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
}

.project-name {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--color-text);
  margin-bottom: var(--space-2);
  line-height: var(--leading-tight);
}

.project-desc {
  font-size: var(--text-sm);
  color: var(--color-text-tertiary);
  line-height: var(--leading-relaxed);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin: 0;
}

.project-card-footer {
  margin-top: var(--space-4);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border-subtle);
}

.project-meta {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: var(--space-16) var(--space-8);
  background: var(--color-surface);
  border: 1px dashed var(--color-border);
  border-radius: var(--radius-xl);
}

.empty-illustration {
  width: 100px;
  height: 100px;
  margin: 0 auto var(--space-5);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-surface-muted);
  border-radius: var(--radius-2xl);
  color: var(--color-text-muted);
}

.empty-title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--color-text);
  margin-bottom: var(--space-2);
}

.empty-text {
  font-size: var(--text-sm);
  color: var(--color-text-tertiary);
  margin-bottom: var(--space-6);
  max-width: 320px;
  margin-left: auto;
  margin-right: auto;
}

/* 入场动画 */
.stagger-enter > * {
  opacity: 0;
  animation: fadeInUp var(--duration-slow) var(--ease-out) forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>