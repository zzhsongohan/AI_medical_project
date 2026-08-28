<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">健康档案</h2>
    </div>

    <div v-loading="loading" class="record-list">
      <div v-for="item in list" :key="item.id" class="record-card">
        <div class="record-header">
          <div class="record-type">
            <el-icon><Document /></el-icon>
            {{ item.record_type || '门诊记录' }}
          </div>
          <div class="record-date">
            <el-icon><Calendar /></el-icon>
            {{ item.visit_date || item.create_time }}
          </div>
        </div>
        <div class="record-doctor" v-if="item.doctor_name">
          医生：{{ item.doctor_name }}
        </div>
        <div class="record-item-row" v-if="item.diagnosis">
          <span class="label">诊断：</span>
          <span class="value">{{ item.diagnosis }}</span>
        </div>
        <div class="record-item-row" v-if="item.treatment">
          <span class="label">治疗方案：</span>
          <span class="value">{{ item.treatment }}</span>
        </div>
        <div class="record-item-row" v-if="item.prescription">
          <span class="label">处方：</span>
          <span class="value">{{ item.prescription }}</span>
        </div>
      </div>
      <el-empty v-if="!list.length && !loading" description="暂无健康档案" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Document, Calendar } from '@element-plus/icons-vue'
import { getMyRecords } from '@/api/record'

const list = ref([])
const loading = ref(false)

async function loadList() {
  loading.value = true
  try {
    list.value = await getMyRecords()
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadList()
})
</script>

<style scoped>
.record-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.record-card {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
  border: 1px solid #f0f0f0;
}
.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.record-type {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 16px;
  font-weight: 600;
  color: #409eff;
}
.record-date {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #909399;
}
.record-doctor {
  color: #606266;
  font-size: 14px;
  margin-bottom: 10px;
}
.record-item-row {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  line-height: 1.6;
}
.record-item-row .label {
  color: #909399;
  flex-shrink: 0;
}
.record-item-row .value {
  color: #303133;
  flex: 1;
}
</style>
