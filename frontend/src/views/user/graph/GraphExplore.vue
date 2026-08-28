<template>
  <div class="page-container">
    <div class="graph-header">
      <h2 class="page-title">知识图谱</h2>
      <p class="page-desc">探索医疗知识图谱，了解疾病、症状、药物之间的关系</p>
    </div>

    <el-card class="infer-card">
      <div class="infer-title">
        <el-icon :size="20" color="#409eff"><MagicStick /></el-icon>
        <span>症状推理疾病</span>
      </div>
      <div class="infer-search">
        <el-input
          v-model="searchKeyword"
          placeholder="输入症状关键词，搜索并添加..."
          clearable
          @keyup.enter="searchAndAdd"
        >
          <template #prefix><el-icon><Search /></el-icon></template>
          <template #append>
            <el-button @click="searchAndAdd">搜索</el-button>
          </template>
        </el-input>
      </div>
      <div v-if="filteredSymptoms.length" class="search-results">
        <span class="results-label">搜索结果（点击添加）：</span>
        <el-tag
          v-for="item in filteredSymptoms"
          :key="item.name"
          class="result-tag"
          size="large"
          type="info"
          effect="plain"
          @click="addSymptom(item.name)"
        >
          + {{ item.name }}
        </el-tag>
      </div>
      <div v-else-if="searchKeyword.trim() && !searchLoading && !filteredSymptoms.length" class="search-empty">
        未找到匹配的症状，试试其他关键词
      </div>
      <div class="selected-symptoms">
        <span class="label">已选症状：</span>
        <el-tag
          v-for="symptom in selectedSymptoms"
          :key="symptom"
          class="symptom-tag"
          size="large"
          closable
          @close="removeSymptom(symptom)"
        >
          {{ symptom }}
        </el-tag>
        <el-button v-if="selectedSymptoms.length" type="danger" text size="small" @click="clearSymptoms">
          清空
        </el-button>
      </div>
      <el-button type="primary" :disabled="selectedSymptoms.length === 0" :loading="inferLoading" @click="doInfer" class="infer-btn">
        <el-icon><MagicStick /></el-icon>
        开始推理
      </el-button>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="16">
        <el-card>
          <template #header>
            <span>知识图谱可视化</span>
          </template>
          <GraphView
            v-if="graphNodes.length"
            :nodes="graphNodes"
            :edges="graphEdges"
            height="500px"
            @node-click="handleNodeClick"
          />
          <el-empty v-else description="点击上方「开始推理」查看疾病图谱" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>推理结果</span>
          </template>
          <div v-loading="inferLoading" class="infer-results">
            <div
              v-for="(item, idx) in inferResults"
              :key="idx"
              class="infer-item"
              @click="viewDisease(item.name || item.disease)"
            >
              <div class="rank">{{ idx + 1 }}</div>
              <div class="disease-info">
                <div class="disease-name">{{ item.name || item.disease }}</div>
                <div class="disease-prob">相关度：{{ (item.probability || item.score || 0) * 100 || '—' }}%</div>
              </div>
              <el-icon class="arrow"><ArrowRight /></el-icon>
            </div>
            <el-empty v-if="!inferResults.length && !inferLoading" description="请选择症状进行推理" :image-size="80" />
          </div>
        </el-card>

        <el-card v-if="diseaseDetail" style="margin-top: 20px;">
          <template #header>
            <span>疾病详情：{{ diseaseDetail.name }}</span>
          </template>
          <div class="disease-detail">
            <div v-if="diseaseDetail.department" class="detail-block">
              <div class="detail-label">所属科室</div>
              <el-tag v-for="d in diseaseDetail.department" :key="d" size="small" type="primary" effect="plain" style="margin:2px;">{{ d }}</el-tag>
            </div>
            <div v-if="diseaseDetail.symptoms" class="detail-block">
              <div class="detail-label">常见症状</div>
              <el-tag v-for="s in diseaseDetail.symptoms.slice(0,12)" :key="s" size="small" type="warning" effect="plain" style="margin:2px;">{{ s }}</el-tag>
            </div>
            <div v-if="diseaseDetail.drugs" class="detail-block">
              <div class="detail-label">推荐药物</div>
              <el-tag v-for="d in diseaseDetail.drugs.slice(0,10)" :key="d" size="small" type="success" effect="plain" style="margin:2px;">{{ d }}</el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Search, MagicStick, ArrowRight } from '@element-plus/icons-vue'
