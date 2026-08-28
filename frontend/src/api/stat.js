import request from './request'

// 统计概览（管理员/医生自适应）
export function getStatOverview() {
  return request({
    url: '/stat/overview',
    method: 'get'
  })
}

// 用户个人统计概览
export function getUserOverview() {
  return request({
    url: '/stat/user-overview',
    method: 'get'
  })
}

// 问诊趋势
export function getConsultTrend(days = 7) {
  return request({
    url: '/stat/consult-trend',
    method: 'get',
    params: { days }
  })
}

// 科室预约分布
export function getAppointmentDept() {
  return request({
    url: '/stat/appointment-dept',
    method: 'get'
  })
}

// 用户增长趋势
export function getUserGrowth(days = 7) {
  return request({
    url: '/stat/user-growth',
    method: 'get',
    params: { days }
  })
}

// 知识库文件类型分布
export function getKnowledgeType() {
  return request({
    url: '/stat/knowledge-type',
    method: 'get'
  })
}
