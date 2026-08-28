import request from './request'

// 公开公告列表
export function getNoticeList() {
  return request({
    url: '/notice/list',
    method: 'get'
  })
}

// 管理员公告列表
export function getAdminNoticeList(params) {
  return request({
    url: '/notice/admin/list',
    method: 'get',
    params
  })
}

// 公告详情
export function getNoticeDetail(noticeId) {
  return request({
    url: `/notice/${noticeId}`,
    method: 'get'
  })
}

// 创建公告
export function createNotice(data) {
  return request({
    url: '/notice/create',
    method: 'post',
    data
  })
}

// 更新公告
export function updateNotice(noticeId, data) {
  return request({
    url: `/notice/${noticeId}`,
    method: 'put',
    data
  })
}

// 删除公告
export function deleteNotice(noticeId) {
  return request({
    url: `/notice/${noticeId}`,
    method: 'delete'
  })
}
