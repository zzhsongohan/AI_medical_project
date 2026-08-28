import request from './request'

// 会话列表
export function getChatSessions() {
  return request({
    url: '/chat/sessions',
    method: 'get'
  })
}

// 会话消息详情
export function getChatMessages(sessionId) {
  return request({
    url: `/chat/sessions/${sessionId}/messages`,
    method: 'get'
  })
}

// 管理员查看所有会话
export function getAdminChatSessions(params) {
  return request({
    url: '/chat/admin/sessions',
    method: 'get',
    params
  })
}

// SSE发送消息 - 使用 fetch + ReadableStream
export function sendChatMessage({ sessionId, message, onSession, onContent, onDone, onError }) {
  const token = localStorage.getItem('ai-medical-user') ? JSON.parse(localStorage.getItem('ai-medical-user')).token : ''
  const baseUrl = import.meta.env.VITE_API_BASE_URL

  const abortController = new AbortController()

  fetch(`${baseUrl}/chat/send`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ session_id: sessionId, message }),
    signal: abortController.signal
  }).then(response => {
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    function read() {
      reader.read().then(({ value, done }) => {
        if (done) return

        buffer += decoder.decode(value, { stream: true })
        const events = buffer.split('\n\n')
        buffer = events.pop()

        for (const event of events) {
          if (!event.trim()) continue
          const dataLine = event.replace(/^data:\s*/, '').trim()
          if (!dataLine) continue

          try {
            const data = JSON.parse(dataLine)
            switch (data.type) {
              case 'session':
                onSession?.(data.session_id)
                break
              case 'content':
                onContent?.(data.content)
                break
              case 'done':
                onDone?.(data.references || [], data.graph || [])
                break
              case 'error':
                onError?.(data.message)
                break
            }
          } catch (e) {
            console.warn('SSE parse error:', e)
          }
        }

        read()
      }).catch(err => {
        if (err.name !== 'AbortError') {
          onError?.(err.message)
        }
      })
    }

    read()
  }).catch(err => {
    if (err.name !== 'AbortError') {
      onError?.(err.message)
    }
  })

  return {
    abort: () => abortController.abort()
  }
}
