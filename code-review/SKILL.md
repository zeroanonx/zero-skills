---
name: code-review
description: 当前端代码需要审查（Code Review）时使用的工程级技能
license: MIT
metadata:
  author: zero
  version: "2.2.0"
---

`fshows` 大前端组内部使用的 **Code Review 工程规范与实践集合**。

本技能用于对 **前端代码变更** 进行系统性审查，目标是：
- 提前发现问题
- 降低技术债
- 保证长期可维护性

---

## 🧠 Skill Trigger（触发条件）

在以下任一情况下 **必须启用本技能**：
- 用户明确提到：`code review / CR / 审查代码 / cr代码 / cr`
- 用户提供 PR、commit diff、分支变更说明
- 用户要求评估代码质量、规范、可维护性、性能或安全性
- 用户请求代码优化建议或重构指导

---

## 📚 规范与依据

### 核心规范（必须遵守）
- **前端规范**: [fshowsRules](rules/fshows.md) - 团队统一编码标准
- **Vue 最佳实践**: [vue](../vue-best-practices/SKILL.md) - Vue 3 项目规范
- **React 最佳实践**: [vercel-react-best-practices](../vercel-react-best-practices/SKILL.md) - React 性能优化
- **TypeScript 最佳实践**: [typescript-best-practices](../typescript-best-practices/SKILL.md) - 类型安全保障

### 补充资源
- 性能优化：数组、对象、函数、正则方法最佳优化
- 安全规范：XSS 防护、数据验证、依赖安全  

---

## 🔍 Code Review 流程（强制执行）

### 1. 项目上下文理解
```bash
# 必须执行的信息收集
- 读取 package.json → 确认技术栈和依赖
- 读取 README.md → 了解项目背景
- 检查构建配置（vite.config.js / webpack.config.js等）
- 确认项目类型：SPA / SSR / 小程序 / H5
```

### 2. 变更范围确认
**必须主动询问用户**：
```
请明确本次审查范围（用户上下键选择）：
1. 当前工作区的未提交变更
2. 指定 commit 的变更
3. 当前分支和主分支的所有差异
4. 特定文件或目录
```

### 3. 多维度审查（按优先级）

#### 🔴 阻塞性问题（必须修复）
- **类型安全**: any 类型、类型缺失、类型错误
- **安全漏洞**: XSS、CSRF、敏感信息泄露
- **架构缺陷**: 循环依赖、职责不清
- **性能瓶颈**: 内存泄漏、无限循环、低效算法

#### 🟡 建议优化（强烈建议）
- **代码规范**: 命名、格式、注释规范
- **可维护性**: 函数复杂度、重复代码
- **错误处理**: 异常捕获、边界情况
- **性能优化**: 计算属性、事件监听、资源加载

#### 🟢 可选建议（非强制）
- **代码风格**: 变量声明方式、模板字符串等
- **最佳实践**: 推荐的写法和模式
- **文档完善**: 类型定义、函数注释

### 4. 知识库扩展机制
```bash
# 错误案例存储规则
文件名格式: error/[项目名]_[日期]_[分支名].md
存储内容:
1. 原错误代码片段
2. 问题分析
3. 优化代码示例
4. 防止复现建议

# 下次审查时自动匹配
- 搜索相似错误模式
- 提醒避免重复问题
```

### 5. 异常处理机制
```bash
# 常见问题处理
1. 文件不存在 → 跳过并记录
2. 权限不足 → 提示用户检查权限
3. Git 状态异常 → 指导用户正确操作
4. 依赖冲突 → 检查 package.json
```
---

## 📝 输出要求（严格执行）

### 输出路径
- **主要输出**: `./code-review-result.html` (项目根目录 HTML 格式)
- **备份路径**: `~/.config/opencode/skills/code-review/results/[项目名]_[日期].md` (Markdown 格式)
- **用户交付**: `~/Desktop/aiCreateFiles/code-review-[项目名]-[日期].html`

### HTML 生成与自动打开机制
**用户端仅输出 HTML 格式，Markdown 仅用于备份和知识库，完成后自动在默认浏览器打开**：

```bash
# 完整执行流程
1. 生成 HTML 报告（项目根目录）
2. 复制到桌面 aiCreateFiles 目录
3. 生成 Markdown 备份（备份目录）
4. 更新知识库（错误案例）
5. 自动打开浏览器显示 HTML 报告

# 浏览器自动打开命令
# macOS: open 命令
# Windows: start 命令  
# Linux: xdg-open 命令
```

### 输出结构模板
```markdown
# 📊 Code Review 报告

## 🎯 本次审查总结
- 审查范围: [具体描述]
- 文件数量: [数字] 个文件
- 变更类型: [新增/修改/删除]
- 审查时间: [时间戳]

## ❌ 阻塞性问题（必须修复）
### 1. [问题标题]
**文件**: `path/to/file.ts:行号`
**等级**: 阻塞性
**描述**: [具体问题描述]

**原代码**:
```typescript
// 错误代码
```

**修复建议**:
```typescript
// 正确代码
```

## ⚠️ 建议优化项（强烈建议）
### 1. [问题标题]
**文件**: `path/to/file.ts:行号`
**等级**: 建议
**描述**: [优化理由]

**原代码**:
```typescript
// 当前代码
```

**优化建议**:
```typescript
// 推荐代码
```

## 💡 可选建议（非强制）
- [建议列表]

## 📈 综合评估
- **代码质量评分**: [A/B/C/D]
- **建议合入**: ✅ 是 / ❌ 否 / ⚠️ 修复后合入
- **技术债风险评估**: [低/中/高]
- **下次审查重点**: [重点关注项]
```

