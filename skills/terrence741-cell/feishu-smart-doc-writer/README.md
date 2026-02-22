# Feishu Smart Doc Writer / 飞书智能文档写入器

> **English**: Feishu/Lark Smart Document Writer with auto-chunking, ownership transfer, auto-indexing, and document search.  
> **中文**: 飞书智能文档写入器，支持自动分块、所有权转移、自动索引和文档搜索。

---

## 🚀 What's New in v1.3.0 / v1.3.0 新功能

### English
- ✅ **Auto-Index Management**: Documents automatically added to local index after creation
- ✅ **Document Search**: Search through all your Feishu documents by keyword
- ✅ **Smart Tagging**: Auto-categorize documents based on content
- ✅ **List Documents**: Filter and list documents by tags

### 中文
- ✅ **自动索引管理**：创建文档后自动添加到本地索引
- ✅ **文档搜索**：按关键词搜索所有飞书文档
- ✅ **智能标签**：根据内容自动分类文档
- ✅ **列出文档**：按标签筛选和列出文档

---

## 🔧 Configuration / 配置说明

### English
This skill uses OpenClaw's built-in Feishu tools. **No manual token required**.

- `tenant_access_token` is managed automatically by OpenClaw
- You only need to configure your **OpenID** (for document ownership transfer)

### 中文
本 Skill 使用 OpenClaw 内置的飞书工具集，**无需手动获取 token**。

- `tenant_access_token` 由 OpenClaw 自动管理
- 只需要配置 **用户 OpenID**（用于文档所有权转移）

---

## ✨ Core Features / 核心功能

### 1. Smart Chunking / 智能分块写入
**English**: Feishu API has limits (~4000 chars for create, ~2000 for append). This skill automatically splits long content into chunks to ensure complete writing without blank documents.

**中文**: 飞书 API 对单次写入有限制（创建~4000字符，追加~2000字符）。本 Skill 自动将长内容分块写入，确保完整无丢失。

### 2. Auto Ownership Transfer / 自动转移所有权
**English**: Documents created by apps belong to the app by default. This skill automatically transfers ownership to you after creation, giving you full control.

**中文**: 应用创建的文档默认所有权属于应用。本 Skill 在创建后自动转移所有权给用户，用户拥有完全控制权。

### 3. Auto-Indexing / 自动索引
**English**: Every document is automatically added to your local index (`memory/feishu-docs-index.md`) with auto-generated summary and tags.

**中文**: 每个文档自动添加到本地索引（`memory/feishu-docs-index.md`），自动生成摘要和标签。

### 4. First-Time Setup Guide / 首次使用自动引导
**English**: Automatic guided configuration on first use. No need to read docs first.

**中文**: 首次使用时自动引导配置，无需提前查阅文档。

---

## 📖 Usage / 使用流程

### Quick Start / 快速开始

**Step 1: Try to create a document / 尝试创建文档**
```
/feishu-smart-doc-writer write_smart
title: My Document
title: 我的文档
content: Your content here...
content: 你的内容...
```

**Step 2: Follow the setup guide / 按照引导配置**

The skill will detect first-time use and show configuration guide.

Skill 会自动检测首次使用并显示配置引导。

**Step 3: Get your OpenID / 获取 OpenID**

**English:**
1. Login to https://open.feishu.cn
2. Go to your app → Permission Management
3. Search `im:message` → Click 【API】Send Message → Go to API Debug Console
4. Click "Quick Copy open_id" → Select account → Copy

**中文：**
1. 登录 https://open.feishu.cn
2. 进入应用 → 权限管理
3. 搜索 `im:message` → 点击【API】发送消息 → 前往API调试台
4. 点击"快速复制 open_id" → 选择账号 → 复制

**Step 4: Configure / 配置**
```
/feishu-smart-doc-writer configure
openid: ou_your_openid_here
permission_checked: true
```

**Step 5: Enable permission and publish / 开通权限并发布**

**English:**
1. Search `docs:permission.member:transfer` in Permission Management
2. Click "Enable"
3. **CRITICAL**: Click "Publish" button!

**中文：**
1. 在权限管理中搜索 `docs:permission.member:transfer`
2. 点击"开通"
3. **关键**：点击"发布"按钮！

---

## 🛠️ Tools / 工具

### write_smart / 智能创建
**English**: Create document with auto-chunking, ownership transfer, and index update.

**中文**: 创建文档，自动分块、转移所有权、更新索引。

### search_docs / 搜索文档
**English**: Search your document index by keyword.

**中文**: 按关键词搜索文档索引。

Example / 示例:
```
/feishu-smart-doc-writer search_docs
keyword: AI
keyword: 人工智能
```

### list_docs / 列出文档
**English**: List documents with optional filtering.

**中文**: 列出文档，可选筛选。

Example / 示例:
```
/feishu-smart-doc-writer list_docs
tag: AI
tag: 电商
status: Completed
```

### append_smart / 追加内容
**English**: Append content to existing document.

**中文**: 向现有文档追加内容。

---

## 📁 Files / 文件说明

- `SKILL.md` - Full documentation / 完整文档
- `CHANGELOG.md` - Version history / 版本历史
- `feishu_smart_doc_writer.py` - Core logic / 核心逻辑
- `index_manager.py` - Index management / 索引管理

---

## 📝 Changelog / 更新日志

See / 查看 [CHANGELOG.md](./CHANGELOG.md) for detailed history.

---

**Made with ❤️ for Feishu/Lark users / 为飞书用户精心制作**