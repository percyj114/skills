---
name: feishu-smart-doc-writer
description: |
  【English】Feishu/Lark Smart Document Writer with auto-chunking, ownership transfer & index management.
  
  【中文】飞书智能文档写入器，支持自动分块、所有权转移和索引管理。
---

# Feishu Smart Doc Writer v1.3.0
# 飞书智能文档写入器 v1.3.0

---

## 🚀 Core Features / 核心功能

### 1. Smart Document Creation / 智能文档创建
**English:**
- **Auto-chunking**: Split long content into chunks to avoid API limits
- **Auto Ownership Transfer**: Automatically transfer document to user after creation
- **Auto Index Update**: Add document info to local index `memory/feishu-docs-index.md`
- **Smart Tagging**: Auto-tag based on content (AI, E-commerce, Health, etc.)

**中文：**
- **自动分块**：长内容自动分割，避免API限制导致的空白文档
- **自动转移所有权**：创建后自动转移给用户
- **自动索引更新**：文档信息自动添加到本地索引
- **智能分类**：根据内容自动打标签（AI技术、电商、健康运动等）

### 2. Document Management / 文档管理
**English:**
- **Search Documents**: Search local index by keyword
- **List Documents**: Filter by tags or status
- **Append Content**: Add content to existing documents

**中文：**
- **搜索文档**：按关键词搜索本地索引
- **列出文档**：按标签、状态筛选
- **追加内容**：向现有文档追加内容

---

## 📋 Tools / 工具列表

### write_smart - Create Document / 创建文档
**English:** Create document with auto-chunking, ownership transfer, and index update.

**中文：** 创建文档，自动完成分块写入、所有权转移、索引更新。

**Parameters / 参数：**
```json
{
  "title": "Document Title / 文档标题",
  "content": "Content (supports long text) / 内容（支持长内容）",
  "folder_token": "Optional folder token / 可选的文件夹token"
}
```

**Returns / 返回：**
```json
{
  "doc_url": "https://feishu.cn/docx/xxx",
  "doc_token": "xxx",
  "chunks_count": 3,
  "owner_transferred": true,
  "index_updated": true
}
```

---

### append_smart - Append Content / 追加内容
**English:** Append content to existing document (auto-chunked).

**中文：** 向现有文档追加内容（自动分块）。

---

### search_docs - Search Documents / 搜索文档
**English:** Search documents in local index.

**中文：** 搜索本地索引中的文档。

**Parameters / 参数：**
```json
{
  "keyword": "Search keyword / 搜索关键词",
  "search_in": ["name", "summary", "tags"]  // optional / 可选
}
```

---

### list_docs - List Documents / 列出文档
**English:** List all documents with filtering.

**中文：** 列出所有文档，支持筛选。

**Parameters / 参数：**
```json
{
  "tag": "AI / 标签",
  "status": "Completed / 状态",
  "limit": 10
}
```

---

### transfer_ownership - Transfer Ownership / 转移所有权
**English:** Manually transfer document ownership (usually automatic).

**中文：** 手动转移文档所有权（通常自动完成）。

**Note / 注意：** Only need `owner_openid`. `tenant_access_token` is obtained automatically by the skill.

只需要提供 `owner_openid`，`tenant_access_token` 由 Skill 自动获取。

---

### configure - Configure / 配置
**English:** Configure OpenID on first use.

**中文：** 首次使用时配置 OpenID。

---

## 🚀 Quick Start / 快速开始

### First-Time Setup (3 Steps) / 首次使用（3步）

**Step 1: Call write_smart / 调用 write_smart**
```
/feishu-smart-doc-writer write_smart
title: Test Document / 测试文档
content: This is a test / 这是测试内容
```

**Step 2: Get Your OpenID / 获取 OpenID**

**English:**
1. Login to https://open.feishu.cn
2. Go to your app → Permission Management
3. Search `im:message` → Click 【API】Send Message → Go to API Debug Console
4. Click "Quick Copy open_id" → Select your account → Copy

