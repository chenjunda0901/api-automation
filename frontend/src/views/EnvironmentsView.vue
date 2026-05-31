<template>
  <div class="environments-view">
    <div class="view-header">
      <h2 class="view-title">环境配置</h2>
      <el-button type="primary" @click="showCreateDialog = true">
        新建环境
      </el-button>
    </div>

    <div class="env-list" v-if="environments.length">
      <div v-for="env in environments" :key="env.id" class="env-card">
        <div class="env-header">
          <div class="env-icon">⚙️</div>
          <div class="env-name">{{ env.name }}</div>
        </div>
        <div class="env-vars" v-if="Object.keys(env.variables || {}).length">
          <div class="vars-title">变量:</div>
          <div v-for="(value, key) in env.variables" :key="key" class="var-item">
            <span class="var-key">{{ key }}</span>
            <span class="var-value">{{ value }}</span>
          </div>
        </div>
        <div class="env-footer">
          <el-button size="small" @click="handleEdit(env)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(env.id)">删除</el-button>
        </div>
      </div>
    </div>

    <div class="empty-state" v-else>
      <div class="empty-icon">⚙️</div>
      <p class="empty-text">暂无环境配置</p>
      <el-button type="primary" @click="showCreateDialog = true">创建第一个环境</el-button>
    </div>

    <el-dialog v-model="showCreateDialog" title="创建环境" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="环境名称 (如: 测试环境)" />
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { projectApi, type Environment } from '@/api/project'

const route = useRoute()
const environments = ref<Environment[]>([])
const showCreateDialog = ref(false)

const form = reactive({
  name: '',
  variables: {} as Record<string, string>,
  headers: {} as Record<string, string>
})

const projectId = computed(() => Number(route.params.projectId))

onMounted(async () => {
  await fetchEnvironments()
})

async function fetchEnvironments() {
  try {
    environments.value = await projectApi.listEnvironments(projectId.value) as unknown as Environment[]
  } catch {
    ElMessage.error('获取环境列表失败')
  }
}

async function handleCreate() {
  try {
    await projectApi.createEnvironment(projectId.value, form)
    ElMessage.success('创建成功')
    showCreateDialog.value = false
    await fetchEnvironments()
  } catch {
    ElMessage.error('创建失败')
  }
}

function handleEdit(_env: Environment) {
  // 编辑功能
}

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除该环境吗？', '提示', { type: 'warning' })
    await projectApi.deleteEnvironment(projectId.value, id)
    ElMessage.success('删除成功')
    await fetchEnvironments()
  } catch {
    // 用户取消
  }
}
</script>

<style scoped>
.environments-view {
  max-width: 1000px;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.view-title {
  font-size: 16px;
  font-weight: 600;
}

.env-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4);
}

.env-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  border: 1px solid var(--color-border);
}

.env-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.env-icon {
  font-size: 24px;
}

.env-name {
  font-weight: 600;
  color: var(--color-text);
}

.env-vars {
  margin-bottom: var(--space-4);
}

.vars-title {
  font-size: 12px;
  color: var(--color-text-muted);
  margin-bottom: var(--space-2);
}

.var-item {
  display: flex;
  justify-content: space-between;
  padding: var(--space-1) 0;
  font-size: 12px;
}

.var-key {
  color: var(--primary-500);
  font-family: monospace;
}

.var-value {
  color: var(--color-text-secondary);
  font-family: monospace;
}

.env-footer {
  display: flex;
  gap: var(--space-2);
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border);
}

.empty-state {
  text-align: center;
  padding: var(--space-12);
  background: var(--color-surface);
  border-radius: var(--radius-lg);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: var(--space-4);
}

.empty-text {
  color: var(--color-text-muted);
  margin-bottom: var(--space-4);
}
</style>