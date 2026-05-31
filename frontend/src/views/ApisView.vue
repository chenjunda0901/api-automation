<template>
  <div class="apis-view">
    <div class="view-header">
      <h2 class="view-title">接口列表</h2>
      <el-button type="primary" @click="showCreateDialog = true">
        新建接口
      </el-button>
    </div>

    <div class="api-list" v-if="apis.length">
      <div v-for="api in apis" :key="api.id" class="api-item">
        <div class="api-method" :class="`method-${api.method.toLowerCase()}`">
          {{ api.method }}
        </div>
        <div class="api-info">
          <div class="api-name">{{ api.name }}</div>
          <div class="api-path">{{ api.path }}</div>
        </div>
        <div class="api-actions">
          <el-button size="small" @click="handleEdit(api)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(api.id)">删除</el-button>
        </div>
      </div>
    </div>

    <div class="empty-state" v-else>
      <div class="empty-icon">🔗</div>
      <p class="empty-text">暂无接口</p>
      <el-button type="primary" @click="showCreateDialog = true">创建第一个接口</el-button>
    </div>

    <el-dialog v-model="showCreateDialog" title="创建接口" width="600px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="接口名称" />
        </el-form-item>
        <el-form-item label="方法">
          <el-select v-model="form.method" style="width: 100%">
            <el-option label="GET" value="GET" />
            <el-option label="POST" value="POST" />
            <el-option label="PUT" value="PUT" />
            <el-option label="DELETE" value="DELETE" />
            <el-option label="PATCH" value="PATCH" />
          </el-select>
        </el-form-item>
        <el-form-item label="路径">
          <el-input v-model="form.path" placeholder="/api/example" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" />
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
import { apiApi, type ApiDefinition } from '@/api/api'

const route = useRoute()

const apis = ref<ApiDefinition[]>([])
const showCreateDialog = ref(false)

const form = reactive({
  name: '',
  method: 'GET',
  path: '',
  description: ''
})

const projectId = computed(() => Number(route.params.projectId))

onMounted(async () => {
  await fetchApis()
})

async function fetchApis() {
  try {
    apis.value = await apiApi.list(projectId.value) as unknown as ApiDefinition[]
  } catch {
    ElMessage.error('获取接口列表失败')
  }
}

async function handleCreate() {
  try {
    await apiApi.create(projectId.value, form)
    ElMessage.success('创建成功')
    showCreateDialog.value = false
    await fetchApis()
  } catch {
    ElMessage.error('创建失败')
  }
}

function handleEdit(_api: ApiDefinition) {
  // 编辑功能
}

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除该接口吗？', '提示', { type: 'warning' })
    await apiApi.delete(id)
    ElMessage.success('删除成功')
    await fetchApis()
  } catch {
    // 用户取消
  }
}
</script>

<style scoped>
.apis-view {
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

.api-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.api-item {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.api-method {
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 600;
  min-width: 60px;
  text-align: center;
}

.method-get {
  color: var(--method-get);
  background: var(--method-get-bg);
}

.method-post {
  color: var(--method-post);
  background: var(--method-post-bg);
}

.method-put {
  color: var(--method-put);
  background: var(--method-put-bg);
}

.method-delete {
  color: var(--method-delete);
  background: var(--method-delete-bg);
}

.api-info {
  flex: 1;
}

.api-name {
  font-weight: 500;
  color: var(--color-text);
  margin-bottom: 2px;
}

.api-path {
  font-size: 12px;
  color: var(--color-text-muted);
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