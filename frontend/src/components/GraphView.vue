<template>
  <div ref="graphRef" class="graph-container"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { Network } from 'vis-network'

const props = defineProps({
  nodes: {
    type: Array,
    default: () => []
  },
  edges: {
    type: Array,
    default: () => []
  },
  height: {
    type: String,
    default: '500px'
  }
})

const emit = defineEmits(['nodeClick'])

const graphRef = ref(null)
let network = null

// 节点类型对应的颜色
const nodeColors = {
  Disease: { background: '#f56c6c', border: '#f56c6c' },
  Symptom: { background: '#e6a23c', border: '#e6a23c' },
  Department: { background: '#409eff', border: '#409eff' },
  Drug: { background: '#67c23a', border: '#67c23a' },
  Check: { background: '#909399', border: '#909399' },
  Food: { background: '#9b59b6', border: '#9b59b6' }
}

function initGraph() {
  if (!graphRef.value) return

  const nodeMap = {}
  const visNodes = props.nodes.map(n => {
    const id = n.id || n.name
    const label = n.label || n.name || ''
    // 兼容多种类型字段：type / group / category
    const type = n.type || n.group || n.category || 'default'
    const colorObj = nodeColors[type] || { background: '#909399', border: '#606266' }
    nodeMap[id] = label
    return {
      id,
      label,
      color: colorObj,
      shape: 'ellipse',
      font: {
        color: '#fff',
        size: 13,
        face: 'Microsoft YaHei, sans-serif'
      },
      margin: 10,
      labelHighlightBold: true
    }
  })

  const visEdges = props.edges.map((e, i) => ({
    id: i,
    from: e.from || e.source,
    to: e.to || e.target,
    label: e.relationship || e.relation || e.label || '',
    arrows: 'to',
    font: { size: 11, align: 'middle', color: '#606266', strokeWidth: 4, strokeColor: '#fff' },
    color: { color: '#c0c4cc', highlight: '#409eff' },
    smooth: { type: 'curvedCW', roundness: 0.2 },
    hoverWidth: 2
  }))

  const data = { nodes: visNodes, edges: visEdges }
  const options = {
    nodes: { borderWidth: 2 },
    edges: { width: 1 },
    physics: {
      enabled: true,
      barnesHut: {
        gravitationalConstant: -3000,
        centralGravity: 0.3,
        springLength: 150,
        springConstant: 0.04
      },
      stabilization: { iterations: 100 }
    },
    interaction: {
      hover: true,
      tooltipDelay: 200
    }
  }

  network = new Network(graphRef.value, data, options)
  network.on('click', (params) => {
    if (params.nodes.length > 0) {
      const nodeId = params.nodes[0]
      const nodeData = props.nodes.find(n => (n.id || n.name) === nodeId)
      emit('nodeClick', nodeData || { id: nodeId })
    }
  })
}

function destroyGraph() {
  if (network) {
    network.destroy()
    network = null
  }
}

watch(() => [props.nodes, props.edges], () => {
  destroyGraph()
  initGraph()
}, { deep: true })

onMounted(() => {
  initGraph()
  window.addEventListener('resize', () => {
    network?.fit()
  })
})

onBeforeUnmount(() => {
  destroyGraph()
})
</script>

<style scoped>
.graph-container {
  width: 100%;
  height: v-bind(height);
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
}
</style>
