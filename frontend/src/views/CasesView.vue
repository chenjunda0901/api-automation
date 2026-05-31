<template>
  <div class="cases-view">
    <div class="view-header">
      <h2 class="view-title">测试用例</h2>
      <el-button type="primary" @click="showCreateDialog = true">
        新建用例
      </el-button>
    </div>

    <div class="case-list" v-if="cases.length">
      <div v-for="caseItem in cases" :key="caseItem.id" class="case-item">
        <div class="case-icon">🧪</div>
        <div class="case-info">
          <div class="case-name">{{ caseItem.name }}</div>
          <div class="case-desc">{{ caseItem.description || '暂无描述' }}</div>
        </div>
        <div class="case-meta">
          <span v-if="caseItem.assertions?.length" class="assertion-count">
            {{ caseItem.assertions.length }} 断言
          </span>
        </div>
        <div class="case-actions">
          <el-button size="small" @click="handleEdit(caseItem)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(caseItem.id)">删除</el-button>
        </div>
      </div>
    </div>

    <div class="empty-state" v-else>
      <div class="empty-icon">🧪</div>
      <p class="empty-text">暂无测试用例</p>
      <el-button type="primary" @click="showCreateDialog = true">创建第一个用例</el-button>
    </div>

    <el-dialog v-model="showCreateDialog" title="创建测试用例" width="600px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="用例名称" />
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
import { caseApi, type TestCase } from '@/api/api'

const route = useRoute()
const cases = ref<TestCase[]>([])
const showCreateDialog = ref(false)

const form = reactive({
  name: '',
  description: ''
})

const projectId = computed(() => Number(route.params.projectId))

onMounted(async () => {
  await fetchCases()
})

async function fetchCases() {
  try {
    cases.value = await caseApi.list(projectId.value) as unknown as TestCase[]
  } catch {
    ElMessage.error('获取用例列表失败')
  }
}

async function handleCreate() {
  try {
    await caseApi.create(projectId.value, form)
    ElMessage.success('创建成功')
    showCreateDialog.value = false
    await fetchCases()
  } catch {
    ElMessage.error('创建失败')
  }
}

function handleEdit(_item: TestCase) {
  // 编辑功能
}

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除该用例吗？', '提示', { type: 'warning' })
    await caseApi.delete(id)
    ElMessage.success('删除成功')
    await fetchCases()
  } catch {
    // 用户取消
  }
}
</script>

<style scoped>
.cases-view {
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

.case-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.case-item {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.case-icon {
  font-size: 24px;
}

.case-info {
  flex: 1;
}

.case-name {
  font-weight: 500;
  color: var(--color-text);
  margin-bottom: 2px;
}

.case-desc {
  font-size: 12px;
  color: var(--color-text-muted);
}

.case-meta {
  margin-right: var(--space-4);
}

.assertion-count {
  font-size: 12px;
  color: var(--color-text-muted);
  padding: var(--space-1) var(--space-2);
  background: var(--color-surface-hover);
  border-radius: var(--radius-sm);
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