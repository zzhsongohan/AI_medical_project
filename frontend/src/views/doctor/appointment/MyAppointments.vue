<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">预约管理</h2>
      <el-radio-group v-model="statusFilter" @change="loadList">
        <el-radio-button value="all">全部</el-radio-button>
        <el-radio-button :value="0">待确认</el-radio-button>
        <el-radio-button :value="1">已确认</el-radio-button>
        <el-radio-button :value="2">已完成</el-radio-button>
        <el-radio-button :value="3">已取消</el-radio-button>
      </el-radio-group>
    </div>

    <el-table v-loading="loading" :data="filteredList" border stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="user_name" label="患者姓名" width="120" />
      <el-table-column prop="department_name" label="科室" width="130" />
      <el-table-column prop="visit_date" label="就诊日期" width="130" />
      <el-table-column prop="time_slot" label="时段" width="100" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <StatusTag :status="row.status" type="appointment" />
        </template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" show-overflow-tooltip />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button
            v-if="row.status === 0"
            type="success"
            link
            @click="updateStatus(row, 1)"
          >确认</el-button>
          <el-button
            v-if="row.status === 1"
            type="primary"
            link
            @click="updateStatus(row, 2)"
          >完成</el-button>
          <el-button
            v-if="row.status === 0 || row.status === 1"
            type="danger"
            link
            @click="updateStatus(row, 3)"
          >取消</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import StatusTag from '@/components/StatusTag.vue'
import { getDoctorAppointments, updateAppointmentStatus } from '@/api/appointment'

const list = ref([])
const loading = ref(false)
const statusFilter = ref('all')

const filteredList = computed(() => {
  if (statusFilter.value === 'all') return list.value
  return list.value.filter(item => item.status === statusFilter.value)
})

async function loadList() {
  loading.value = true
  try {
    list.value = await getDoctorAppointments()
  } finally {
    loading.value = false
  }
}

async function updateStatus(row, status) {
  try {
    await updateAppointmentStatus(row.id, status)
    ElMessage.success('操作成功')
    loadList()
  } catch (e) {}
}

onMounted(() => {
  loadList()
})
</script>