**中文：**
1. 登录 https://open.feishu.cn
2. 进入应用 → 权限管理
3. 搜索 `im:message` → 点击【API】发送消息 → 前往API调试台
4. 点击"快速复制 open_id" → 选择账号 → 复制

**Step 3: Configure / 配置**
```
/feishu-smart-doc-writer configure
openid: ou_your_openid
permission_checked: true
```

Then enable permission `docs:permission.member:transfer` and **publish** your app.

然后开通权限 `docs:permission.member:transfer` 并**发布**应用。

---

## 📊 Index Management / 索引管理

### Auto-Index Workflow / 自动索引流程
```
write_smart creates document
    ↓
Write content (auto-chunked) / 写入内容（自动分块）
    ↓
Transfer ownership / 转移所有权
    ↓
Auto-update index → memory/feishu-docs-index.md / 自动更新索引
    ↓
Done! / 完成！
```

### Auto-Tagging / 自动标签
**English:** Tags are automatically assigned based on content:

**中文：** 根据内容自动识别标签：

| Keyword / 关键词 | Tag / 标签 |
|----------------|-----------|
| AI, 人工智能, GPT | AI技术 |
| OpenClaw, skill, agent | OpenClaw |
| Feishu, 飞书, docx | 飞书文档 |
| E-commerce, 电商, TikTok | 电商 |
| Garmin, Strava, 骑行 | 健康运动 |

---

## 📝 Examples / 示例

### Example 1: Create Tech Document / 创建技术文档
```
/feishu-smart-doc-writer write_smart
title: AI Research Report / AI技术调研报告
content: # Overview / 概述

AI technology is... / 人工智能是...
```

**Result / 结果：**
- Document created / 文档创建成功
- Tagged "AI Technology" / 自动打上"AI技术"标签
- Index updated / 索引已更新

### Example 2: Search Documents / 搜索文档
```
/feishu-smart-doc-writer search_docs
keyword: AI
```

### Example 3: List by Tag / 按标签列出
```
/feishu-smart-doc-writer list_docs
tag: AI
```

---

## ⚙️ Configuration / 配置

### User Config File / 用户配置文件
**Location / 位置：** `skills/feishu-smart-doc-writer/user_config.json`

```json
{
  "owner_openid": "ou_5b921cba0fd6e7c885276a02d730ec19",
  "permission_noted": true,
  "first_time": false
}
```

### Required Permissions / 必需权限
- `docx:document:create` - Create documents / 创建文档
- `docx:document:write` - Write content / 写入内容
- `docs:permission.member:transfer` - Transfer ownership ⚠️ **Critical** / 转移所有权 ⚠️ **关键**

---

## 🐛 Troubleshooting / 故障排除

### "open_id is not exist" Error / 错误
**Cause / 原因：** Used `user_id` instead of `openid`

**Fix / 解决：** Use format `ou_xxxxxxxx` (starts with "ou_")

### "Permission denied" Error / 权限不足错误
**Cause / 原因：** Missing `docs:permission.member:transfer` or not published

**Fix / 解决：**
1. Enable the permission / 开通权限
2. Click "Publish" button / 点击"发布"按钮

### Index Not Updated / 索引未更新
**Check / 检查：**
1. Check `memory/feishu-docs-index.md` exists / 检查索引文件是否存在
2. Check `index_updated` field in response / 检查返回的 `index_updated` 字段
3. Check error logs / 查看错误日志

---

## 📝 Version History / 版本历史

### v1.3.0 (2026-02-22)
- ✅ Auto-index management / 自动索引管理
- ✅ search_docs & list_docs tools / 搜索和列出工具
- ✅ Smart auto-tagging / 智能自动标签
- ✅ Write smart auto-updates index / 写入时自动更新索引

### v1.2.0
- ✅ Auto-chunking / 自动分块
- ✅ Auto ownership transfer / 自动转移所有权
- ✅ First-time user guide / 首次使用引导

### v1.1.0
- ✅ Basic document operations / 基础文档操作

---

*Last updated / 最后更新：2026-02-22*