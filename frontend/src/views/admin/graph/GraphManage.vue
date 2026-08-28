<template>
  <div class="page-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-title">图谱统计</div>
          <div v-loading="loadingStats" class="stat-list">
            <div v-for="(item, key) in stats" :key="key" class="stat-item">
              <span class="label">{{ key }}</span>
              <span class="value">{{ item }}</span>
            </div>
            <el-empty v-if="!Object.keys(stats).length && !loadingStats" description="暂无数据" :image-size="60" />
          </div>
        </el-card>
        <el-card class="search-card">
          <div class="stat-title">实体搜索</div>
          <el-input v-model="searchKeyword" placeholder="搜索疾病/症状/药物..." clearable @keyup.enter="searchEntities">
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
          <div v-if="searchResults.length" class="search-results">
            <div
              v-for="item in searchResults"
              :key="item.name"
              class="search-item"
              @click="viewEntity(item)"
            >
              <el-tag size="small" :type="tagType(item.type)">{{ item.type }}</el-tag>
              <span class="name">{{ item.name }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="18">
        <el-card>
          <template #header>
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <span>知识图谱</span>
              <el-radio-group v-model="viewMode" size="small">
                <el-radio-button value="full">完整图谱</el-radio-button>
                <el-radio-button value="subgraph">实体子图</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <GraphView
            v-if="graphNodes.length"
            :nodes="graphNodes"
            :edges="graphEdges"
            height="550px"
            @node-click="handleNodeClick"
          />
          <el-empty v-else description="暂无图谱数据" />
        </el-card>
        <el-card v-if="selectedNode" class="detail-card" style="margin-top: 20px;">
          <template #header>
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <span>实体详情：{{ selectedNode.name || selectedNode.id }}</span>
              <el-button type="primary" link size="small" @click="loadDiseaseDetail">
                查看疾病详情
              </el-button>
            </div>
          </template>
          <div v-loading="detailLoading" class="entity-detail">
            <template v-if="diseaseDetail">
              <div v-if="diseaseDetail.department" class="detail-row">
                <span class="label">所属科室：</span>
                <span>{{ diseaseDetail.department.join('、') }}</span>
              </div>
              <div v-if="diseaseDetail.symptoms" class="detail-row">
                <span class="label">相关症状：</span>
                <el-tag v-for="s in diseaseDetail.symptoms.slice(0,10)" :key="s" size="small" effect="plain" style="margin:2px;">{{ s }}</el-tag>
              </div>
              <div v-if="diseaseDetail.drugs" class="detail-row">
                <span class="label">推荐药物：</span>
                <el-tag v-for="d in diseaseDetail.drugs.slice(0,10)" :key="d" size="small" type="success" effect="plain" style="margin:2px;">{{ d }}</el-tag>
              </div>
              <div v-if="diseaseDetail.checks" class="detail-row">
                <span class="label">检查项目：</span>
                <el-tag v-for="c in diseaseDetail.checks.slice(0,10)" :key="c" size="small" type="warning" effect="plain" style="margin:2px;">{{ c }}</el-tag>
              </div>
            </template>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search } from '@element-plus/icons-vue'
import GraphView from '@/components/GraphView.vue'
import { getGraphStats, getFullGraph, getSubgraph, searchGraph, getDiseaseDetail } from '@/api/graph'

const stats = ref({})
const loadingStats = ref(false)
const searchKeyword = ref('')
const searchResults = ref([])
const viewMode = ref('full')
const graphNodes = ref([])
const graphEdges = ref([])
const selectedNode = ref(null)
const diseaseDetail = ref(null)
const detailLoading = ref(false)

function tagType(type) {
  const map = { Disease: 'danger', Symptom: 'warning', Department: 'primary', Drug: 'success', Check: 'info', Food: '' }
  return map[type] || 'info'
}

async function loadStats() {
  loadingStats.value = true
  try {
    stats.value = await getGraphStats()
  } catch (e) {}
  finally { loadingStats.value = false }
}

async function loadFullGraph() {
  try {
    const data = await getFullGraph()
    graphNodes.value = data.nodes || []
    graphEdges.value = data.edges || []
  } catch (e) {}
}

async function searchEntities() {
  if (!searchKeyword.value.trim()) {
    searchResults.value = []
    return
  }
  try {
    searchResults.value = await searchGraph(searchKeyword.value)
  } catch (e) {}
}

async function viewEntity(item) {
  viewMode.value = 'subgraph'
  try {
    const data = await getSubgraph(item.name)
    graphNodes.value = data.nodes || []
    graphEdges.value = data.edges || []
    selectedNode.value = item
  } catch (e) {}
}

function handleNodeClick(node) {
  selectedNode.value = node
}

async function loadDiseaseDetail() {
  if (!selectedNode.value?.name) return
  detailLoading.value = true
  diseaseDetail.value = null
  try {
    diseaseDetail.value = await getDiseaseDetail(selectedNode.value.name)
  } catch (e) {}
  finally { detailLoading.value = false }
}

onMounted(() => {
  loadStats()
  loadFullGraph()
})
</script>

<style scoped>
.stat-card, .search-card {
  margin-bottom: 20px;
}
.stat-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 12px;
}
.stat-list {
  min-height: 120px;
}
.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 14px;
}
.stat-item:last-child { border-bottom: none; }
.stat-item .label { color: #606266; }
.stat-item .value { font-weight: 600; color: #409eff; }
.search-results {
  margin-top: 12px;
  max-height: 300px;
  overflow-y: auto;
}
.search-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 4px;
  cursor: pointer;
}
.search-item:hover { background: #f5f7fa; }
.search-item .name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
}
.detail-card .entity-detail {
  min-height: 80px;
}
.detail-row {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
  line-height: 1.8;
}
.detail-row .label {
  color: #909399;
  flex-shrink: 0;
  width: 100px;
}
</style>
