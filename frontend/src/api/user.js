import request from './request'

// 用户列表
export function getUserList(params) {
  return request({
    url: '/user/list',
    method: 'get',
    params
  })
}

// 创建用户
export function createUser(data) {
  return request({
    url: '/user/create',
    method: 'post',
    data
  })
}

// 更新用户
export function updateUser(userId, data) {
  return request({
    url: `/user/${userId}`,
    method: 'put',
    data
  })
}

// 删除用户
export function deleteUser(userId) {
  return request({
    url: `/user/${userId}`,
    method: 'delete'
  })
}

// 切换用户状态
export function changeUserStatus(userId, status) {
  return request({
    url: `/user/${userId}/status`,
    method: 'put',
    params: { status }
  })
}
