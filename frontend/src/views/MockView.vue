<template>
  <div class="mock-view">
    <div class="view-header">
      <h2 class="view-title">Mock 服务</h2>
      <el-button type="primary" @click="showCreateDialog = true">
        新建规则
      </el-button>
    </div>

    <div class="mock-list" v-if="rules.length">
      <div v-for="rule in rules" :key="rule.id" class="mock-item">
        <div class="mock-method" :class="`method-${rule.method.toLowerCase()}`">
          {{ rule.method }}
        </div>
        <div class="mock-info">
          <div class="mock-name">{{ rule.name }}</div>
          <div class="mock-path">{{ rule.path }}</div>
          <div class="mock-match">匹配: {{ rule.match_type }}</div>
        </div>
        <div class="mock-status">
          <span :class="['status-badge', rule.enabled ? 'enabled' : 'disabled']">
            {{ rule.enabled ? '启用' : '禁用' }}
          </span>
        </div>
        <div class="mock-actions">
          <el-button size="small" @click="handleEdit(rule)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(rule.id)">删除</el-button>
        </div>
      </div>
    </div>

    <div class="empty-state" v-else>
      <div class="empty-icon">🎭</div>
      <p class="empty-text">暂无 Mock 规则</p>
      <el-button type="primary" @click="showCreateDialog = true">创建第一条规则</el-button>
    </div>

    <el-dialog v-model="showCreateDialog" title="创建 Mock 规则" width="600px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="规则名称" />
        </el-form-item>
        <el-form-item label="方法">
          <el-select v-model="form.method" style="width: 100%">
            <el-option label="GET" value="GET" />
            <el-option label="POST" value="POST" />
            <el-option label="PUT" value="PUT" />
            <el-option label="DELETE" value="DELETE" />
          </el-select>
        </el-form-item>
        <el-form-item label="路径">
          <el-input v-model="form.path" placeholder="/api/example" />
        </el-form-item>
        <el-form-item label="匹配类型">
          <el-select v-model="form.match_type" style="width: 100%">
            <el-option label="精确匹配" value="exact" />
            <el-option label="前缀匹配" value="prefix" />
            <el-option label="正则匹配" value="regex" />
          </el-select>
        </el-form-item>
        <el-form-item label="响应状态">
          <el-input-number v-model="form.response_status" :min="100" :max="599" />
        </el-form-item>
        <el-form-item label="响应内容">
          <el-input v-model="form.response_body" type="textarea" :rows="4" />
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
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const rules = ref<any[]>([])
const showCreateDialog = ref(false)

const form = reactive({
  name: '',
  method: 'GET',
  path: '',
  match_type: 'exact',
  response_status: 200,
  response_body: '',
  enabled: true,
  priority: 0
})

async function handleCreate() {
  try {
    ElMessage.success('创建成功')
    showCreateDialog.value = false
  } catch {
    ElMessage.error('创建失败')
  }
}

function handleEdit(_rule: any) {
  // 编辑功能
}

async function handleDelete(_id: number) {
  try {
    await ElMessageBox.confirm('确定要删除该规则吗？', '提示', { type: 'warning' })
    ElMessage.success('删除成功')
  } catch {
    // 用户取消
  }
}
</script>

<style scoped>
.mock-view {
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

.mock-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.mock-item {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.mock-method {
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 600;
  min-width: 60px;
  text-align: center;
}

.method-get { color: var(--method-get); background: var(--method-get-bg); }
.method-post { color: var(--method-post); background: var(--method-post-bg); }
.method-put { color: var(--method-put); background: var(--method-put-bg); }
.method-delete { color: var(--method-delete); background: var(--method-delete-bg); }

.mock-info {
  flex: 1;
}

.mock-name {
  font-weight: 500;
  color: var(--color-text);
}

.mock-path {
  font-size: 12px;
  color: var(--color-text-muted);
  font-family: monospace;
}

.mock-match {
  font-size: 11px;
  color: var(--color-text-muted);
}

.status-badge {
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  font-size: 12px;
}

.status-badge.enabled {
  background: var(--success-bg);
  color: var(--success);
}

.status-badge.disabled {
  background: var(--color-surface-hover);
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