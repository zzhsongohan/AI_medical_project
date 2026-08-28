<template>
  <div class="page-container">
    <div class="detail-card">
      <el-button link @click="$router.back()" style="margin-bottom: 16px; padding: 0;">
        <el-icon><ArrowLeft /></el-icon> 返回列表
      </el-button>
      <div v-loading="loading">
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-meta">
          <el-tag v-if="article.category" size="small" type="primary" effect="plain">{{ article.category }}</el-tag>
          <span><el-icon><View /></el-icon> {{ article.view_count || 0 }} 阅读</span>
          <span>{{ article.create_time }}</span>
        </div>
        <div class="article-content" v-html="article.content"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, View } from '@element-plus/icons-vue'
import { getArticleDetail } from '@/api/article'

const route = useRoute()
const article = ref({})
const loading = ref(false)

async function loadDetail() {
  loading.value = true
  try {
    article.value = await getArticleDetail(route.params.id)
  } finally { loading.value = false }
}

onMounted(() => { loadDetail() })
</script>

<style scoped>
.detail-card {
  max-width: 800px;
  margin: 0 auto;
  background: #fff;
  border-radius: 10px;
  padding: 30px 40px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
}
.article-title {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 16px;
  color: #303133;
}
.article-meta {
  display: flex;
  gap: 16px;
  align-items: center;
  color: #909399;
  font-size: 13px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 24px;
}
.article-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}
.article-content {
  line-height: 1.8;
  font-size: 15px;
  color: #303133;
}
.article-content :deep(img) {
  max-width: 100%;
  border-radius: 6px;
}
.article-content :deep(p) {
  margin: 0 0 16px;
}
.article-content :deep(h1),
.article-content :deep(h2),
.article-content :deep(h3) {
  margin: 24px 0 12px;
}
</style>
