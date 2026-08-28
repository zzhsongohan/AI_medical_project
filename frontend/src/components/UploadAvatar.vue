<template>
  <div class="upload-avatar">
    <el-upload
      class="avatar-uploader"
      :action="uploadUrl"
      :headers="uploadHeaders"
      :show-file-list="false"
      :before-upload="beforeUpload"
      :on-success="handleSuccess"
      accept="image/*"
    >
      <el-avatar v-if="imageUrl" :size="size" :src="imageUrl" class="avatar-img" />
      <div v-else class="avatar-placeholder">
        <el-icon :size="24"><Plus /></el-icon>
      </div>
    </el-upload>
    <div v-if="tip" class="upload-tip">{{ tip }}</div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  size: {
    type: Number,
    default: 80
  },
  tip: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'success'])

const userStore = useUserStore()
const imageUrl = ref('')

const uploadUrl = computed(() => {
  const base = import.meta.env.VITE_API_BASE_URL
  return base + '/profile/avatar'
})

const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${userStore.token}`
}))

watch(() => props.modelValue, (val) => {
  if (val) {
    imageUrl.value = val.startsWith('http') ? val : (import.meta.env.VITE_UPLOAD_BASE_URL || '') + val
  }
}, { immediate: true })

function beforeUpload(file) {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('头像图片大小不能超过 2MB!')
    return false
  }
  return true
}

function handleSuccess(response) {
  if (response.code === 200) {
    const avatar = response.data.avatar
    imageUrl.value = avatar.startsWith('http') ? avatar : (import.meta.env.VITE_UPLOAD_BASE_URL || '') + avatar
    emit('update:modelValue', avatar)
    emit('success', avatar)
    ElMessage.success('上传成功')
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}
</script>

<style scoped>
.upload-avatar {
  display: inline-block;
}
.avatar-uploader {
  display: block;
}
:deep(.avatar-uploader .el-upload) {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}
:deep(.avatar-uploader .el-upload:hover) {
  border-color: #409eff;
}
.avatar-placeholder {
  width: v-bind(size + 'px');
  height: v-bind(size + 'px');
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8c939d;
  background: #f5f7fa;
  border-radius: 50%;
}
.avatar-img {
  display: block;
}
.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
  text-align: center;
}
</style>
