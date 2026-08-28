import request from './request'

// 症状推理疾病
export function inferDisease(symptoms) {
  return request({
    url: '/graph/infer',
    method: 'post',
    data: { symptoms }
  })
}

// 疾病详情
export function getDiseaseDetail(name) {
  return request({
    url: `/graph/disease/${encodeURIComponent(name)}`,
    method: 'get'
  })
}

// 完整知识图谱
export function getFullGraph() {
  return request({
    url: '/graph/full',
    method: 'get'
  })
}

// 实体子图
export function getSubgraph(entity) {
  return request({
    url: '/graph/subgraph',
    method: 'get',
    params: { entity }
  })
}

// 搜索图谱实体
export function searchGraph(keyword) {
  return request({
    url: '/graph/search',
    method: 'get',
    params: { keyword }
  })
}

// 图谱统计
export function getGraphStats() {
  return request({
    url: '/graph/stats',
    method: 'get'
  })
}
