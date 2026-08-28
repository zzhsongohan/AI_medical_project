<template>
  <div class="page-container">
    <el-card class="notice-card">
      <template v-if="notice">
        <h1 class="notice-title">{{ notice.title }}</h1>
        <div class="notice-meta">{{ notice.create_time }}</div>
        <div class="notice-content" v-html="notice.content"></div>
      </template>
      <el-empty v-else description="公告不存在" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getNoticeDetail } from '@/api/notice'

const route = useRoute()
const notice = ref(null)

async function loadDetail() {
  try {
    notice.value = await getNoticeDetail(route.params.id)
  } catch (e) {}
}

onMounted(() => { loadDetail() })
</script>

<style scoped>
.notice-card {
  max-width: 800px;
  margin: 0 auto;
  padding: 30px 40px;
}
.notice-title {
  font-size: 22px;
  font-weight: 600;
  margin: 0 0 12px;
  text-align: center;
}
.notice-meta {
  text-align: center;
  color: #909399;
  font-size: 13px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 24px;
}
.notice-content {
  line-height: 1.8;
  font-size: 15px;
  color: #303133;
}
</style>
