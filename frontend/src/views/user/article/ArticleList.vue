<template>
  <div class="page-container">
    <div class="article-header">
      <h2 class="page-title">健康科普</h2>
      <div class="category-tabs">
        <el-tag
          :class="{ active: !selectedCategory }"
          size="large"
          effect="plain"
          @click="selectCategory('')"
        >全部</el-tag>
        <el-tag
          v-for="cat in categories"
          :key="cat"
          :class="{ active: selectedCategory === cat }"
          size="large"
          effect="plain"
          @click="selectCategory(cat)"
        >{{ cat }}</el-tag>
      </div>
    </div>

    <div v-loading="loading" class="article-grid">
      <div v-for="article in list" :key="article.id" class="article-card" @click="viewDetail(article.id)">
        <div v-if="article.cover" class="article-cover" :style="{ backgroundImage: `url(${getCover(article.cover)})` }"></div>
        <div class="article-content">
          <div class="article-category" v-if="article.category">
            <el-tag size="small" type="primary" effect="plain">{{ article.category }}</el-tag>
          </div>
          <h3 class="article-title">{{ article.title }}</h3>
          <div class="article-summary">{{ article.summary || article.content?.replace(/<[^>]*>/g, '').slice(0, 100) }}...</div>
          <div class="article-meta">
            <span><el-icon><View /></el-icon> {{ article.view_count || 0 }}</span>
            <span>{{ article.create_time }}</span>
          </div>
        </div>
      </div>
      <el-empty v-if="!list.length && !loading" description="暂无文章" />
    </div>

    <el-pagination
      v-if="total > 0"
      class="pagination"
      v-model:current-page="page"
      v-model:page-size="pageSize"
      :total="total"
      layout="prev, pager, next"
      background
      @current-change="loadList"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { View } from '@element-plus/icons-vue'
import { getArticleList } from '@/api/article'

const router = useRouter()
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(8)
const loading = ref(false)
const selectedCategory = ref('')
const allCategories = ref([])

const categories = computed(() => {
  const set = new Set()
  allCategories.value.forEach(c => set.add(c))
  list.value.forEach(a => a.category && set.add(a.category))
  return Array.from(set).slice(0, 8)
})

function getCover(cover) {
  if (!cover) return ''
  if (cover.startsWith('http')) return cover
  return (import.meta.env.VITE_UPLOAD_BASE_URL || '') + cover
}

async function loadList() {
  loading.value = true
  try {
    const data = await getArticleList({
      page: page.value,
      page_size: pageSize.value,
      category: selectedCategory.value || undefined
    })
    list.value = data.items || []
    total.value = data.total || 0
  } finally { loading.value = false }
}

function selectCategory(cat) {
  selectedCategory.value = cat
  page.value = 1
  loadList()
}

function viewDetail(id) {
  router.push(`/user/article/${id}`)
}

onMounted(() => { loadList() })
</script>

<style scoped>
.article-header {
  margin-bottom: 24px;
}
.category-tabs {
  display: flex;
  gap: 10px;
  margin-top: 16px;
  flex-wrap: wrap;
}
.category-tabs .el-tag {
  cursor: pointer;
}
.category-tabs .el-tag.active {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}
.article-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.article-card {
  background: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
  border: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
}
.article-card:hover {
  box-shadow: 0 6px 20px 0 rgba(0, 0, 0, 0.08);
  transform: translateY(-3px);
}
.article-cover {
  height: 180px;
  background-size: cover;
  background-position: center;
  background-color: #f0f0f0;
}
.article-content {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.article-category {
  margin-bottom: 8px;
}
.article-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  color: #303133;
}
.article-summary {
  flex: 1;
  font-size: 13px;
  color: #606266;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 12px;
}
.article-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
}
.article-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>
