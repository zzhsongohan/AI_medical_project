<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">数据概览</h2>
    </div>
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6" v-for="item in statCards" :key="item.label">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" :style="{ background: item.color }">
            <el-icon :size="28" color="#fff"><component :is="item.icon" /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ item.value || '--' }}</div>
            <div class="stat-label">{{ item.label }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>
            <span>问诊趋势（近7天）</span>
          </template>
          <div ref="consultTrendChart" class="chart"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>
            <span>科室预约分布</span>
          </template>
          <div ref="apptDeptChart" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>
            <span>用户增长趋势（近7天）</span>
          </template>
          <div ref="userGrowthChart" class="chart"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>
            <span>知识库文件类型分布</span>
          </template>
          <div ref="knowledgeTypeChart" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, markRaw } from 'vue'
import * as echarts from 'echarts'
import { getStatOverview, getConsultTrend, getAppointmentDept, getUserGrowth, getKnowledgeType } from '@/api/stat'

const consultTrendChart = ref(null)
const apptDeptChart = ref(null)
const userGrowthChart = ref(null)
const knowledgeTypeChart = ref(null)

const statCards = ref([
  { label: '用户总数', value: 0, icon: markRaw({ name: 'User' }), color: '#409eff' },
  { label: '医生总数', value: 0, icon: markRaw({ name: 'UserFilled' }), color: '#67c23a' },
  { label: '科室数量', value: 0, icon: markRaw({ name: 'OfficeBuilding' }), color: '#e6a23c' },
  { label: '预约总数', value: 0, icon: markRaw({ name: 'Calendar' }), color: '#f56c6c' },
  { label: '问诊总数', value: 0, icon: markRaw({ name: 'ChatDotRound' }), color: '#909399' },
  { label: '文章数量', value: 0, icon: markRaw({ name: 'Reading' }), color: '#8e44ad' }
])

async function loadOverview() {
  try {
    const data = await getStatOverview()
    statCards.value[0].value = data.user_count || 0
    statCards.value[1].value = data.doctor_count || 0
    statCards.value[2].value = data.department_count || 0
    statCards.value[3].value = data.appointment_count || 0
    statCards.value[4].value = data.consult_count || 0
    statCards.value[5].value = data.article_count || 0
  } catch (e) {}
}

function initLineChart(dom, data, title) {
  const chart = echarts.init(dom)
  chart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.map(d => d.date),
      boundaryGap: false
    },
    yAxis: { type: 'value' },
    series: [{
      name: title,
      type: 'line',
      smooth: true,
      areaStyle: { opacity: 0.3 },
      data: data.map(d => d.count),
      itemStyle: { color: '#409eff' }
    }]
  })
  return chart
}

function initPieChart(dom, data) {
  const chart = echarts.init(dom)
  chart.setOption({
    tooltip: { trigger: 'item' },
    legend: { orient: 'vertical', left: 'left' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 6, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
      data: data.map((d, i) => ({ name: d.name, value: d.value }))
    }]
  })
  return chart
}

async function loadCharts() {
  try {
    const [trend, apptDept, userGrowth, knowledgeType] = await Promise.all([
      getConsultTrend(7),
      getAppointmentDept(),
      getUserGrowth(7),
      getKnowledgeType()
    ])
    if (consultTrendChart.value) initLineChart(consultTrendChart.value, trend, '问诊量')
    if (apptDeptChart.value) initPieChart(apptDeptChart.value, apptDept)
    if (userGrowthChart.value) initLineChart(userGrowthChart.value, userGrowth, '新增用户')
    if (knowledgeTypeChart.value) initPieChart(knowledgeTypeChart.value, knowledgeType)
  } catch (e) {}
}

onMounted(() => {
  loadOverview()
  loadCharts()
  window.addEventListener('resize', () => {
    document.querySelectorAll('.chart').forEach(el => {
      const inst = echarts.getInstanceByDom(el)
      inst?.resize()
    })
  })
})
</script>

<style scoped>
.stat-cards {
  margin-bottom: 20px;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px;
}
.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.stat-info {
  flex: 1;
}
.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}
.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}
.chart-row {
  margin-bottom: 20px;
}
.chart {
  height: 300px;
  width: 100%;
}
</style>
