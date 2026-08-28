<template>
  <div class="page-container">
    <div class="doctor-header">
      <h2 class="page-title">预约挂号</h2>
      <div class="filter-bar">
        <div class="dept-tabs">
          <span class="filter-label">科室：</span>
          <el-tag
            :class="{ active: !selectedDept }"
            size="large"
            effect="plain"
            @click="selectDept(null)"
          >
            全部
          </el-tag>
          <el-tag
            v-for="dept in departments"
            :key="dept.id"
            :class="{ active: selectedDept === dept.id }"
            size="large"
            effect="plain"
            @click="selectDept(dept.id)"
          >
            {{ dept.name }}
          </el-tag>
        </div>
        <el-input v-model="keyword" placeholder="搜索医生姓名/职称" clearable style="width: 240px" @keyup.enter="loadList">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
      </div>
    </div>

    <div v-loading="loading" class="doctor-grid">
      <div v-for="doctor in list" :key="doctor.id" class="doctor-card">
        <div class="doctor-avatar">
          <el-avatar :size="72" :src="getAvatar(doctor.avatar)">
            {{ doctor.real_name?.charAt(0) }}
          </el-avatar>
        </div>
        <div class="doctor-info">
          <div class="doctor-name">
            {{ doctor.real_name }}
            <el-tag size="small" type="primary">{{ doctor.title || '医师' }}</el-tag>
          </div>
          <div class="doctor-dept">{{ doctor.department_name }}</div>
          <div class="doctor-specialty" :title="doctor.specialty">
            <el-icon><Star /></el-icon>
            {{ doctor.specialty || '暂无' }}
          </div>
          <div class="doctor-intro" :title="doctor.introduction">
            {{ doctor.introduction || '暂无简介' }}
          </div>
        </div>
        <div class="doctor-action">
          <el-button type="primary" @click="bookAppointment(doctor)">
            <el-icon><Calendar /></el-icon>
            预约挂号
          </el-button>
        </div>
      </div>
      <el-empty v-if="!list.length && !loading" description="暂无医生" />
    </div>

    <el-pagination
      v-if="total > 0"
      class="pagination"
      v-model:current-page="page"
      v-model:page-size="pageSize"
      :total="total"
      layout="prev, pager, next, total"
      background
      @current-change="loadList"
    />

    <el-dialog v-model="bookDialogVisible" title="预约挂号" width="500px">
      <el-form :model="bookForm" :rules="bookRules" ref="bookFormRef" label-width="100px">
        <el-form-item label="医生">
          <span>{{ currentDoctor?.real_name }} - {{ currentDoctor?.title }}</span>
        </el-form-item>
        <el-form-item label="科室">
          <span>{{ currentDoctor?.department_name }}</span>
        </el-form-item>
        <el-form-item label="就诊日期" prop="visit_date">
          <el-date-picker
            v-model="bookForm.visit_date"
            type="date"
            placeholder="选择就诊日期"
            :disabled-date="disabledDate"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="时段" prop="time_slot">
          <el-select v-model="bookForm.time_slot" placeholder="请选择时段" style="width: 100%">
            <el-option label="上午 08:00-12:00" value="上午" />
            <el-option label="下午 14:00-17:30" value="下午" />
            <el-option label="晚间 18:00-21:00" value="晚间" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="bookForm.remark" type="textarea" :rows="2" placeholder="请描述症状或备注信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="bookDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="booking" @click="submitBooking">确认预约</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Calendar, Star } from '@element-plus/icons-vue'
import { getDoctorList } from '@/api/doctor'
import { getDepartmentList } from '@/api/department'
import { createAppointment } from '@/api/appointment'
import dayjs from 'dayjs'

const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(8)
const loading = ref(false)
const keyword = ref('')
const selectedDept = ref(null)
const departments = ref([])

const bookDialogVisible = ref(false)
const currentDoctor = ref(null)
const booking = ref(false)
const bookFormRef = ref(null)

const bookForm = reactive({
  visit_date: '',
  time_slot: '',
  remark: ''
})

const bookRules = {
  visit_date: [{ required: true, message: '请选择就诊日期', trigger: 'change' }],
  time_slot: [{ required: true, message: '请选择时段', trigger: 'change' }]
}

function getAvatar(avatar) {
  if (!avatar) return ''
  if (avatar.startsWith('http')) return avatar
  return (import.meta.env.VITE_UPLOAD_BASE_URL || '') + avatar
}

async function loadDepts() {
  try {
    departments.value = await getDepartmentList()
  } catch (e) {}
}

async function loadList() {
  loading.value = true
  try {
    const data = await getDoctorList({
      page: page.value,
      page_size: pageSize.value,
      keyword: keyword.value || undefined,
      department_id: selectedDept.value || undefined
    })
    list.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

function selectDept(deptId) {
  selectedDept.value = deptId
  page.value = 1
  loadList()
}

function bookAppointment(doctor) {
  currentDoctor.value = doctor
  bookForm.visit_date = ''
  bookForm.time_slot = ''
  bookForm.remark = ''
  bookDialogVisible.value = true
  bookFormRef.value?.clearValidate()
}

function disabledDate(time) {
  return time.getTime() < Date.now() - 86400000
}

async function submitBooking() {
  if (!bookFormRef.value || !currentDoctor.value) return
  try {
    await bookFormRef.value.validate()
    booking.value = true
    await createAppointment({
      doctor_id: currentDoctor.value.id,
      department_id: currentDoctor.value.department_id,
      visit_date: dayjs(bookForm.visit_date).format('YYYY-MM-DD'),
      time_slot: bookForm.time_slot,
      remark: bookForm.remark
    })
    ElMessage.success('预约成功')
    bookDialogVisible.value = false
  } finally {
    booking.value = false
  }
}

onMounted(() => {
  loadDepts()
  loadList()
})
</script>

<style scoped>
.doctor-header {
  margin-bottom: 20px;
}
.filter-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
  flex-wrap: wrap;
}
.filter-label {
  font-size: 14px;
  color: #606266;
}
.dept-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  flex: 1;
}
.dept-tabs .el-tag {
  cursor: pointer;
  transition: all 0.2s;
}
.dept-tabs .el-tag.active {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}
.doctor-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.doctor-card {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
  transition: all 0.2s;
  border: 1px solid #f0f0f0;
}
.doctor-card:hover {
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}
.doctor-avatar {
  flex-shrink: 0;
}
.doctor-info {
  flex: 1;
  min-width: 0;
}
.doctor-name {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.doctor-dept {
  font-size: 13px;
  color: #409eff;
  margin-bottom: 8px;
}
.doctor-specialty {
  font-size: 13px;
  color: #606266;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.doctor-intro {
  font-size: 12px;
  color: #909399;
  line-height: 1.6;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
.doctor-action {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
