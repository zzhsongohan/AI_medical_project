<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">文章管理</h2>
      <div class="header-actions">
        <el-input v-model="keyword" placeholder="搜索标题" clearable style="width: 240px" @keyup.enter="loadList">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <el-button type="primary" @click="openDialog(null)">
          <el-icon><Plus /></el-icon>新增文章
        </el-button>
      </div>
    </div>
    <PageTable
      :data="list"
      :total="total"
      :loading="loading"
      v-model:page="page"
      v-model:page-size="pageSize"
      @change="loadList"
    >
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
      <el-table-column prop="category" label="分类" width="120" />
      <el-table-column prop="view_count" label="浏览量" width="100" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'info'" size="small">
            {{ row.status === 1 ? '已发布' : '草稿' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="create_time" label="创建时间" width="170" />
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="openDialog(row)">编辑</el-button>
          <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </PageTable>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑文章' : '新增文章'" width="800px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-input v-model="form.category" placeholder="如：健康常识、疾病预防" />
        </el-form-item>
        <el-form-item label="摘要" prop="summary">
          <el-input v-model="form.summary" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <div style="border: 1px solid #dcdfe6; border-radius: 4px;">
            <Toolbar
              style="border-bottom: 1px solid #dcdfe6;"
              :editor="editorRef"
              :default-config="toolbarConfig"
              mode="default"
            />
            <Editor
              v-model="form.content"
              style="height: 350px; overflow-y: hidden;"
              :default-config="editorConfig"
              mode="default"
              @on-created="handleEditorCreated"
            />
          </div>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio :label="1">发布</el-radio>
            <el-radio :label="0">草稿</el-radio>
          </el-radio-group>
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
import { ref, reactive, shallowRef, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import '@wangeditor/editor/dist/css/style.css'
import PageTable from '@/components/PageTable.vue'
import { getAdminArticleList, createArticle, updateArticle, deleteArticle } from '@/api/article'

const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const loading = ref(false)
const keyword = ref('')

const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const submitting = ref(false)
const formRef = ref(null)
const editorRef = shallowRef()

const form = reactive({
  title: '',
  category: '',
  summary: '',
  content: '',
  status: 1
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

const toolbarConfig = { excludeKeys: [] }
const editorConfig = { placeholder: '请输入文章内容...' }

function handleEditorCreated(editor) {
  editorRef.value = editor
}

async function loadList() {
  loading.value = true
  try {
    const data = await getAdminArticleList({
      page: page.value, page_size: pageSize.value,
      keyword: keyword.value || undefined
    })
    list.value = data.items
    total.value = data.total
  } finally { loading.value = false }
}

function openDialog(row) {
  isEdit.value = !!row
  editId.value = row?.id || null
  Object.assign(form, {
    title: row?.title || '',
    category: row?.category || '',
    summary: row?.summary || '',
    content: row?.content || '',
    status: row?.status ?? 1
  })
  dialogVisible.value = true
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    submitting.value = true
    if (isEdit.value) {
      await updateArticle(editId.value, form)
      ElMessage.success('更新成功')
    } else {
      await createArticle(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadList()
  } finally { submitting.value = false }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确定删除文章「${row.title}」吗？`, '提示', { type: 'warning' })
    await deleteArticle(row.id)
    ElMessage.success('删除成功')
    loadList()
  } catch (e) {}
}

onMounted(() => { loadList() })
</script>

<style scoped>
.header-actions { display: flex; gap: 12px; }
</style>
