<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">问诊回复</h2>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="待回复" name="pending" />
        <el-tab-pane label="全部" name="all" />
      </el-tabs>
    </div>

    <div v-loading="loading" class="consult-list">
      <div v-for="item in displayList" :key="item.id" class="consult-card">
        <div class="consult-header">
          <div class="patient-info">
            <el-avatar :size="40" :src="getAvatar(item.user_avatar)">
              {{ item.user_name?.charAt(0) }}
            </el-avatar>
            <div>
              <div class="patient-name">{{ item.user_name || '患者' }}</div>
              <div class="consult-time">{{ item.create_time }}</div>
            </div>
          </div>
          <StatusTag :status="item.status" type="consult" />
        </div>
        <div class="complaint">
          <span class="label">主诉：</span>
          {{ item.chief_complaint }}
        </div>
        <div v-if="item.replies && item.replies.length" class="reply-section">
          <div class="reply-title">已回复 ({{ item.replies.length }})</div>
          <div v-for="reply in item.replies" :key="reply.id" class="reply-item">
            <div class="reply-time">{{ reply.create_time }}</div>
            <div class="reply-content">{{ reply.content }}</div>
          </div>
        </div>
        <div class="consult-action" v-if="item.status === 0">
          <el-button type="primary" @click="openReplyDialog(item)">
            <el-icon><Edit /></el-icon>回复
          </el-button>
        </div>
      </div>
      <el-empty v-if="!displayList.length && !loading" description="暂无问诊" />
    </div>

    <el-dialog v-model="replyDialogVisible" title="回复问诊" width="500px">
      <div class="complaint-preview">
        <div class="label">患者主诉：</div>
        <div class="content">{{ currentConsult?.chief_complaint }}</div>
      </div>
      <el-form :model="replyForm" :rules="replyRules" ref="replyFormRef" style="margin-top: 20px;">
        <el-form-item label="回复内容" prop="content" label-width="100px">
          <el-input v-model="replyForm.content" type="textarea" :rows="6" placeholder="请输入回复内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="replyDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitReply">提交回复</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Edit } from '@element-plus/icons-vue'
import StatusTag from '@/components/StatusTag.vue'
import { getDoctorPendingConsults, replyConsult } from '@/api/consult'

const list = ref([])
const loading = ref(false)
const activeTab = ref('pending')

const replyDialogVisible = ref(false)
const currentConsult = ref(null)
const submitting = ref(false)
const replyFormRef = ref(null)
const replyForm = reactive({
  content: ''
})
const replyRules = {
  content: [{ required: true, message: '请输入回复内容', trigger: 'blur' }]
}

const displayList = computed(() => {
  if (activeTab.value === 'pending') {
    return list.value.filter(item => item.status === 0)
  }
  return list.value
})

function getAvatar(avatar) {
  if (!avatar) return ''
  if (avatar.startsWith('http')) return avatar
  return (import.meta.env.VITE_UPLOAD_BASE_URL || '') + avatar
}

async function loadList() {
  loading.value = true
  try {
    list.value = await getDoctorPendingConsults()
  } finally {
    loading.value = false
  }
}

function openReplyDialog(item) {
  currentConsult.value = item
  replyForm.content = ''
  replyDialogVisible.value = true
  replyFormRef.value?.clearValidate()
}

async function submitReply() {
  if (!replyFormRef.value || !currentConsult.value) return
  try {
    await replyFormRef.value.validate()
    submitting.value = true
    await replyConsult({
      consult_id: currentConsult.value.id,
      content: replyForm.content
    })
    ElMessage.success('回复成功')
    replyDialogVisible.value = false
    loadList()
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadList()
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
.patient-info {
  display: flex;
  align-items: center;
  gap: 12px;
}
.patient-name {
  font-weight: 600;
  font-size: 15px;
}
.consult-time {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}
.complaint {
  color: #303133;
  line-height: 1.6;
  margin-bottom: 12px;
}
.complaint .label {
  color: #909399;
}
.reply-section {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #e4e7ed;
}
.reply-title {
  color: #67c23a;
  font-size: 13px;
  margin-bottom: 8px;
}
.reply-item {
  background: #f0f9eb;
  border-radius: 6px;
  padding: 10px 12px;
  margin-bottom: 6px;
}
.reply-time {
  font-size: 12px;
  color: #67c23a;
  margin-bottom: 4px;
}
.reply-content {
  font-size: 14px;
  color: #303133;
  line-height: 1.6;
}
.consult-action {
  margin-top: 12px;
  text-align: right;
}
.complaint-preview {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 12px 16px;
}
.complaint-preview .label {
  color: #909399;
  font-size: 13px;
  margin-bottom: 4px;
}
.complaint-preview .content {
  color: #303133;
  line-height: 1.6;
}
</style>
