<template>
  <div class="scenes-view">
    <div class="view-header">
      <h2 class="view-title">测试场景</h2>
      <el-button type="primary" @click="showCreateDialog = true">
        新建场景
      </el-button>
    </div>

    <div class="scene-list" v-if="scenes.length">
      <div v-for="scene in scenes" :key="scene.id" class="scene-card">
        <div class="scene-header">
          <div class="scene-icon">🎬</div>
          <div class="scene-info">
            <div class="scene-name">{{ scene.name }}</div>
            <div class="scene-desc">{{ scene.description || '暂无描述' }}</div>
          </div>
        </div>
        <div class="scene-footer">
          <el-button size="small" type="primary" @click="handleRun(scene)">运行</el-button>
          <el-button size="small" @click="handleEdit(scene)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scene.id)">删除</el-button>
        </div>
      </div>
    </div>

    <div class="empty-state" v-else>
      <div class="empty-icon">🎬</div>
      <p class="empty-text">暂无测试场景</p>
      <el-button type="primary" @click="showCreateDialog = true">创建第一个场景</el-button>
    </div>

    <el-dialog v-model="showCreateDialog" title="创建测试场景" width="600px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="场景名称" />
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
import { sceneApi, type TestScene } from '@/api/api'
import { runApi } from '@/api/run'

const route = useRoute()
const scenes = ref<TestScene[]>([])
const showCreateDialog = ref(false)

const form = reactive({
  name: '',
  description: ''
})

const projectId = computed(() => Number(route.params.projectId))

onMounted(async () => {
  await fetchScenes()
})

async function fetchScenes() {
  try {
    scenes.value = await sceneApi.list(projectId.value) as unknown as TestScene[]
  } catch {
    ElMessage.error('获取场景列表失败')
  }
}

async function handleCreate() {
  try {
    await sceneApi.create(projectId.value, form)
    ElMessage.success('创建成功')
    showCreateDialog.value = false
    await fetchScenes()
  } catch {
    ElMessage.error('创建失败')
  }
}

function handleEdit(_scene: TestScene) {
  // 编辑功能
}

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除该场景吗？', '提示', { type: 'warning' })
    await sceneApi.delete(id)
    ElMessage.success('删除成功')
    await fetchScenes()
  } catch {
    // 用户取消
  }
}

async function handleRun(scene: TestScene) {
  try {
    const result = await runApi.runSceneSync({ scene_id: scene.id }) as unknown as { status: string; failed_steps?: number }
    if (result.status === 'passed') {
      ElMessage.success('场景执行成功')
    } else {
      ElMessage.error(`场景执行失败: ${result.failed_steps || 0} 个步骤失败`)
    }
  } catch {
    ElMessage.error('执行失败')
  }
}
</script>

<style scoped>
.scenes-view {
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

.scene-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4);
}

.scene-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  border: 1px solid var(--color-border);
}

.scene-header {
  display: flex;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.scene-icon {
  font-size: 28px;
}

.scene-name {
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: var(--space-1);
}

.scene-desc {
  font-size: 12px;
  color: var(--color-text-muted);
}

.scene-footer {
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