import request from './request'

// 我的健康档案（患者）
export function getMyRecords() {
  return request({
    url: '/record/my',
    method: 'get'
  })
}

// 医生查看患者档案
export function getDoctorPatientRecords() {
  return request({
    url: '/record/doctor/patients',
    method: 'get'
  })
}

// 可选患者列表
export function getPatientOptions() {
  return request({
    url: '/record/doctor/patient-options',
    method: 'get'
  })
}

// 医生创建档案
export function createRecord(data) {
  return request({
    url: '/record/doctor/create',
    method: 'post',
    data
  })
}

// 医生更新档案
export function updateRecord(recordId, data) {
  return request({
    url: `/record/doctor/${recordId}`,
    method: 'put',
    data
  })
}

// 医生删除档案
export function deleteRecord(recordId) {
  return request({
    url: `/record/doctor/${recordId}`,
    method: 'delete'
  })
}
