<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">知识库管理</h2>
      <div class="header-actions">
        <el-input v-model="keyword" placeholder="搜索文件名" clearable style="width: 240px" @keyup.enter="loadList">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <el-upload
          :action="uploadUrl"
          :headers="uploadHeaders"
          :show-file-list="false"
          :before-upload="beforeUpload"
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
          accept=".txt,.md,.pdf,.docx,.doc"
        >
          <el-button type="primary">
            <el-icon><Upload /></el-icon>上传文件
          </el-button>
        </el-upload>
      </div>
    </div>
    <PageTable
      :data="list"
      :total="total"
      :loading="loading"
      v-model:page="page"
      v-model:page-size="pageSize"
      @change="loadList"
    >
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="file_name" label="文件名" min-width="200" show-overflow-tooltip />
      <el-table-column prop="file_type" label="类型" width="100" />
      <el-table-column label="大小" width="120">
        <template #default="{ row }">{{ formatFileSize(row.file_size) }}</template>
      </el-table-column>
      <el-table-column prop="chunk_count" label="分块数" width="100" />
      <el-table-column label="向量化状态" width="120">
        <template #default="{ row }">
          <StatusTag :status="row.vector_status" type="vector" />
        </template>
      </el-table-column>
      <el-table-column prop="upload_time" label="上传时间" width="170" />
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link :disabled="row.vector_status === 1" @click="revectorize(row)">
            重新向量化
          </el-button>
          <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </PageTable>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Upload } from '@element-plus/icons-vue'
import PageTable from '@/components/PageTable.vue'
import StatusTag from '@/components/StatusTag.vue'
import { getKnowledgeList, revectorizeFile, deleteKnowledgeFile } from '@/api/knowledge'
import { formatFileSize } from '@/utils/format'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const loading = ref(false)
const keyword = ref('')

const uploadUrl = computed(() => import.meta.env.VITE_API_BASE_URL + '/knowledge/upload')
const uploadHeaders = computed(() => ({ Authorization: `Bearer ${userStore.token}` }))

async function loadList() {
  loading.value = true
  try {
    const data = await getKnowledgeList({
      page: page.value, page_size: pageSize.value,
      keyword: keyword.value || undefined
    })
    list.value = data.items
    total.value = data.total
  } finally { loading.value = false }
}

function beforeUpload(file) {
  const allowed = ['.txt', '.md', '.pdf', '.docx', '.doc']
  const ext = '.' + file.name.split('.').pop().toLowerCase()
  if (!allowed.includes(ext)) {
    ElMessage.error('仅支持 txt、md、pdf、docx、doc 格式的文件')
    return false
  }
  if (file.size > 50 * 1024 * 1024) {
    ElMessage.error('文件大小不能超过 50MB')
    return false
  }
  return true
}

function handleUploadSuccess(response) {
  if (response.code === 200) {
    ElMessage.success('上传成功，正在向量化处理...')
    loadList()
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

function handleUploadError() {
  ElMessage.error('上传失败')
}

async function revectorize(row) {
  try {
    await revectorizeFile(row.id)
    ElMessage.success('已提交重新向量化任务')
    loadList()
  } catch (e) {}
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确定删除文件「${row.file_name}」吗？\n相关向量数据也会被删除。`, '提示', { type: 'warning' })
    await deleteKnowledgeFile(row.id)
    ElMessage.success('删除成功')
    loadList()
  } catch (e) {}
}

onMounted(() => { loadList() })
</script>

<style scoped>.header-actions { display: flex; gap: 12px; }</style>
