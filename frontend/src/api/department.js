import request from './request'

// 公开科室列表
export function getDepartmentList() {
  return request({
    url: '/department/list',
    method: 'get'
  })
}

// 管理员科室列表
export function getAdminDeptList(params) {
  return request({
    url: '/department/admin/list',
    method: 'get',
    params
  })
}

// 创建科室
export function createDepartment(data) {
  return request({
    url: '/department/create',
    method: 'post',
    data
  })
}

// 更新科室
export function updateDepartment(deptId, data) {
  return request({
    url: `/department/${deptId}`,
    method: 'put',
    data
  })
}

// 删除科室
export function deleteDepartment(deptId) {
  return request({
    url: `/department/${deptId}`,
    method: 'delete'
  })
}
