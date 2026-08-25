# Git 工作流规范

基于 **GitHub Flow** 的团队协作标准流程。所有代码合入 `main` 必须走 Pull Request。

---

## 一、分支命名规范

| 类型 | 前缀 | 示例 | 说明 |
|------|------|------|------|
| 功能开发 | `feature/` | `feature/user-login` | 新功能、新模块 |
| Bug 修复 | `bugfix/` | `bugfix/login-error` | 开发阶段发现的 bug |
| 线上紧急修复 | `hotfix/` | `hotfix/payment-crash` | 生产环境紧急修复 |
| 杂项/工具 | `chore/` | `chore/update-deps` | 构建脚本、依赖升级等 |

> 命名使用 **kebab-case**（小写+连字符），见名知意。

---

## 二、Commit 信息规范

采用 **Conventional Commits** 格式：

```
<type>: <描述>
```

### type 类型

| type | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 bug |
| `docs` | 文档变更 |
| `style` | 代码格式调整（不影响逻辑） |
| `refactor` | 代码重构（非新功能也非修 bug） |
| `perf` | 性能优化 |
| `test` | 增加或调整测试 |
| `chore` | 构建/工具/依赖等杂项 |
| `merge` | 合并分支 |

### 示例
```
feat: 实现用户登录接口
fix: 修复登录失败时错误提示不正确的问题
docs: 更新API文档说明
chore: 升级 pandas 到 2.0.0
```

---

## 三、完整开发流程

### 第 1 步：从 main 切出新分支

```bash
# 切到 main 并拉取最新代码
git checkout main
git pull origin main

# 从 main 切出 feature 分支
git checkout -b feature/xxx
```

> ⚠️ 每次切新分支前务必 `git pull`，确保基于最新主干开发。

---

### 第 2 步：日常开发与提交

```bash
# 编写代码...

# 提交（一个功能点一个 commit）
git add .
git commit -m "feat: xxx"

# 推送到远程（第一次加 -u，自动创建远程分支）
git push -u origin feature/xxx
# 之后直接 git push 即可
```

> 💡 远程 feature 分支无需手动创建，`git push` 时会自动创建。

---

### 第 3 步：定期同步主干

开发周期较长或准备提 PR 前，将 `main` 的最新改动合入你的 feature 分支：

```bash
# 拉取远程 main 最新代码
git checkout main
git pull origin main

# 切回 feature 分支，合并 main
git checkout feature/xxx
git merge main
```

#### 遇到冲突怎么办？

1. Git 会提示哪些文件有冲突（`both modified`）
2. 打开冲突文件，找到 `<<<<<<<` / `=======` / `>>>>>>>` 标记
3. 手动选择保留的代码，删除标记行
4. 解决完所有冲突后：
   ```bash
   git add .
   git commit -m "merge: 同步 main 最新代码"
   git push
   ```

---

### 第 4 步：发起 Pull Request (PR)

功能开发完、自测通过、同步完主干后：

```bash
# 确认所有代码都已推送
git status
git push
```

在 GitHub/GitLab 网页操作：

1. 点击 **Compare & pull request**（或手动选分支）
2. **Base**: `main` ｜ **Compare**: `feature/xxx`
3. 填写 PR 描述：
   - **做了什么**（What）
   - **为什么做**（Why）
   - **怎么验证**（How to test）
4. 指定 **Reviewer**（至少 1 人审核）
5. 点击 **Create Pull Request**

---

### 第 5 步：代码审查 & 修改

- Reviewer 审核代码，可能提出意见
- 在本地 feature 分支修改后正常 commit + push，新提交会自动追加到同一 PR
- 所有问题解决后，Reviewer 点击 **Approve**

---

### 第 6 步：合并 PR

审查通过 + CI 通过后，在 PR 页面合并：

| 合并方式 | 效果 | 推荐场景 |
|----------|------|----------|
| **Squash and merge** ⭐ | 整个分支压缩成 1 个 commit 合入 main | 大多数场景，保持 main 历史整洁 |
| **Create a merge commit** | 保留完整分支历史，产生 merge commit | 大功能分支，需保留开发轨迹 |
| **Rebase and merge** | 将分支提交接到 main 后面，线性历史 | 追求干净线性历史的团队 |

> 🔧 本项目默认使用 **Squash and merge**。

---

### 第 7 步：收尾清理

```bash
# 切回 main，拉取最新代码
git checkout main
git pull origin main

# 删除本地 feature 分支
git branch -d feature/xxx

# 删除远程 feature 分支（也可在 GitHub 页面点 Delete）
git push origin --delete feature/xxx
```

---

## 四、流程图

```
开始新功能
  │
  ▼
git pull main → git checkout -b feature/xxx
  │
  ▼
开发 → commit → push  ←──┐
  │                      │
  ├──→ 定期 merge main ──┘  （同步主干）
  │
  ▼
提 PR → 代码审查 → 修改 → 通过
  │
  ▼
合并 PR（Squash and merge）
  │
  ▼
git pull main → 删除分支 → 完成
```

---

## 五、核心原则（三条速记）

1. **`main` 永远是可发布的** — 不能直接改，所有改动走 PR
2. **feature 分支是私人空间** — 随便折腾，同步主干时把 `main` 合进来（不要反过来）
3. **切新分支前先 `git pull`** — 保证起点是最新的

---

## 六、常用命令速查

| 操作             | 命令                                                                                                                  |
|----------------|---------------------------------------------------------------------------------------------------------------------|
| 查看状态           | `git status`                                                                                                        |
| 查看本地分支         | `git branch`                                                                                                        |
| 查看所有分支         | `git branch -a`                                                                                                     |
| 查看提交历史         | `git log --oneline`                                                                                                 |
| 切换分支           | `git checkout <branch>` / `git switch <branch>`                                                                     |
| 创建并切换          | `git checkout -b <branch>` / `git switch -c <branch>`                                                               |
| 删除本地分支         | `git branch -d <branch>`                                                                                            |
| 删除远程分支         | `git push origin --delete <branch>`                                                                                 |
| 暂存当前修改         | `git stash`                                                                                                         |
| 恢复暂存           | `git stash pop`                                                                                                     |
| 撤销最后一次提交（保留改动） | `git reset --soft HEAD~1`                                                                                           |
| 查看暂存和工作区差异     | `git diff`                                                                                                          |
| 配置VPN          | `git config --global http.proxy http://127.0.0.1:7890<br/>git config --global https.proxy http://127.0.0.1:7890git` |

