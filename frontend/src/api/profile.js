import request from './request'

// 获取个人信息
export function getProfile() {
  return request({
    url: '/profile/info',
    method: 'get'
  })
}

// 更新个人资料
export function updateProfile(data) {
  return request({
    url: '/profile/update',
    method: 'put',
    data
  })
}

// 修改密码
export function changePassword(data) {
  return request({
    url: '/profile/password',
    method: 'put',
    data
  })
}

// 上传头像
export function uploadAvatar(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/profile/avatar',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
