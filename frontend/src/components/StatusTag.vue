<template>
  <el-tag :type="tagType" size="small">
    {{ label }}
  </el-tag>
</template>

<script setup>
import { computed } from 'vue'
import { userStatusMap, appointmentStatusMap, consultStatusMap, vectorStatusMap } from '@/utils/format'

const props = defineProps({
  status: {
    type: [Number, String],
    default: 0
  },
  type: {
    type: String,
    default: 'user' // user / appointment / consult / vector
  }
})

const statusMap = computed(() => {
  const maps = {
    user: userStatusMap,
    appointment: appointmentStatusMap,
    consult: consultStatusMap,
    vector: vectorStatusMap
  }
  return maps[props.type] || userStatusMap
})

const tagType = computed(() => statusMap.value[props.status]?.type || 'info')
const label = computed(() => statusMap.value[props.status]?.label || '未知')
</script>
