import request from './request'

// 知识库文件列表
export function getKnowledgeList(params) {
  return request({
    url: '/knowledge/list',
    method: 'get',
    params
  })
}

// 上传文件
export function uploadKnowledgeFile(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/knowledge/upload',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 重新向量化
export function revectorizeFile(fileId) {
  return request({
    url: `/knowledge/${fileId}/revectorize`,
    method: 'post'
  })
}

// 删除文件
export function deleteKnowledgeFile(fileId) {
  return request({
    url: `/knowledge/${fileId}`,
    method: 'delete'
  })
}
