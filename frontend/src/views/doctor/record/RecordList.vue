<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">患者档案</h2>
      <div class="header-actions">
        <el-select v-model="patientFilter" placeholder="按患者筛选" clearable style="width: 200px" @change="loadList">
          <el-option
            v-for="p in patientOptions"
            :key="p.id"
            :label="p.name"
            :value="p.id"
          />
        </el-select>
        <el-button type="primary" @click="openDialog(null)">
          <el-icon><Plus /></el-icon>新建档案
        </el-button>
      </div>
    </div>

    <el-table v-loading="loading" :data="filteredList" border stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="patient_name" label="患者" width="120" />
      <el-table-column prop="record_type" label="类型" width="120" />
      <el-table-column prop="diagnosis" label="诊断" show-overflow-tooltip />
      <el-table-column prop="visit_date" label="就诊日期" width="130" />
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="openDialog(row)">编辑</el-button>
          <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑档案' : '新建档案'" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="选择患者" prop="user_id" v-if="!isEdit">
          <el-select v-model="form.user_id" placeholder="请选择患者" style="width: 100%">
            <el-option
              v-for="p in patientOptions"
              :key="p.id"
              :label="p.name"
              :value="p.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="档案类型" prop="record_type">
          <el-input v-model="form.record_type" placeholder="如：门诊记录、住院记录等" />
        </el-form-item>
        <el-form-item label="诊断" prop="diagnosis">
          <el-input v-model="form.diagnosis" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="治疗方案" prop="treatment">
          <el-input v-model="form.treatment" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="处方" prop="prescription">
          <el-input v-model="form.prescription" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="就诊日期" prop="visit_date">
          <el-date-picker v-model="form.visit_date" type="date" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getDoctorPatientRecords, getPatientOptions, createRecord, updateRecord, deleteRecord } from '@/api/record'
import dayjs from 'dayjs'

const list = ref([])
const loading = ref(false)
const patientOptions = ref([])
const patientFilter = ref(null)

const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const submitting = ref(false)
const formRef = ref(null)

const form = reactive({
  user_id: null,
  record_type: '',
  diagnosis: '',
  treatment: '',
  prescription: '',
  visit_date: ''
})

const rules = {
  user_id: [{ required: true, message: '请选择患者', trigger: 'change' }],
  record_type: [{ required: true, message: '请输入档案类型', trigger: 'blur' }],
  diagnosis: [{ required: true, message: '请输入诊断', trigger: 'blur' }]
}

const filteredList = computed(() => {
  if (!patientFilter.value) return list.value
  return list.value.filter(item => item.user_id === patientFilter.value)
})

async function loadPatients() {
  try {
    patientOptions.value = await getPatientOptions()
  } catch (e) {}
}

async function loadList() {
  loading.value = true
  try {
    list.value = await getDoctorPatientRecords()
  } finally {
    loading.value = false
  }
}

function openDialog(row) {
  isEdit.value = !!row
  editId.value = row?.id || null
  Object.assign(form, {
    user_id: row?.user_id || null,
    record_type: row?.record_type || '',
    diagnosis: row?.diagnosis || '',
    treatment: row?.treatment || '',
    prescription: row?.prescription || '',
    visit_date: row?.visit_date ? dayjs(row.visit_date).toDate() : ''
  })
  dialogVisible.value = true
  formRef.value?.clearValidate()
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    submitting.value = true
    const data = {
      ...form,
      visit_date: form.visit_date ? dayjs(form.visit_date).format('YYYY-MM-DD') : ''
    }
    if (isEdit.value) {
      await updateRecord(editId.value, data)
      ElMessage.success('更新成功')
    } else {
      await createRecord(data)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadList()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm('确定删除该档案吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteRecord(row.id)
    ElMessage.success('删除成功')
    loadList()
  } catch (e) {}
}

onMounted(() => {
  loadPatients()
  loadList()
})
</script>

<style scoped>
.header-actions {
  display: flex;
  gap: 12px;
}
</style>
