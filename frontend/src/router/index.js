import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getRoleHome } from '@/utils/auth'

// 公开路由
const publicRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/login/Register.vue'),
    meta: { title: '注册' }
  },
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue'),
    meta: { title: '页面不存在' }
  }
]

// 患者端路由
const userRoutes = {
  path: '/user',
  component: () => import('@/layouts/UserLayout.vue'),
  meta: { role: 'user' },
  children: [
    { path: 'home', name: 'UserHome', component: () => import('@/views/user/Home.vue'), meta: { title: '首页', icon: 'HomeFilled' } },
    { path: 'chat', name: 'UserChat', component: () => import('@/views/user/chat/AIChat.vue'), meta: { title: 'AI智能问诊', icon: 'ChatDotRound' } },
    { path: 'doctors', name: 'UserDoctors', component: () => import('@/views/user/appointment/DoctorList.vue'), meta: { title: '预约挂号', icon: 'Calendar' } },
    { path: 'appointment', name: 'UserAppointment', component: () => import('@/views/user/appointment/MyAppointments.vue'), meta: { title: '我的预约', icon: 'Document' } },
    { path: 'consult', name: 'UserConsult', component: () => import('@/views/user/consult/MyConsult.vue'), meta: { title: '人工问诊', icon: 'Service' } },
    { path: 'records', name: 'UserRecords', component: () => import('@/views/user/record/MyRecords.vue'), meta: { title: '健康档案', icon: 'Files' } },
    { path: 'articles', name: 'UserArticles', component: () => import('@/views/user/article/ArticleList.vue'), meta: { title: '健康科普', icon: 'Reading' } },
    { path: 'article/:id', name: 'UserArticleDetail', component: () => import('@/views/user/article/ArticleDetail.vue'), meta: { title: '文章详情', hidden: true } },
    { path: 'graph', name: 'UserGraph', component: () => import('@/views/user/graph/GraphExplore.vue'), meta: { title: '知识图谱', icon: 'Share' } },
    { path: 'profile', name: 'UserProfile', component: () => import('@/views/user/profile/Profile.vue'), meta: { title: '个人中心', icon: 'User' } }
  ]
}

// 医生端路由
const doctorRoutes = {
  path: '/doctor',
  component: () => import('@/layouts/DoctorLayout.vue'),
  meta: { role: 'doctor' },
  children: [
    { path: 'dashboard', name: 'DoctorDashboard', component: () => import('@/views/doctor/Dashboard.vue'), meta: { title: '工作台', icon: 'Odometer' } },
    { path: 'appointments', name: 'DoctorAppointments', component: () => import('@/views/doctor/appointment/MyAppointments.vue'), meta: { title: '预约管理', icon: 'Calendar' } },
    { path: 'consults', name: 'DoctorConsults', component: () => import('@/views/doctor/consult/PendingConsult.vue'), meta: { title: '问诊回复', icon: 'ChatDotRound' } },
    { path: 'records', name: 'DoctorRecords', component: () => import('@/views/doctor/record/RecordList.vue'), meta: { title: '健康档案', icon: 'Files' } },
    { path: 'graph', name: 'DoctorGraph', component: () => import('@/views/doctor/graph/GraphInfer.vue'), meta: { title: '知识图谱', icon: 'Share' } },
    { path: 'profile', name: 'DoctorProfile', component: () => import('@/views/doctor/profile/Profile.vue'), meta: { title: '个人中心', icon: 'User' } }
  ]
}

