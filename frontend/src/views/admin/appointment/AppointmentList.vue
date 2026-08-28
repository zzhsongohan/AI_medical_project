<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">预约管理</h2>
      <div class="header-actions">
        <el-input v-model="keyword" placeholder="搜索患者/医生" clearable style="width: 200px" @keyup.enter="loadList">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <el-select v-model="deptFilter" placeholder="科室筛选" clearable style="width: 160px" @change="loadList">
          <el-option v-for="dept in departments" :key="dept.id" :label="dept.name" :value="dept.id" />
        </el-select>
        <el-select v-model="statusFilter" placeholder="状态筛选" clearable style="width: 140px" @change="loadList">
          <el-option label="待确认" :value="0" />
          <el-option label="已确认" :value="1" />
          <el-option label="已完成" :value="2" />
          <el-option label="已取消" :value="3" />
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
      <el-table-column prop="department_name" label="科室" width="130" />
      <el-table-column prop="visit_date" label="就诊日期" width="120" />
      <el-table-column prop="time_slot" label="时段" width="100" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }"><StatusTag :status="row.status" type="appointment" /></template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" show-overflow-tooltip />
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="updateStatus(row, 1)" v-if="row.status === 0">确认</el-button>
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
import { getAdminAppointments, deleteAppointment, updateAppointmentStatus } from '@/api/appointment'
import { getDepartmentList } from '@/api/department'

const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const loading = ref(false)
const keyword = ref('')
const deptFilter = ref(null)
const statusFilter = ref(null)
const departments = ref([])

async function loadDepts() {
  try { departments.value = await getDepartmentList() } catch (e) {}
}

async function loadList() {
  loading.value = true
  try {
    const data = await getAdminAppointments({
      page: page.value, page_size: pageSize.value,
      keyword: keyword.value || undefined,
      department_id: deptFilter.value || undefined,
      status: statusFilter.value !== null ? statusFilter.value : undefined
    })
    list.value = data.items
    total.value = data.total
  } finally { loading.value = false }
}

async function updateStatus(row, status) {
  try {
    await updateAppointmentStatus(row.id, status)
    ElMessage.success('操作成功')
    loadList()
  } catch (e) {}
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm('确定删除该预约吗？', '提示', { type: 'warning' })
    await deleteAppointment(row.id)
    ElMessage.success('删除成功')
    loadList()
  } catch (e) {}
}

onMounted(() => { loadDepts(); loadList() })
</script>

<style scoped>.header-actions { display: flex; gap: 12px; }</style>
