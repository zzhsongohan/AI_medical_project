<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">我的预约</h2>
      <el-radio-group v-model="statusFilter" size="default" @change="loadList">
        <el-radio-button value="all">全部</el-radio-button>
        <el-radio-button :value="0">待确认</el-radio-button>
        <el-radio-button :value="1">已确认</el-radio-button>
        <el-radio-button :value="2">已完成</el-radio-button>
        <el-radio-button :value="3">已取消</el-radio-button>
      </el-radio-group>
    </div>

    <div v-loading="loading" class="appt-list">
      <div v-for="item in filteredList" :key="item.id" class="appt-card">
        <div class="appt-status">
          <StatusTag :status="item.status" type="appointment" />
        </div>
        <div class="appt-info">
          <div class="appt-doctor">
            <el-avatar :size="48" :src="getAvatar(item.doctor_avatar)">
              {{ item.doctor_name?.charAt(0) }}
            </el-avatar>
            <div class="doctor-detail">
              <div class="doctor-name">
                {{ item.doctor_name }}
                <el-tag size="small">{{ item.doctor_title || '医师' }}</el-tag>
              </div>
              <div class="dept-name">{{ item.department_name }}</div>
            </div>
          </div>
          <div class="appt-detail">
            <div class="detail-item">
              <el-icon><Calendar /></el-icon>
              <span>{{ item.visit_date }} {{ item.time_slot }}</span>
            </div>
            <div v-if="item.remark" class="detail-item">
              <el-icon><EditPen /></el-icon>
              <span>{{ item.remark }}</span>
            </div>
          </div>
        </div>
        <div class="appt-action">
          <el-button
            v-if="item.status === 0 || item.status === 1"
            type="danger"
            plain
            size="small"
            @click="cancelAppt(item)"
          >
            取消预约
          </el-button>
        </div>
      </div>
      <el-empty v-if="!filteredList.length && !loading" description="暂无预约记录" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Calendar, EditPen } from '@element-plus/icons-vue'
import StatusTag from '@/components/StatusTag.vue'
import { getMyAppointments, updateAppointmentStatus } from '@/api/appointment'

const list = ref([])
const loading = ref(false)
const statusFilter = ref('all')

const filteredList = computed(() => {
  if (statusFilter.value === 'all') return list.value
  return list.value.filter(item => item.status === statusFilter.value)
})

function getAvatar(avatar) {
  if (!avatar) return ''
  if (avatar.startsWith('http')) return avatar
  return (import.meta.env.VITE_UPLOAD_BASE_URL || '') + avatar
}

async function loadList() {
  loading.value = true
  try {
    list.value = await getMyAppointments()
  } finally {
    loading.value = false
  }
}

async function cancelAppt(item) {
  try {
    await ElMessageBox.confirm('确定要取消该预约吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await updateAppointmentStatus(item.id, 3)
    ElMessage.success('已取消预约')
    loadList()
  } catch (e) {}
}

onMounted(() => {
  loadList()
})
</script>

<style scoped>
.appt-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.appt-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
  border: 1px solid #f0f0f0;
}
.appt-status {
  flex-shrink: 0;
}
.appt-info {
  flex: 1;
  min-width: 0;
}
.appt-doctor {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 12px;
}
.doctor-detail {
  flex: 1;
}
.doctor-name {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.dept-name {
  font-size: 13px;
  color: #409eff;
}
.appt-detail {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #606266;
  font-size: 14px;
}
.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
}
.appt-action {
  flex-shrink: 0;
}
</style>