// 管理员端路由
const adminRoutes = {
  path: '/admin',
  component: () => import('@/layouts/AdminLayout.vue'),
  meta: { role: 'admin' },
  children: [
    { path: 'dashboard', name: 'AdminDashboard', component: () => import('@/views/admin/Dashboard.vue'), meta: { title: '数据概览', icon: 'Odometer', group: '数据统计' } },
    { path: 'users', name: 'AdminUsers', component: () => import('@/views/admin/user/UserList.vue'), meta: { title: '用户管理', icon: 'User', group: '用户管理' } },
    { path: 'doctors', name: 'AdminDoctors', component: () => import('@/views/admin/doctor/DoctorList.vue'), meta: { title: '医生管理', icon: 'UserFilled', group: '用户管理' } },
    { path: 'departments', name: 'AdminDepartments', component: () => import('@/views/admin/department/DeptList.vue'), meta: { title: '科室管理', icon: 'OfficeBuilding', group: '用户管理' } },
    { path: 'appointments', name: 'AdminAppointments', component: () => import('@/views/admin/appointment/AppointmentList.vue'), meta: { title: '预约管理', icon: 'Calendar', group: '业务管理' } },
    { path: 'consults', name: 'AdminConsults', component: () => import('@/views/admin/consult/ConsultList.vue'), meta: { title: '问诊管理', icon: 'ChatDotRound', group: '业务管理' } },
    { path: 'chat-records', name: 'AdminChatRecords', component: () => import('@/views/admin/chat/ChatRecords.vue'), meta: { title: 'AI问诊记录', icon: 'Monitor', group: '业务管理' } },
    { path: 'articles', name: 'AdminArticles', component: () => import('@/views/admin/article/ArticleList.vue'), meta: { title: '文章管理', icon: 'Reading', group: '内容管理' } },
    { path: 'notices', name: 'AdminNotices', component: () => import('@/views/admin/notice/NoticeList.vue'), meta: { title: '公告管理', icon: 'Bell', group: '内容管理' } },
    { path: 'knowledge', name: 'AdminKnowledge', component: () => import('@/views/admin/knowledge/KnowledgeList.vue'), meta: { title: '知识库管理', icon: 'Folder', group: 'AI管理' } },
    { path: 'graph', name: 'AdminGraph', component: () => import('@/views/admin/graph/GraphManage.vue'), meta: { title: '图谱管理', icon: 'Share', group: 'AI管理' } },
    { path: 'profile', name: 'AdminProfile', component: () => import('@/views/admin/profile/Profile.vue'), meta: { title: '个人中心', icon: 'Setting', group: '系统设置' } }
  ]
}

const roleRouteMap = {
  user: userRoutes,
  doctor: doctorRoutes,
  admin: adminRoutes
}

const router = createRouter({
  history: createWebHistory(),
  routes: publicRoutes
})

// 动态路由标记
let dynamicRoutesAdded = false

// 添加动态路由
export function addDynamicRoutes(role) {
  const routeConfig = roleRouteMap[role]
  if (routeConfig) {
    router.addRoute(routeConfig)
    // 添加404兜底
    router.addRoute({ path: '/:pathMatch(.*)*', redirect: '/404' })
    dynamicRoutesAdded = true
  }
}

// 重置路由
export function resetRouter() {
  if (dynamicRoutesAdded) {
    // 移除所有角色路由（通过重新创建router实例更干净，这里简化处理）
    window.location.reload()
  }
}

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  const token = userStore.token
  const role = userStore.role

  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - AI智能医疗问诊平台` : 'AI智能医疗问诊平台'

  // 公开页面直接放行
  if (publicRoutes.some(r => to.path.startsWith('/login') || to.path.startsWith('/register') || to.path.startsWith('/404'))) {
    // 已登录用户访问登录页，跳转对应首页
    if (token && (to.path === '/login' || to.path === '/register')) {
      next(getRoleHome(role))
      return
    }
    next()
    return
  }

  // 无token跳转登录
  if (!token) {
    next(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
    return
  }

  // 有token但无用户信息，拉取用户信息
  if (!userStore.userInfo || !userStore.userInfo.user_id) {
    try {
      await userStore.fetchUserInfo()
    } catch (err) {
      userStore.logout()
      next(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
      return
    }
  }

  // 动态路由未添加时，根据角色添加
  if (!dynamicRoutesAdded) {
    addDynamicRoutes(userStore.role)
    next({ ...to, replace: true })
    return
  }

  // 校验角色与路径前缀
  const currentRole = userStore.role
  const rolePrefixMap = {
    user: '/user',
    doctor: '/doctor',
    admin: '/admin'
  }
  const expectedPrefix = rolePrefixMap[currentRole]

  if (expectedPrefix && !to.path.startsWith(expectedPrefix)) {
    // 路径与角色不匹配，跳转对应首页
    next(getRoleHome(currentRole))
    return
  }

  next()
})

export default router
