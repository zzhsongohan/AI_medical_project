<template>
  <div class="page-container">
    <div class="welcome-banner">
      <div class="banner-content">
        <h1>欢迎回来，{{ userStore.nickname }} 👋</h1>
        <p>AI智能医疗问诊平台，为您的健康保驾护航</p>
      </div>
    </div>

    <el-row :gutter="20" class="stat-row">
      <el-col :span="6" v-for="item in stats" :key="item.label">
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
      <el-col :span="16">
        <el-card class="quick-access">
          <template #header>
            <span>快捷功能</span>
          </template>
          <div class="quick-grid">
            <div class="quick-item" @click="$router.push('/user/chat')">
              <div class="quick-icon ai"><el-icon :size="32"><ChatDotRound /></el-icon></div>
              <span>AI智能问诊</span>
            </div>
            <div class="quick-item" @click="$router.push('/user/doctors')">
              <div class="quick-icon doctor"><el-icon :size="32"><UserFilled /></el-icon></div>
              <span>预约挂号</span>
            </div>
            <div class="quick-item" @click="$router.push('/user/consult')">
              <div class="quick-icon consult"><el-icon :size="32"><Service /></el-icon></div>
              <span>人工问诊</span>
            </div>
            <div class="quick-item" @click="$router.push('/user/graph')">
              <div class="quick-icon graph"><el-icon :size="32"><Share /></el-icon></div>
              <span>知识图谱</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="notice-card">
          <template #header>
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <span>最新公告</span>
              <el-button type="primary" link @click="$router.push('/user/articles')">更多 ></el-button>
            </div>
          </template>
          <div v-loading="loadingNotice" class="notice-list">
            <div v-for="item in notices" :key="item.id" class="notice-item" @click="showNotice(item.id)">
              <el-icon><Bell /></el-icon>
              <span class="notice-title">{{ item.title }}</span>
            </div>
            <el-empty v-if="!notices.length && !loadingNotice" description="暂无公告" />
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
import { getUserOverview } from '@/api/stat'
import { getNoticeList } from '@/api/notice'

const router = useRouter()
const userStore = useUserStore()

const stats = ref([
  { label: 'AI问诊次数', value: 0, icon: markRaw({ name: 'ChatDotRound' }), color: '#409eff', path: '/user/chat' },
  { label: '预约次数', value: 0, icon: markRaw({ name: 'Calendar' }), color: '#67c23a', path: '/user/appointment' },
  { label: '健康档案', value: 0, icon: markRaw({ name: 'Files' }), color: '#e6a23c', path: '/user/records' },
  { label: '人工问诊', value: 0, icon: markRaw({ name: 'Service' }), color: '#f56c6c', path: '/user/consult' }
])

const notices = ref([])
const loadingNotice = ref(false)

async function loadStats() {
  try {
    const data = await getUserOverview()
    stats.value[0].value = data.chat_count || 0
    stats.value[1].value = data.appointment_count || 0
    stats.value[2].value = data.record_count || 0
    stats.value[3].value = data.consult_count || 0
  } catch (e) {}
}

async function loadNotices() {
  loadingNotice.value = true
  try {
    const data = await getNoticeList()
    notices.value = data.slice(0, 5)
  } catch (e) {}
  finally {
    loadingNotice.value = false
  }
}

function goToPage(path) {
  router.push(path)
}

function showNotice(id) {
  // 可以跳转到公告详情，这里用文章详情页代替
  router.push(`/user/articles`)
}

onMounted(() => {
  loadStats()
  loadNotices()
})
</script>

<style scoped>
.welcome-banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
  transition: transform 0.2s;
}
.stat-card:hover {
  transform: translateY(-2px);
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
  color: #303133;
}
.stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 2px;
}
.quick-access {
  margin-bottom: 20px;
}
.quick-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}
.quick-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.quick-item:hover {
  background: #f5f7fa;
}
.quick-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}
.quick-icon.ai { background: linear-gradient(135deg, #667eea, #764ba2); }
.quick-icon.doctor { background: linear-gradient(135deg, #11998e, #38ef7d); }
.quick-icon.consult { background: linear-gradient(135deg, #f093fb, #f5576c); }
.quick-icon.graph { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.notice-card {
  height: 100%;
}
.notice-list {
  min-height: 200px;
}
.notice-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: color 0.2s;
}
.notice-item:hover {
  color: #409eff;
}
.notice-item:last-child {
  border-bottom: none;
}
.notice-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
}
</style>
