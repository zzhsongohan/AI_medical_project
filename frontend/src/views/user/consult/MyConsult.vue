<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">人工问诊</h2>
      <el-button type="primary" @click="dialogVisible = true">
        <el-icon><Plus /></el-icon>发起问诊
      </el-button>
    </div>

    <div v-loading="loading" class="consult-list">
      <div v-for="item in list" :key="item.id" class="consult-card">
        <div class="consult-header">
          <StatusTag :status="item.status" type="consult" />
          <span class="consult-time">{{ item.create_time }}</span>
        </div>
        <div class="consult-content">
          <div class="complaint-label">主诉：</div>
          <div class="complaint-text">{{ item.chief_complaint }}</div>
        </div>
        <div v-if="item.replies && item.replies.length" class="reply-section">
          <div class="reply-title">
            <el-icon><ChatLineRound /></el-icon>
            医生回复 ({{ item.replies.length }})
          </div>
          <div v-for="reply in item.replies" :key="reply.id" class="reply-item">
            <div class="reply-meta">
              <el-avatar :size="28" :src="getAvatar(reply.doctor_avatar)">
                {{ reply.doctor_name?.charAt(0) }}
              </el-avatar>
              <span class="reply-doctor">{{ reply.doctor_name }}医生</span>
              <span class="reply-time">{{ reply.create_time }}</span>
            </div>
            <div class="reply-content">{{ reply.content }}</div>
          </div>
        </div>
      </div>
      <el-empty v-if="!list.length && !loading" description="暂无问诊记录" />
    </div>

    <el-dialog v-model="dialogVisible" title="发起人工问诊" width="500px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="选择医生" prop="doctor_id">
          <el-select v-model="form.doctor_id" placeholder="可选择指定医生（可选）" style="width: 100%" clearable>
            <el-option
              v-for="doc in doctors"
              :key="doc.id"
              :label="`${doc.real_name} - ${doc.department_name}`"
              :value="doc.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="主诉症状" prop="chief_complaint">
          <el-input
            v-model="form.chief_complaint"
            type="textarea"
            :rows="4"
            placeholder="请详细描述您的症状、持续时间等信息"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitConsult">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, ChatLineRound } from '@element-plus/icons-vue'
import StatusTag from '@/components/StatusTag.vue'
import { getMyConsults, createConsult } from '@/api/consult'
import { getDoctorList } from '@/api/doctor'

const list = ref([])
const loading = ref(false)
const doctors = ref([])
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref(null)

const form = reactive({
  doctor_id: null,
  chief_complaint: ''
})

const rules = {
  chief_complaint: [{ required: true, message: '请输入主诉症状', trigger: 'blur' }]
}

function getAvatar(avatar) {
  if (!avatar) return ''
  if (avatar.startsWith('http')) return avatar
  return (import.meta.env.VITE_UPLOAD_BASE_URL || '') + avatar
}

async function loadList() {
  loading.value = true
  try {
    list.value = await getMyConsults()
  } finally {
    loading.value = false
  }
}

async function loadDoctors() {
  try {
    const data = await getDoctorList({ page: 1, page_size: 100 })
    doctors.value = data.items || []
  } catch (e) {}
}

async function submitConsult() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    submitting.value = true
    await createConsult(form)
    ElMessage.success('提交成功，医生会尽快回复您')
    dialogVisible.value = false
    form.chief_complaint = ''
    form.doctor_id = null
    loadList()
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadList()
  loadDoctors()
})
</script>

<style scoped>
.consult-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.consult-card {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
  border: 1px solid #f0f0f0;
}
.consult-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.consult-time {
  font-size: 13px;
  color: #909399;
}
.consult-content {
  display: flex;
  gap: 8px;
}
.complaint-label {
  color: #606266;
  flex-shrink: 0;
}
.complaint-text {
  color: #303133;
  line-height: 1.6;
}
.reply-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px dashed #e4e7ed;
}
.reply-title {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #606266;
  font-size: 14px;
  margin-bottom: 12px;
}
.reply-item {
  background: #f9fafc;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 8px;
}
.reply-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
.reply-doctor {
  font-weight: 500;
  color: #409eff;
  font-size: 13px;
}
.reply-time {
  font-size: 12px;
  color: #909399;
}
.reply-content {
  color: #303133;
  font-size: 14px;
  line-height: 1.6;
}
</style>
