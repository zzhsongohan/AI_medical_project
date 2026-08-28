<template>
  <el-header class="layout-header">
    <div class="header-left">
      <el-icon class="collapse-btn" @click="toggleSidebar" :size="20">
        <Fold v-if="!collapsed" />
        <Expand v-else />
      </el-icon>
      <el-breadcrumb separator="/" class="breadcrumb">
        <el-breadcrumb-item v-for="item in breadcrumbs" :key="item.path">
          {{ item.title }}
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="header-right">
      <el-dropdown @command="handleCommand">
        <div class="user-info">
          <el-avatar :size="32" :src="userStore.avatar">
            {{ userStore.nickname?.charAt(0) }}
          </el-avatar>
          <span class="username">{{ userStore.nickname }}</span>
          <el-tag :type="roleTagType" size="small" class="role-tag">{{ roleLabel }}</el-tag>
          <el-icon><CaretBottom /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">
              <el-icon><User /></el-icon>个人中心
            </el-dropdown-item>
            <el-dropdown-item divided command="logout">
              <el-icon><SwitchButton /></el-icon>退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </el-header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useAppStore } from '@/stores/app'
import { ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const appStore = useAppStore()

const collapsed = computed(() => appStore.sidebarCollapsed)

function toggleSidebar() {
  appStore.toggleSidebar()
}

const breadcrumbs = computed(() => {
  const items = []
  route.matched.forEach(r => {
    if (r.meta?.title && !r.meta?.hidden) {
      items.push({
        path: r.path,
        title: r.meta.title
      })
    }
  })
  return items
})

const roleLabel = computed(() => {
  const map = { admin: '管理员', doctor: '医生', user: '患者' }
  return map[userStore.role] || '用户'
})

const roleTagType = computed(() => {
  const map = { admin: 'danger', doctor: 'primary', user: 'success' }
  return map[userStore.role] || 'info'
})

function handleCommand(command) {
  if (command === 'profile') {
    const prefixMap = { admin: '/admin', doctor: '/doctor', user: '/user' }
    router.push(`${prefixMap[userStore.role]}/profile`)
  } else if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      userStore.logout()
    }).catch(() => {})
  }
}
</script>

<style scoped>
.layout-header {
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  height: 60px !important;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}
.collapse-btn {
  cursor: pointer;
  color: #606266;
  transition: color 0.3s;
}
.collapse-btn:hover {
  color: #409eff;
}
.breadcrumb {
  font-size: 14px;
}
.header-right {
  display: flex;
  align-items: center;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background 0.3s;
}
.user-info:hover {
  background: #f5f7fa;
}
.username {
  font-size: 14px;
  color: #303133;
}
.role-tag {
  margin-left: 4px;
}
</style>
