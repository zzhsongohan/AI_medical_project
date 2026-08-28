import request from './request'

// 公开文章列表
export function getArticleList(params) {
  return request({
    url: '/article/list',
    method: 'get',
    params
  })
}

// 管理员文章列表
export function getAdminArticleList(params) {
  return request({
    url: '/article/admin/list',
    method: 'get',
    params
  })
}

// 文章详情
export function getArticleDetail(articleId) {
  return request({
    url: `/article/${articleId}`,
    method: 'get'
  })
}

// 创建文章
export function createArticle(data) {
  return request({
    url: '/article/create',
    method: 'post',
    data
  })
}

// 更新文章
export function updateArticle(articleId, data) {
  return request({
    url: `/article/${articleId}`,
    method: 'put',
    data
  })
}

// 删除文章
export function deleteArticle(articleId) {
  return request({
    url: `/article/${articleId}`,
    method: 'delete'
  })
}
