<template>
  <el-aside :width="collapsed ? '64px' : '220px'" class="sidebar">
    <div class="logo" :class="{ collapsed }">
      <el-icon :size="24" color="#fff"><FirstAidKit /></el-icon>
      <span v-if="!collapsed" class="logo-text">医疗问诊平台</span>
    </div>
    <el-menu
      :default-active="activeMenu"
      :collapse="collapsed"
      :collapse-transition="false"
      router
      background-color="#001529"
      text-color="#b7c3cf"
      active-text-color="#409eff"
    >
      <template v-for="(group, gIndex) in menuGroups" :key="gIndex">
        <el-menu-item v-if="showGroupTitle(gIndex)" class="menu-group-title" disabled>
          <span>{{ group.name }}</span>
        </el-menu-item>
        <el-menu-item
          v-for="item in group.items"
          :key="item.path"
          :index="item.path"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <template #title>{{ item.title }}</template>
        </el-menu-item>
      </template>
    </el-menu>
  </el-aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'

const props = defineProps({
  role: {
    type: String,
    required: true
  }
})

const route = useRoute()
const appStore = useAppStore()

const collapsed = computed(() => appStore.sidebarCollapsed)
const activeMenu = computed(() => route.path)

// 按分组组织菜单
const menuGroups = computed(() => {
  const routes = route.matched[0]?.children || []
  const groups = {}
  routes.forEach(r => {
    if (r.meta?.hidden) return
    const groupName = r.meta?.group || '菜单'
    if (!groups[groupName]) {
      groups[groupName] = { name: groupName, items: [] }
    }
    groups[groupName].items.push({
      path: `/${props.role}/${r.path}`,
      title: r.meta?.title || r.name,
      icon: r.meta?.icon || 'Menu'
    })
  })
  return Object.values(groups)
})

function showGroupTitle(index) {
  // 只在有多组且未折叠时显示分组标题
  return menuGroups.value.length > 1 && !collapsed.value
}
</script>

<style scoped>
.sidebar {
  background-color: #001529;
  height: 100vh;
  overflow-y: auto;
  overflow-x: hidden;
  transition: width 0.3s;
}
.sidebar::-webkit-scrollbar {
  width: 4px;
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  border-bottom: 1px solid #1f2d3d;
}
.logo.collapsed {
  padding: 0;
}
.logo-text {
  white-space: nowrap;
}
:deep(.el-menu) {
  border-right: none;
}
:deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
}
.menu-group-title {
  font-size: 12px !important;
  color: #6b7b8a !important;
  padding-left: 20px !important;
  height: 36px !important;
  line-height: 36px !important;
}
</style>
