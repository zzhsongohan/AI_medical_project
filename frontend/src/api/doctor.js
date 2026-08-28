import request from './request'

// 公开医生列表
export function getDoctorList(params) {
  return request({
    url: '/doctor/list',
    method: 'get',
    params
  })
}

// 管理员医生列表
export function getAdminDoctorList(params) {
  return request({
    url: '/doctor/admin/list',
    method: 'get',
    params
  })
}

// 创建医生
export function createDoctor(data) {
  return request({
    url: '/doctor/create',
    method: 'post',
    data
  })
}

// 更新医生
export function updateDoctor(doctorId, data) {
  return request({
    url: `/doctor/${doctorId}`,
    method: 'put',
    data
  })
}

// 删除医生
export function deleteDoctor(doctorId) {
  return request({
    url: `/doctor/${doctorId}`,
    method: 'delete'
  })
}

// 切换医生状态
export function changeDoctorStatus(doctorId, status) {
  return request({
    url: `/doctor/${doctorId}/status`,
    method: 'put',
    params: { status }
  })
}
