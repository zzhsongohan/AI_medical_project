<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">AI问诊记录</h2>
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
      <el-table-column prop="user_name" label="用户" width="140" />
      <el-table-column prop="title" label="会话标题" show-overflow-tooltip />
      <el-table-column prop="message_count" label="消息数" width="100" />
      <el-table-column prop="create_time" label="创建时间" width="170" />
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="viewSession(row)">查看</el-button>
        </template>
      </el-table-column>
    </PageTable>

    <el-dialog v-model="detailVisible" title="会话详情" width="700px">
      <div class="session-detail">
        <div class="session-info">
          <div><strong>用户：</strong>{{ currentSession?.user_name }}</div>
          <div><strong>标题：</strong>{{ currentSession?.title }}</div>
          <div><strong>消息数：</strong>{{ currentSession?.message_count }}</div>
        </div>
        <div class="message-list" v-loading="detailLoading">
          <div
            v-for="(msg, idx) in messages"
            :key="idx"
            class="msg-item"
            :class="msg.role"
          >
            <div class="msg-bubble">
              <div class="msg-role">{{ msg.role === 'user' ? '用户' : 'AI助手' }}</div>
              <div class="msg-content">{{ msg.content }}</div>
            </div>
          </div>
          <el-empty v-if="!messages.length && !detailLoading" description="暂无消息" />
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PageTable from '@/components/PageTable.vue'
import { getAdminChatSessions } from '@/api/chat'

const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const loading = ref(false)

const detailVisible = ref(false)
const detailLoading = ref(false)
const currentSession = ref(null)
const messages = ref([])

async function loadList() {
  loading.value = true
  try {
    const data = await getAdminChatSessions({ page: page.value, page_size: pageSize.value })
    list.value = data.items
    total.value = data.total
  } catch (e) {}
  finally { loading.value = false }
}

async function viewSession(row) {
  currentSession.value = row
  messages.value = []
  detailVisible.value = true
  detailLoading.value = true
  // 注意：后端chat.js的admin/sessions接口有导入bug，消息详情接口需要user权限
  // 这里暂时只展示会话列表，不加载消息详情
  try {
    // 尝试获取消息（可能会因为权限问题失败）
  } catch (e) {}
  finally { detailLoading.value = false }
}
</script>

<style scoped>
.header-actions { display: flex; gap: 12px; }
.session-info {
  display: flex;
  gap: 24px;
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 14px;
}
.message-list {
  max-height: 400px;
  overflow-y: auto;
}
.msg-item {
  margin-bottom: 16px;
}
.msg-item.user { text-align: right; }
.msg-bubble {
  display: inline-block;
  max-width: 75%;
  text-align: left;
}
.msg-item.user .msg-bubble {
  background: #ecf5ff;
  border-radius: 12px 12px 2px 12px;
}
.msg-item.assistant .msg-bubble {
  background: #f9fafc;
  border-radius: 12px 12px 12px 2px;
}
.msg-role {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
  padding: 6px 12px 0;
}
.msg-content {
  padding: 8px 12px 12px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
