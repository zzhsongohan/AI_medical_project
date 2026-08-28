<template>
  <div class="page-table">
    <el-table
      v-loading="loading"
      :data="tableData"
      :border="border"
      stripe
      style="width: 100%"
    >
      <slot />
    </el-table>
    <div class="pagination-wrap">
      <el-pagination
        :current-page="innerPage"
        :page-size="innerPageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  total: {
    type: Number,
    default: 0
  },
  loading: {
    type: Boolean,
    default: false
  },
  border: {
    type: Boolean,
    default: false
  },
  page: {
    type: Number,
    default: 1
  },
  pageSize: {
    type: Number,
    default: 10
  }
})

const emit = defineEmits(['update:page', 'update:pageSize', 'change'])

const innerPage = ref(props.page)
const innerPageSize = ref(props.pageSize)
const tableData = ref(props.data)

watch(() => props.data, (val) => {
  tableData.value = val
}, { deep: true })

watch(() => props.page, (val) => {
  innerPage.value = val
})

watch(() => props.pageSize, (val) => {
  innerPageSize.value = val
})

function handleSizeChange(size) {
  innerPageSize.value = size
  innerPage.value = 1
  emit('update:pageSize', size)
  emit('update:page', 1)
  emit('change', { page: 1, pageSize: size })
}

function handleCurrentChange(page) {
  innerPage.value = page
  emit('update:page', page)
  emit('change', { page, pageSize: innerPageSize.value })
}
</script>

<style scoped>
.page-table {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
}
.pagination-wrap {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
