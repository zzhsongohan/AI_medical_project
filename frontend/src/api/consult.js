import request from './request'

// 患者发起人工问诊
export function createConsult(data) {
  return request({
    url: '/consult/create',
    method: 'post',
    data
  })
}

// 患者查看自己的问诊
export function getMyConsults() {
  return request({
    url: '/consult/my',
    method: 'get'
  })
}

// 医生待回复列表
export function getDoctorPendingConsults() {
  return request({
    url: '/consult/doctor/pending',
    method: 'get'
  })
}

// 医生回复
export function replyConsult(data) {
  return request({
    url: '/consult/reply',
    method: 'post',
    data
  })
}

// 管理员列表
export function getAdminConsults(params) {
  return request({
    url: '/consult/admin/list',
    method: 'get',
    params
  })
}

// 管理员删除咨询工单
export function deleteConsult(consultId) {
  return request({
    url: `/consult/admin/${consultId}`,
    method: 'delete'
  })
}
