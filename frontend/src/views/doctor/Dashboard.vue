<template>
  <div class="page-container">
    <div class="welcome-banner">
      <div class="banner-content">
        <h1>您好，{{ userStore.nickname }}医生 👋</h1>
        <p>欢迎使用AI智能医疗问诊平台</p>
      </div>
    </div>

    <el-row :gutter="20" class="stat-row">
      <el-col :span="6" v-for="item in statCards" :key="item.label">
        <el-card shadow="hover" class="stat-card" @click="goToPage(item.path)">
          <div class="stat-icon" :style="{ background: item.color }">
            <el-icon :size="24" color="#fff"><component :is="item.icon" /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ item.value }}</div>
            <div class="stat-label">{{ item.label }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <span>待回复问诊</span>
              <el-button type="primary" link @click="$router.push('/doctor/consults')">查看全部</el-button>
            </div>
          </template>
          <div v-loading="loadingConsults" class="todo-list">
            <div v-for="item in pendingConsults.slice(0, 5)" :key="item.id" class="todo-item">
              <div class="todo-user">{{ item.user_name || '患者' }}</div>
              <div class="todo-content">{{ item.chief_complaint }}</div>
            </div>
            <el-empty v-if="!pendingConsults.length && !loadingConsults" description="暂无待回复" :image-size="60" />
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <span>今日预约</span>
              <el-button type="primary" link @click="$router.push('/doctor/appointments')">查看全部</el-button>
            </div>
          </template>
          <div v-loading="loadingAppts" class="todo-list">
            <div v-for="item in todayAppts.slice(0, 5)" :key="item.id" class="todo-item">
              <div class="todo-user">{{ item.user_name || '患者' }}</div>
              <div class="todo-content">{{ item.time_slot }} - {{ item.remark || '无备注' }}</div>
            </div>
            <el-empty v-if="!todayAppts.length && !loadingAppts" description="今日暂无预约" :image-size="60" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, markRaw } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getStatOverview } from '@/api/stat'
import { getDoctorPendingConsults } from '@/api/consult'
import { getDoctorAppointments } from '@/api/appointment'
import dayjs from 'dayjs'

const router = useRouter()
const userStore = useUserStore()

const statCards = ref([
  { label: '今日预约', value: 0, icon: markRaw({ name: 'Calendar' }), color: '#409eff', path: '/doctor/appointments' },
  { label: '待回复问诊', value: 0, icon: markRaw({ name: 'ChatDotRound' }), color: '#e6a23c', path: '/doctor/consults' },
  { label: '患者档案', value: 0, icon: markRaw({ name: 'Files' }), color: '#67c23a', path: '/doctor/records' },
  { label: '累计问诊', value: 0, icon: markRaw({ name: 'Service' }), color: '#f56c6c', path: '/doctor/consults' }
])

const pendingConsults = ref([])
const todayAppts = ref([])
const loadingConsults = ref(false)
const loadingAppts = ref(false)

async function loadStats() {
  try {
    const data = await getStatOverview()
    statCards.value[0].value = data.today_appointment_count || 0
    statCards.value[1].value = data.pending_consult_count || 0
    statCards.value[2].value = data.patient_count || 0
    statCards.value[3].value = data.total_consult_count || 0
  } catch (e) {}
}

async function loadConsults() {
  loadingConsults.value = true
  try {
    pendingConsults.value = await getDoctorPendingConsults()
  } catch (e) {}
  finally { loadingConsults.value = false }
}

async function loadAppts() {
  loadingAppts.value = true
  try {
    const data = await getDoctorAppointments()
    const today = dayjs().format('YYYY-MM-DD')
    todayAppts.value = data.filter(a => dayjs(a.visit_date).format('YYYY-MM-DD') === today)
  } catch (e) {}
  finally { loadingAppts.value = false }
}

function goToPage(path) {
  router.push(path)
}

onMounted(() => {
  loadStats()
  loadConsults()
  loadAppts()
})
</script>

<style scoped>
.welcome-banner {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  border-radius: 12px;
  padding: 30px 40px;
  color: #fff;
  margin-bottom: 20px;
}
.welcome-banner h1 {
  margin: 0 0 8px;
  font-size: 24px;
}
.welcome-banner p {
  margin: 0;
  opacity: 0.85;
  font-size: 14px;
}
.stat-row {
  margin-bottom: 20px;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 8px;
  cursor: pointer;
}
.stat-card:hover {
  transform: translateY(-2px);
  transition: transform 0.2s;
}
.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.stat-value {
  font-size: 22px;
  font-weight: 600;
}
.stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 2px;
}
.todo-list {
  min-height: 220px;
}
.todo-item {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}
.todo-item:last-child {
  border-bottom: none;
}
.todo-user {
  font-size: 14px;
  font-weight: 500;
  color: #409eff;
  margin-bottom: 4px;
}
.todo-content {
  font-size: 13px;
  color: #606266;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
