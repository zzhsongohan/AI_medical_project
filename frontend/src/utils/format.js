import dayjs from 'dayjs'

// 格式化日期
export function formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
  if (!date) return '-'
  return dayjs(date).format(format)
}

// 格式化日期（仅日期）
export function formatDateOnly(date) {
  return formatDate(date, 'YYYY-MM-DD')
}

// 格式化文件大小
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 预约状态映射
export const appointmentStatusMap = {
  0: { label: '待确认', type: 'warning' },
  1: { label: '已确认', type: 'success' },
  2: { label: '已完成', type: 'info' },
  3: { label: '已取消', type: 'danger' }
}

// 问诊状态映射
export const consultStatusMap = {
  0: { label: '待回复', type: 'warning' },
  1: { label: '已回复', type: 'success' },
  2: { label: '已关闭', type: 'info' }
}

// 用户状态映射
export const userStatusMap = {
  0: { label: '禁用', type: 'danger' },
  1: { label: '正常', type: 'success' }
}

// 向量化状态映射
export const vectorStatusMap = {
  0: { label: '待处理', type: 'info' },
  1: { label: '处理中', type: 'warning' },
  2: { label: '已完成', type: 'success' },
  3: { label: '失败', type: 'danger' }
}

// 性别映射
export const genderMap = {
  0: '未知',
  1: '男',
  2: '女'
}