import GraphView from '@/components/GraphView.vue'
import { searchGraph, inferDisease, getDiseaseDetail, getSubgraph } from '@/api/graph'

const searchKeyword = ref('')
const searchResults = ref([])
const searchLoading = ref(false)
const selectedSymptoms = ref([])

// 只展示 Symptom 类型的搜索结果（症状推理模块只选症状）
const filteredSymptoms = computed(() =>
  searchResults.value.filter(item => item.label === 'Symptom' || item.category === 'Symptom')
)
const inferLoading = ref(false)
const inferResults = ref([])
const graphNodes = ref([])
const graphEdges = ref([])
const diseaseDetail = ref(null)

async function searchAndAdd() {
  if (!searchKeyword.value.trim()) return
  searchLoading.value = true
  try {
    searchResults.value = await searchGraph(searchKeyword.value)
  } catch (e) {
    searchResults.value = []
  } finally {
    searchLoading.value = false
  }
}

function addSymptom(name) {
  if (!selectedSymptoms.value.includes(name)) {
    selectedSymptoms.value.push(name)
  }
  searchResults.value = []
  searchKeyword.value = ''
}

function removeSymptom(name) {
  selectedSymptoms.value = selectedSymptoms.value.filter(s => s !== name)
}

function clearSymptoms() {
  selectedSymptoms.value = []
  inferResults.value = []
  graphNodes.value = []
  graphEdges.value = []
  diseaseDetail.value = null
}

async function doInfer() {
  if (selectedSymptoms.value.length === 0) return
  inferLoading.value = true
  diseaseDetail.value = null
  try {
    const data = await inferDisease(selectedSymptoms.value)
    inferResults.value = data || []
    // 加载第一个疾病的子图
    if (data && data.length > 0) {
      const firstDisease = data[0].name || data[0].disease
      if (firstDisease) {
        viewDisease(firstDisease)
      }
    }
  } catch (e) {}
  finally { inferLoading.value = false }
}

async function viewDisease(name) {
  if (!name) return
  try {
    const [detail, subgraph] = await Promise.all([
      getDiseaseDetail(name),
      getSubgraph(name)
    ])
    diseaseDetail.value = { name, ...detail }
    graphNodes.value = subgraph.nodes || []
    graphEdges.value = subgraph.edges || subgraph.links || []
  } catch (e) {}
}

function handleNodeClick(node) {
  if (node.type === 'Disease' || node.group === 'Disease') {
    viewDisease(node.name || node.id)
  }
}
</script>

<style scoped>
.graph-header {
  margin-bottom: 20px;
}
.page-desc {
  color: #909399;
  margin: 6px 0 0;
  font-size: 14px;
}
.infer-card {
  margin-bottom: 20px;
}
.infer-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
}
.infer-search {
  max-width: 500px;
  margin-bottom: 12px;
}
.search-results {
  margin-bottom: 16px;
}
.search-empty {
  color: #909399;
  font-size: 13px;
  margin-bottom: 16px;
  padding: 8px 0;
}
.results-label {
  font-size: 13px;
  color: #909399;
  margin-right: 8px;
}
.result-tag {
  margin: 4px 6px 4px 0;
  cursor: pointer;
}
.selected-symptoms {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 6px;
}
.selected-symptoms .label {
  color: #606266;
  font-size: 14px;
}
.symptom-tag {
  margin: 0;
}
.infer-btn {
  min-width: 140px;
}
.infer-results {
  min-height: 200px;
}
.infer-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 8px;
  border: 1px solid #f0f0f0;
}
.infer-item:hover {
  background: #ecf5ff;
  border-color: #d9ecff;
}
.rank {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #409eff;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
}
.disease-info {
  flex: 1;
}
.disease-name {
  font-weight: 600;
  font-size: 15px;
  color: #303133;
}
.disease-prob {
  font-size: 12px;
  color: #67c23a;
  margin-top: 2px;
}
.arrow {
  color: #c0c4cc;
}
.disease-detail {
  max-height: 320px;
  overflow-y: auto;
}
.detail-block {
  margin-bottom: 16px;
}
.detail-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 6px;
}
</style>
