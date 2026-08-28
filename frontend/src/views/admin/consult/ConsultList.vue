<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">问诊管理</h2>
      <div class="header-actions">
        <el-input v-model="keyword" placeholder="搜索" clearable style="width: 200px" @keyup.enter="loadList">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <el-select v-model="statusFilter" placeholder="状态筛选" clearable style="width: 140px" @change="loadList">
          <el-option label="待回复" :value="0" />
          <el-option label="已回复" :value="1" />
          <el-option label="已关闭" :value="2" />
        </el-select>
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
      <el-table-column prop="user_name" label="患者" width="120" />
      <el-table-column prop="doctor_name" label="医生" width="120" />
      <el-table-column prop="chief_complaint" label="主诉" show-overflow-tooltip />
      <el-table-column label="状态" width="100">
        <template #default="{ row }"><StatusTag :status="row.status" type="consult" /></template>
      </el-table-column>
      <el-table-column prop="create_time" label="创建时间" width="170" />
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </PageTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import PageTable from '@/components/PageTable.vue'
import StatusTag from '@/components/StatusTag.vue'
import { getAdminConsults, deleteConsult } from '@/api/consult'

const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const loading = ref(false)
const keyword = ref('')
const statusFilter = ref(null)

async function loadList() {
  loading.value = true
  try {
    const data = await getAdminConsults({
      page: page.value, page_size: pageSize.value,
      keyword: keyword.value || undefined,
      status: statusFilter.value !== null ? statusFilter.value : undefined
    })
    list.value = data.items
    total.value = data.total
  } finally { loading.value = false }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm('确定删除该问诊工单吗？', '提示', { type: 'warning' })
    await deleteConsult(row.id)
    ElMessage.success('删除成功')
    loadList()
  } catch (e) {}
}

onMounted(() => { loadList() })
</script>

<style scoped>.header-actions { display: flex; gap: 12px; }</style>
