<template>
  <div class="page-container">
    <el-card class="profile-card">
      <template #header>
        <span>个人中心</span>
      </template>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本资料" name="basic">
          <el-form :model="profileForm" label-width="100px" class="profile-form">
            <el-form-item label="头像">
              <UploadAvatar v-model="profileForm.avatar" @success="handleAvatarSuccess" />
            </el-form-item>
            <el-form-item label="用户名">
              <el-input v-model="profileForm.username" disabled />
            </el-form-item>
            <el-form-item label="昵称">
              <el-input v-model="profileForm.nickname" placeholder="请输入昵称" />
            </el-form-item>
            <el-form-item label="手机号">
              <el-input v-model="profileForm.phone" placeholder="请输入手机号" />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="profileForm.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="saving" @click="saveProfile">保存修改</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="修改密码" name="password">
          <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="120px" class="password-form">
            <el-form-item label="原密码" prop="old_password">
              <el-input v-model="passwordForm.old_password" type="password" show-password placeholder="请输入原密码" />
            </el-form-item>
            <el-form-item label="新密码" prop="new_password">
              <el-input v-model="passwordForm.new_password" type="password" show-password placeholder="请输入新密码" />
            </el-form-item>
            <el-form-item label="确认新密码" prop="confirm_password">
              <el-input v-model="passwordForm.confirm_password" type="password" show-password placeholder="请再次输入新密码" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="changingPwd" @click="handleChangePassword">确认修改</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import UploadAvatar from '@/components/UploadAvatar.vue'
import { getProfile, updateProfile, changePassword as apiChangePassword } from '@/api/profile'
import { useUserStore } from '@/stores/user'
import { validateConfirmPassword } from '@/utils/validate'

const userStore = useUserStore()

const activeTab = ref('basic')
const saving = ref(false)
const changingPwd = ref(false)
const passwordFormRef = ref(null)

const profileForm = reactive({
  username: '',
  nickname: '',
  phone: '',
  email: '',
  avatar: '',
  role: ''
})

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const passwordRules = {
  old_password: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 4, max: 20, message: '密码长度4-20位', trigger: 'blur' }
  ],
  confirm_password: [
    { validator: validateConfirmPassword(() => passwordForm.new_password), trigger: 'blur' }
  ]
}

async function loadProfile() {
  const data = await getProfile()
  Object.assign(profileForm, data)
  if (data.real_name && !data.nickname) {
    profileForm.nickname = data.real_name
  }
}

async function saveProfile() {
  saving.value = true
  try {
    await updateProfile(profileForm)
    ElMessage.success('保存成功')
    userStore.updateUserInfo(profileForm)
    userStore.fetchUserInfo()
  } finally {
    saving.value = false
  }
}

function handleAvatarSuccess(avatar) {
  userStore.updateUserInfo({ avatar })
}

async function handleChangePassword() {
  if (!passwordFormRef.value) return
  try {
    await passwordFormRef.value.validate()
    changingPwd.value = true
    await apiChangePassword(passwordForm)
    ElMessage.success('密码修改成功')
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  } finally {
    changingPwd.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.profile-card {
  max-width: 700px;
  margin: 0 auto;
}
.profile-form {
  max-width: 500px;
}
.password-form {
  max-width: 420px;
}
</style>