### 输出要求
- ✅ **用户端仅输出 HTML**：项目根目录 `./code-review-result.html`
- ✅ **必须输出具体问题**，不允许"看起来不错"等模糊评价
- ✅ **必须提供修复方案**，包含可运行的代码示例
- ✅ **必须标注文件位置**，便于快速定位
- ✅ **必须给出明确结论**：是否建议合入
- ✅ **自动打开浏览器**：完成后在默认浏览器中打开 HTML 报告
- ✅ **备份生成 Markdown**：仅在备份目录和知识库扩展机制中使用 Markdown
- ✅ **必须更新知识库**：存储错误案例（Markdown 格式）

### HTML 报告标准化内容
**使用现代 HTML + CSS + JS 生成交互式报告**：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Review 报告 - [项目名]</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <style>
        /* 响应式设计、代码高亮、交互样式 */
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }
        .issue-card { border: 1px solid #e1e5e9; border-radius: 8px; margin: 1rem 0; overflow: hidden; }
        .issue-header { padding: 1rem; cursor: pointer; }
        .issue-content { padding: 1rem; display: none; }
        .code-block { background: #f6f8fa; border-radius: 6px; padding: 1rem; }
    </style>
</head>
<body>
    <header class="header">
        <h1>Code Review 报告 - [项目名]</h1>
        <div class="meta">
            <span>审查时间: [时间戳]</span>
            <span>项目: [项目名]</span>
            <span>审查者: AI Code Review</span>
        </div>
    </header>
    
    <section class="summary">
        <div class="score">评分: [A/B/C/D]</div>
        <div class="stats">
            <span>阻塞性问题: [数字]</span>
            <span>建议优化: [数字]</span>
            <span>可选建议: [数字]</span>
        </div>
    </section>
    
    <section class="issues">
        <!-- 按重要性排序的问题列表，支持折叠展开 -->
    </section>
    
    <section class="conclusion">
        <!-- 综合评估和建议 -->
    </section>
    
    <script>
        // 交互功能：折叠展开、代码高亮
        hljs.highlightAll();
    </script>
</body>
</html>
```

---

## 🈲 行为约束

### 严格遵守
- ✅ **专注审查范围**：不偏离用户指定的变更范围
- ✅ **具体问题导向**：提供可操作的修复建议
- ✅ **避免教学式长篇解释**：直接指出问题和解决方案
- ✅ **不主动重写代码**：除非用户明确要求重构

### 禁止行为
- ❌ **模糊评价**：如"代码质量不错"、"总体良好"等
- ❌ **过度扩展**：审查与本次变更无关的代码
- ❌ **纯理论解释**：不提供具体修复方案的长篇说明
- ❌ **忽略等级划分**：不区分问题严重程度

### 特殊场景处理
```bash
# 情况1: 代码完全正确
→ HTML 输出: 生成"审查通过"的简洁 HTML 报告
→ 备份 Markdown: "✅ 审查通过，未发现问题，建议合入"
→ 自动打开: 在默认浏览器中显示报告

# 情况2: 只有风格问题
→ HTML 输出: 详细的风格优化指南报告（交互式）
→ 备份 Markdown: "💡 发现[数量]处风格建议，非阻塞性问题，可选择性优化"
→ 自动打开: 在默认浏览器中显示报告

# 情况3: 发现阻塞性问题
→ HTML 输出: 完整的问题清单和修复方案报告（交互式）
→ 备份 Markdown: "❌ 发现[数量]个阻塞性问题，必须修复后重新审查"
→ 自动打开: 在默认浏览器中显示报告
```

---

## 🚀 技能更新日志

### v2.2.0 (2026-02-10)
- 🌐 **HTML 自动生成**：生成响应式交互式 HTML 报告
- 🖥️ **自动浏览器打开**：完成后在默认浏览器中显示报告
- 📋 **优化输出格式**：用户端仅输出 HTML，备份和知识库使用 Markdown
- 🎨 **HTML 标准化模板**：支持代码高亮、响应式设计和交互功能

### v2.1.0 (2026-02-10)
- 📄 **PDF 自动生成**：集成 PDF Skill，自动生成标准化审查报告
- 📋 **双重输出格式**：同时生成 Markdown 和 PDF 两种格式
- 🎨 **PDF 标准化模板**：统一的 Code Review 报告格式

### v2.0.0 (2026-02-10)
- 🔧 **重构输出模板**：提供标准化的审查报告格式
- 🛠️ **完善错误处理**：添加异常情况处理机制
- 📊 **量化评估体系**：引入代码质量评分和技术债风险评估
- 🔍 **知识库扩展**：建立错误案例存储和复现检测机制
- 🎯 **触发条件优化**：增加更多场景识别
- 📚 **规范引用完善**：补充 TypeScript 等核心规范引用

### v1.0.0 (原版本)
- 基础 CR 流程定义
- fshows 规范集成
- 基本输出要求

