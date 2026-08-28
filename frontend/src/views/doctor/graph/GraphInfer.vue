<template>
  <div class="page-container">
    <el-card class="infer-card">
      <template #header>
        <span>知识图谱 - 疾病推理</span>
      </template>
      <div class="infer-section">
        <div class="section-title">输入症状</div>
        <div class="symptom-input">
          <el-input
            v-model="inputSymptom"
            placeholder="输入症状名称，回车添加"
            @keyup.enter="addSymptom"
            style="width: 300px;"
          >
            <template #prefix><el-icon><Plus /></el-icon></template>
          </el-input>
          <el-button type="primary" @click="addSymptom" style="margin-left: 10px;">添加</el-button>
        </div>
        <div class="symptom-tags">
          <el-tag
            v-for="s in symptoms"
            :key="s"
            closable
            size="large"
            style="margin: 4px 6px;"
            @close="removeSymptom(s)"
          >
            {{ s }}
          </el-tag>
          <span v-if="!symptoms.length" class="empty-tip">请添加症状</span>
        </div>
        <el-button
          type="primary"
          :disabled="symptoms.length === 0"
          :loading="loading"
          @click="doInfer"
        >
          <el-icon><MagicStick /></el-icon>
          开始推理
        </el-button>
      </div>
    </el-card>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="10">
        <el-card>
          <template #header><span>推理结果</span></template>
          <div v-loading="loading" class="result-list">
            <div
              v-for="(item, idx) in results"
              :key="idx"
              class="result-item"
              @click="viewDetail(item.name || item.disease)"
            >
              <span class="rank">{{ idx + 1 }}</span>
              <span class="name">{{ item.name || item.disease }}</span>
            </div>
            <el-empty v-if="!results.length && !loading" description="暂无结果" />
          </div>
        </el-card>
      </el-col>
      <el-col :span="14">
        <el-card>
          <template #header><span>疾病详情</span></template>
          <div v-loading="detailLoading" class="detail-content">
            <template v-if="diseaseDetail">
              <h3>{{ diseaseDetail.name }}</h3>
              <div v-if="diseaseDetail.department" class="detail-block">
                <div class="label">科室</div>
                <el-tag v-for="d in diseaseDetail.department" :key="d" style="margin:2px;">{{ d }}</el-tag>
              </div>
              <div v-if="diseaseDetail.symptoms" class="detail-block">
                <div class="label">症状</div>
                <el-tag v-for="s in diseaseDetail.symptoms" :key="s" type="warning" effect="plain" style="margin:2px;">{{ s }}</el-tag>
              </div>
              <div v-if="diseaseDetail.drugs" class="detail-block">
                <div class="label">推荐药物</div>
                <el-tag v-for="d in diseaseDetail.drugs" :key="d" type="success" effect="plain" style="margin:2px;">{{ d }}</el-tag>
              </div>
              <div v-if="diseaseDetail.checks" class="detail-block">
                <div class="label">检查项目</div>
                <el-tag v-for="c in diseaseDetail.checks" :key="c" type="info" effect="plain" style="margin:2px;">{{ c }}</el-tag>
              </div>
            </template>
            <el-empty v-else description="点击左侧疾病查看详情" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Plus, MagicStick } from '@element-plus/icons-vue'
import { inferDisease, getDiseaseDetail } from '@/api/graph'

const symptoms = ref([])
const inputSymptom = ref('')
const results = ref([])
const loading = ref(false)
const detailLoading = ref(false)
const diseaseDetail = ref(null)

function addSymptom() {
  const s = inputSymptom.value.trim()
  if (s && !symptoms.value.includes(s)) {
    symptoms.value.push(s)
  }
  inputSymptom.value = ''
}

function removeSymptom(s) {
  symptoms.value = symptoms.value.filter(item => item !== s)
}

async function doInfer() {
  if (symptoms.value.length === 0) return
  loading.value = true
  diseaseDetail.value = null
  try {
    results.value = await inferDisease(symptoms.value)
  } catch (e) {}
  finally { loading.value = false }
}

async function viewDetail(name) {
  detailLoading.value = true
  try {
    diseaseDetail.value = { name, ...await getDiseaseDetail(name) }
  } catch (e) {}
  finally { detailLoading.value = false }
}
</script>

<style scoped>
.infer-section {
  text-align: center;
}
.section-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #303133;
}
.symptom-input {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}
.symptom-tags {
  min-height: 60px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 16px;
  text-align: left;
}
.empty-tip {
  color: #c0c4cc;
  font-size: 14px;
}
.result-list {
  min-height: 300px;
}
.result-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.result-item:hover {
  background: #ecf5ff;
  border-color: #d9ecff;
}
.rank {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #409eff;
  color: #fff;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.name {
  font-weight: 500;
}
.detail-content {
  min-height: 300px;
}
.detail-content h3 {
  margin: 0 0 20px;
  color: #303133;
}
.detail-block {
  margin-bottom: 20px;
}
.detail-block .label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 8px;
}
</style>
