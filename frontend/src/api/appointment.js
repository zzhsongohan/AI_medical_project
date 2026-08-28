import request from './request'

// 创建预约
export function createAppointment(data) {
  return request({
    url: '/appointment/create',
    method: 'post',
    data
  })
}

// 我的预约（患者）
export function getMyAppointments() {
  return request({
    url: '/appointment/my',
    method: 'get'
  })
}

// 医生的预约
export function getDoctorAppointments() {
  return request({
    url: '/appointment/doctor/my',
    method: 'get'
  })
}

// 管理员预约列表
export function getAdminAppointments(params) {
  return request({
    url: '/appointment/admin/list',
    method: 'get',
    params
  })
}

// 管理员删除预约
export function deleteAppointment(apptId) {
  return request({
    url: `/appointment/admin/${apptId}`,
    method: 'delete'
  })
}

// 更新预约状态
export function updateAppointmentStatus(apptId, status) {
  return request({
    url: `/appointment/${apptId}/status`,
    method: 'put',
    params: { status }
  })
}
