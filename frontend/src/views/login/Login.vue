<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-left">
        <div class="brand">
          <el-icon :size="48" color="#409eff"><FirstAidKit /></el-icon>
          <h1>AI智能医疗问诊平台</h1>
          <p>基于RAG + 知识图谱的智能医疗系统</p>
        </div>
        <div class="features">
          <div class="feature-item">
            <el-icon><ChatDotRound /></el-icon>
            <span>AI智能问诊</span>
          </div>
          <div class="feature-item">
            <el-icon><Share /></el-icon>
            <span>知识图谱推理</span>
          </div>
          <div class="feature-item">
            <el-icon><UserFilled /></el-icon>
            <span>在线预约挂号</span>
          </div>
          <div class="feature-item">
            <el-icon><Service /></el-icon>
            <span>人工医生咨询</span>
          </div>
        </div>
      </div>
      <div class="login-right">
        <h2>欢迎登录</h2>
        <el-tabs v-model="activeRole" class="login-tabs" @tab-change="handleTabChange">
          <el-tab-pane label="患者登录" name="user" />
          <el-tab-pane label="医生登录" name="doctor" />
          <el-tab-pane label="管理员登录" name="admin" />
        </el-tabs>
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          @keyup.enter="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              :prefix-icon="User"
              size="large"
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              :prefix-icon="Lock"
              show-password
              size="large"
            />
          </el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-btn"
            :loading="loading"
            @click="handleLogin"
          >
            登 录
          </el-button>
        </el-form>
        <div class="login-footer">
          <span v-if="activeRole === 'user'">
            还没有账号？
            <router-link to="/register">立即注册</router-link>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { getRoleHome } from '@/utils/auth'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loginFormRef = ref(null)
const loading = ref(false)
const activeRole = ref('user')

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度3-20位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 4, max: 20, message: '密码长度4-20位', trigger: 'blur' }
  ]
}

function handleTabChange() {
  loginForm.username = ''
  loginForm.password = ''
  loginFormRef.value?.clearValidate()
}

async function handleLogin() {
  if (!loginFormRef.value) return
  try {
    await loginFormRef.value.validate()
    loading.value = true
    await userStore.login({
      username: loginForm.username,
      password: loginForm.password,
      role: activeRole.value
    })
    ElMessage.success('登录成功')
    const redirect = route.query.redirect
    if (redirect) {
      router.push(decodeURIComponent(redirect))
    } else {
      router.push(getRoleHome(activeRole.value))
    }
  } catch (err) {
    // 错误已在拦截器中处理
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.login-box {
  width: 900px;
  height: 520px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  display: flex;
  overflow: hidden;
}
.login-left {
  width: 48%;
  background: linear-gradient(135deg, #1890ff 0%, #36cfc9 100%);
  padding: 50px 40px;
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.brand h1 {
  font-size: 24px;
  margin: 16px 0 8px;
}
.brand p {
  font-size: 14px;
  opacity: 0.85;
  margin: 0;
}
.features {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
}
.feature-item .el-icon {
  font-size: 20px;
}
.login-right {
  flex: 1;
  padding: 50px 50px 30px;
  display: flex;
  flex-direction: column;
}
.login-right h2 {
  font-size: 24px;
  margin: 0 0 20px;
  color: #303133;
  font-weight: 600;
}
.login-tabs {
  margin-bottom: 10px;
}
:deep(.login-tabs .el-tabs__header) {
  margin-bottom: 20px;
}
.login-form {
  margin-top: 10px;
}
.login-btn {
  width: 100%;
  margin-top: 10px;
}
.login-footer {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  color: #909399;
}
.login-footer a {
  color: #409eff;
  text-decoration: none;
}
</style>
