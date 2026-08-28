// 获取token
export function getToken() {
  try {
    const data = JSON.parse(localStorage.getItem('ai-medical-user') || '{}')
    return data.token || ''
  } catch {
    return ''
  }
}

// 获取角色首页路径
export function getRoleHome(role) {
  const homeMap = {
    admin: '/admin/dashboard',
    doctor: '/doctor/dashboard',
    user: '/user/home'
  }
  return homeMap[role] || '/login'
}
