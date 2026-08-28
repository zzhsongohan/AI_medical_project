import { defineStore } from 'pinia'
import { login as loginApi, register as registerApi } from '@/api/auth'
import { getProfile } from '@/api/profile'
import router from '@/router'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: '',
    userInfo: null,
    role: ''
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    nickname: (state) => state.userInfo?.nickname || state.userInfo?.username || '用户',
    avatar: (state) => {
      const avatar = state.userInfo?.avatar
      if (!avatar) return ''
      if (avatar.startsWith('http')) return avatar
      return (import.meta.env.VITE_UPLOAD_BASE_URL || '') + avatar
    }
  },

  actions: {
    // 登录
    async login(loginForm) {
      const data = await loginApi(loginForm)
      this.token = data.access_token
      this.role = data.role
      this.userInfo = {
        user_id: data.user_id,
        username: data.username,
        nickname: data.nickname,
        avatar: data.avatar,
        role: data.role
      }
      return data
    },

    // 注册
    async register(registerForm) {
      const data = await registerApi(registerForm)
      this.token = data.access_token
      this.role = data.role
      this.userInfo = {
        user_id: data.user_id,
        username: data.username,
        nickname: data.nickname,
        avatar: data.avatar,
        role: data.role
      }
      return data
    },

    // 获取用户信息
    async fetchUserInfo() {
      const data = await getProfile()
      this.userInfo = data
      this.role = data.role
      return data
    },

    // 更新用户信息
    updateUserInfo(data) {
      this.userInfo = { ...this.userInfo, ...data }
    },

    // 登出
    logout() {
      this.token = ''
      this.userInfo = null
      this.role = ''
      router.push('/login')
    }
  },

  persist: {
    key: 'ai-medical-user',
    paths: ['token', 'role', 'userInfo']
  }
})
