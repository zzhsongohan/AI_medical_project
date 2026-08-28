<template>
  <div class="chat-container">
    <div class="chat-sidebar">
      <div class="sidebar-header">
        <el-button type="primary" class="new-chat-btn" @click="createNewSession">
          <el-icon><Plus /></el-icon>
          新建问诊
        </el-button>
      </div>
      <div class="session-list" v-loading="loadingSessions">
        <div
          v-for="session in sessions"
          :key="session.id"
          class="session-item"
          :class="{ active: currentSessionId === session.id }"
          @click="selectSession(session.id)"
        >
          <el-icon><ChatDotRound /></el-icon>
          <span class="session-title">{{ session.title }}</span>
        </div>
        <el-empty v-if="!sessions.length && !loadingSessions" description="暂无问诊记录" />
      </div>
    </div>

    <div class="chat-main">
      <div class="chat-header">
        <span v-if="currentSessionId">{{ currentTitle }}</span>
        <span v-else class="header-tip">开始新的AI问诊</span>
      </div>

      <div class="chat-messages" ref="messagesRef">
        <div v-if="!messages.length" class="welcome-tip">
          <el-icon :size="48" color="#409eff"><FirstAidKit /></el-icon>
          <h3>AI智能问诊助手</h3>
          <p>您好，我是AI医疗助手，请描述您的症状，我将为您提供专业的健康建议。</p>
          <div class="quick-symptoms">
            <el-tag
              v-for="symptom in quickSymptoms"
              :key="symptom"
              size="large"
              class="symptom-tag"
              @click="sendQuickSymptom(symptom)"
            >
              {{ symptom }}
            </el-tag>
          </div>
        </div>

        <div
          v-for="(msg, index) in messages"
          :key="index"
          class="message-item"
          :class="msg.role"
        >
          <div class="message-avatar">
            <el-avatar v-if="msg.role === 'user'" :size="36" :src="userStore.avatar">
              {{ userStore.nickname?.charAt(0) }}
            </el-avatar>
            <el-avatar v-else :size="36" style="background: linear-gradient(135deg, #667eea, #764ba2)">
              <el-icon :size="20"><FirstAidKit /></el-icon>
            </el-avatar>
          </div>
          <div class="message-bubble">
            <div class="message-content" v-html="formatMessage(msg.content)"></div>
            <div v-if="msg.role === 'assistant' && msg.references && msg.references.length" class="message-refs">
              <div class="refs-title">
                <el-icon><Document /></el-icon>
                引用来源
              </div>
              <div class="ref-list">
                <div v-for="(ref, ri) in msg.references" :key="ri" class="ref-item">
                  [{{ ri + 1 }}] {{ ref.source || ref.file_name || '未知来源' }}
                </div>
              </div>
            </div>
            <div v-if="msg.role === 'assistant' && msg.graph && msg.graph.length" class="message-graph">
              <div class="graph-title">
                <el-icon><Share /></el-icon>
                知识图谱关联
              </div>
              <div class="graph-tags">
                <el-tag v-for="(g, gi) in msg.graph" :key="gi" size="small" type="info" effect="plain">
                  {{ g.name || g }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>

        <div v-if="isStreaming" class="message-item assistant">
          <div class="message-avatar">
            <el-avatar :size="36" style="background: linear-gradient(135deg, #667eea, #764ba2)">
              <el-icon :size="20"><FirstAidKit /></el-icon>
            </el-avatar>
          </div>
          <div class="message-bubble">
            <div class="message-content streaming">
              {{ streamingContent }}<span class="cursor">▌</span>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-input-area">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="2"
          placeholder="请描述您的症状，按 Enter 发送，Shift+Enter 换行"
          :disabled="isStreaming"
          @keydown="handleKeydown"
          resize="none"
        />
        <el-button
          type="primary"
          :icon="Promotion"
          :loading="isStreaming"
          @click="sendMessage"
          class="send-btn"
        >
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { getChatSessions, getChatMessages, sendChatMessage } from '@/api/chat'
import { Plus, ChatDotRound, FirstAidKit, Document, Share, Promotion } from '@element-plus/icons-vue'
import { marked } from 'marked'

const userStore = useUserStore()

const sessions = ref([])
const currentSessionId = ref(null)
const messages = ref([])
const inputMessage = ref('')
const isStreaming = ref(false)
const streamingContent = ref('')
const loadingSessions = ref(false)
const messagesRef = ref(null)

const quickSymptoms = ['头痛', '发烧咳嗽', '胃痛', '失眠', '皮肤过敏', '腰痛']

const currentTitle = computed(() => {
  const s = sessions.value.find(s => s.id === currentSessionId.value)
  return s?.title || '新问诊'
})

function formatMessage(content) {
  if (!content) return ''
  return marked.parse(content)
}

async function scrollToBottom() {
  await nextTick()
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}

async function loadSessions() {
  loadingSessions.value = true
  try {
    sessions.value = await getChatSessions()
  } catch (e) {}
  finally {
    loadingSessions.value = false
  }
}

async function selectSession(sessionId) {
  if (isStreaming.value) return
  currentSessionId.value = sessionId
  messages.value = []
  try {
    const msgs = await getChatMessages(sessionId)
    messages.value = msgs.map(m => ({
      role: m.role,
      content: m.content,
      references: m.references_json ? JSON.parse(m.references_json) : null,
      graph: m.graph_json ? JSON.parse(m.graph_json) : null
    }))
  } catch (e) {}
  scrollToBottom()
}

function createNewSession() {
  if (isStreaming.value) return
  currentSessionId.value = null
  messages.value = []
}

function sendQuickSymptom(symptom) {
  inputMessage.value = `我最近${symptom}，可能是什么原因？`
  sendMessage()
}

function handleKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

async function sendMessage() {
  const text = inputMessage.value.trim()
  if (!text || isStreaming.value) return

  // 添加用户消息
  messages.value.push({ role: 'user', content: text })
  inputMessage.value = ''
  isStreaming.value = true
  streamingContent.value = ''
  scrollToBottom()

  const assistantMsg = { role: 'assistant', content: '', references: null, graph: null }

  sendChatMessage({
    sessionId: currentSessionId.value,
    message: text,
    onSession: (sessionId) => {
      currentSessionId.value = sessionId
      loadSessions()
    },
    onContent: (chunk) => {
      streamingContent.value += chunk
      scrollToBottom()
    },
    onDone: (references, graph) => {
      assistantMsg.content = streamingContent.value
      assistantMsg.references = references
      assistantMsg.graph = graph
      messages.value.push(assistantMsg)
      isStreaming.value = false
      streamingContent.value = ''
      scrollToBottom()
    },
    onError: (errMsg) => {
      assistantMsg.content = '抱歉，出现了错误：' + errMsg
      messages.value.push(assistantMsg)
      isStreaming.value = false
      streamingContent.value = ''
      scrollToBottom()
    }
  })
}

onMounted(() => {
  loadSessions()
})
</script>

<style scoped>
.chat-container {
  display: flex;
  height: calc(100vh - 60px);
  background: #f5f7fa;
}
.chat-sidebar {
  width: 260px;
  background: #fff;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}
.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #e4e7ed;
}
.new-chat-btn {
  width: 100%;
}
.session-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}
.session-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 4px;
}
.session-item:hover {
  background: #f5f7fa;
}
.session-item.active {
  background: #ecf5ff;
  color: #409eff;
}
.session-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
}
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
}
.chat-header {
  height: 56px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid #e4e7ed;
  font-size: 16px;
  font-weight: 500;
}
.header-tip {
  color: #909399;
  font-size: 14px;
  font-weight: normal;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f9fafc;
}
.welcome-tip {
  text-align: center;
  padding: 60px 20px;
  color: #606266;
}
.welcome-tip h3 {
  margin: 16px 0 8px;
  font-size: 20px;
}
.welcome-tip p {
  color: #909399;
  margin-bottom: 24px;
}
.quick-symptoms {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  max-width: 500px;
  margin: 0 auto;
}
.symptom-tag {
  cursor: pointer;
  transition: all 0.2s;
}
.symptom-tag:hover {
  transform: translateY(-1px);
}
.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}
.message-item.user {
  flex-direction: row-reverse;
}
.message-avatar {
  flex-shrink: 0;
}
.message-bubble {
  max-width: 70%;
  background: #fff;
  border-radius: 12px;
  padding: 12px 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #eef0f3;
}
.message-item.user .message-bubble {
  background: #ecf5ff;
  border-color: #d9ecff;
}
.message-content {
  line-height: 1.7;
  font-size: 14px;
  word-wrap: break-word;
}
.message-content :deep(p) {
  margin: 0 0 8px;
}
.message-content :deep(p:last-child) {
  margin-bottom: 0;
}
.message-content :deep(ul),
.message-content :deep(ol) {
  margin: 8px 0;
  padding-left: 20px;
}
.message-content.streaming {
  min-height: 20px;
}
.cursor {
  animation: blink 1s infinite;
  color: #409eff;
}
@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}
.message-refs, .message-graph {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
  font-size: 12px;
}
.refs-title, .graph-title {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #606266;
  font-weight: 500;
  margin-bottom: 8px;
}
.ref-item {
  color: #909399;
  padding: 4px 0;
  font-size: 12px;
}
.graph-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.chat-input-area {
  padding: 16px 20px;
  border-top: 1px solid #e4e7ed;
  background: #fff;
  display: flex;
  gap: 12px;
  align-items: flex-end;
}
.chat-input-area :deep(.el-textarea__inner) {
  resize: none;
}
.send-btn {
  height: 40px;
  padding: 0 20px;
}
</style>
