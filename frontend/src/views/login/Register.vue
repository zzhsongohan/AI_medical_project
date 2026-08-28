<template>
  <div class="register-container">
    <div class="register-box">
      <div class="register-header">
        <el-icon :size="36" color="#409eff"><FirstAidKit /></el-icon>
        <h2>患者注册</h2>
        <p>欢迎加入AI智能医疗问诊平台</p>
      </div>
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="100px"
        class="register-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="registerForm.password" type="password" show-password placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input v-model="registerForm.confirm_password" type="password" show-password placeholder="请再次输入密码" />
        </el-form-item>
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="registerForm.real_name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="registerForm.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-button
          type="primary"
          size="large"
          class="register-btn"
          :loading="loading"
          @click="handleRegister"
        >
          注 册
        </el-button>
      </el-form>
      <div class="register-footer">
        已有账号？<router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { validatePhone, validateConfirmPassword } from '@/utils/validate'

const router = useRouter()
const userStore = useUserStore()

const registerFormRef = ref(null)
const loading = ref(false)

const registerForm = reactive({
  username: '',
  password: '',
  confirm_password: '',
  real_name: '',
  phone: ''
})

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度3-20位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 4, max: 20, message: '密码长度4-20位', trigger: 'blur' }
  ],
  confirm_password: [
    { validator: validateConfirmPassword(() => registerForm.password), trigger: 'blur' }
  ],
  real_name: [
    { min: 1, max: 20, message: '姓名长度1-20位', trigger: 'blur' }
  ],
  phone: [
    { validator: validatePhone, trigger: 'blur' }
  ]
}

async function handleRegister() {
  if (!registerFormRef.value) return
  try {
    await registerFormRef.value.validate()
    loading.value = true
    await userStore.register(registerForm)
    ElMessage.success('注册成功')
    router.push('/user/home')
  } catch (err) {
    // 错误已在拦截器中处理
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.register-box {
  width: 500px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  padding: 40px 50px;
}
.register-header {
  text-align: center;
  margin-bottom: 30px;
}
.register-header h2 {
  font-size: 24px;
  margin: 12px 0 6px;
  color: #303133;
}
.register-header p {
  color: #909399;
  font-size: 14px;
  margin: 0;
}
.register-btn {
  width: 100%;
  margin-top: 10px;
}
.register-footer {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  color: #909399;
}
.register-footer a {
  color: #409eff;
  text-decoration: none;
}
</style>
