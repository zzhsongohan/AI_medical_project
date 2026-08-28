# ==========================================
# 前端 Dockerfile - 多阶段构建
# ==========================================

# 构建阶段
FROM node:18-alpine AS builder
WORKDIR /app

# 安装依赖（使用国内源加速）
COPY package*.json ./
RUN npm config set registry https://registry.npmmirror.com \
    && npm install

# 拷贝源码并构建
COPY . .
RUN npm run build

# 生产阶段 - nginx
FROM nginx:alpine

# 拷贝构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 拷贝nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]
