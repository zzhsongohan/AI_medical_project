# AI智能医疗问诊平台 - 前端

基于 Vue 3 + Vite + Element Plus 的医疗问诊平台前端。

## 技术栈

- **框架**: Vue 3 + Composition API
- **构建工具**: Vite 5
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **UI组件库**: Element Plus
- **HTTP请求**: Axios
- **图表**: ECharts 5
- **图谱可视化**: vis-network
- **富文本编辑器**: wangEditor

## 功能模块

### 患者端 (user)
- 🏠 首页概览
- 💬 AI智能问诊（SSE流式对话）
- 👨‍⚕️ 找医生 + 预约挂号
- 📅 我的预约
- 💊 人工问诊
- 📁 健康档案
- 📚 健康科普文章
- 🕸️ 知识图谱探索
- 👤 个人中心

### 医生端 (doctor)
- 🏥 工作台
- 📅 预约管理
- 💬 问诊回复
- 📁 患者档案管理
- 🕸️ 图谱推理
- 👤 个人中心

### 管理员端 (admin)
- 📊 数据概览（仪表盘）
- 👤 用户管理
- 👨‍⚕️ 医生管理
- 🏥 科室管理
- 📅 预约管理
- 💬 问诊管理
- 🤖 AI问诊记录
- 📚 文章管理
- 🔔 公告管理
- 📁 知识库管理
- 🕸️ 图谱管理
- 👤 个人中心

## 开发

### 安装依赖
```bash
npm install
```

### 启动开发服务器
```bash
npm run dev
```
访问 http://localhost:5173

### 构建生产版本
```bash
npm run build
```

## Docker 部署

项目根目录执行：

```bash
docker-compose up -d --build
```

前端访问地址：http://localhost:8080

后端API通过nginx代理转发，无需单独配置。

## 项目结构

```
src/
├── api/              # API接口封装
├── assets/           # 静态资源
├── components/       # 通用组件
├── layouts/          # 布局组件
├── router/           # 路由配置
├── stores/           # Pinia状态管理
├── utils/            # 工具函数
├── views/            # 页面视图
│   ├── login/        # 登录注册
│   ├── user/         # 患者端
│   ├── doctor/       # 医生端
│   └── admin/        # 管理员端
├── App.vue
└── main.js
```

## 默认账号

| 角色 | 用户名 | 密码 | 说明 |
|------|--------|------|------|
| 管理员 | admin | admin123 | 系统管理员 |
| 医生 | doctor1 | 123456 | 测试医生 |
| 患者 | user1 | 123456 | 测试患者 |

（具体账号以数据库初始化脚本为准）
