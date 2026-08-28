<template>
  <div class="not-found">
    <div class="code">404</div>
    <div class="message">页面不存在</div>
    <el-button type="primary" @click="goHome">返回首页</el-button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getRoleHome } from '@/utils/auth'

const router = useRouter()
const userStore = useUserStore()

function goHome() {
  if (userStore.token) {
    router.push(getRoleHome(userStore.role))
  } else {
    router.push('/login')
  }
}
</script>

<style scoped>
.not-found {
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  background: #f5f7fa;
}
.code {
  font-size: 120px;
  font-weight: bold;
  color: #409eff;
  line-height: 1;
}
.message {
  font-size: 18px;
  color: #606266;
  margin-bottom: 20px;
}
</style>
