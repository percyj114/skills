## Changelog

### v1.3.0 - Major Update with Auto-Indexing & Document Management

**Release Date:** 2026-02-22

#### 🚀 New Features

1. **Automatic Index Management**
   - Documents are automatically added to local index (`memory/feishu-docs-index.md`) after creation
   - Auto-generated summaries from document content
   - Smart content-based tagging (AI, E-commerce, Health, etc.)
   - No manual index updates needed - everything is automatic!

2. **Document Search & List Tools**
   - `search_docs`: Search through all your Feishu documents by keyword
   - `list_docs`: List documents with filtering by tags or status
   - Find any document instantly without remembering URLs

3. **Enhanced Auto-Chunking**
   - Smart content splitting to avoid API limits
   - Maintains document structure (headings, lists)
   - Handles long documents (10,000+ characters) seamlessly

#### 🔧 First-Time Setup Guide

**Step 1: Get Your Feishu OpenID**

Before using this skill, you need to obtain your Feishu OpenID:

1. **Login to Feishu Open Platform**
   - Visit: https://open.feishu.cn
   - Login with your Feishu account

2. **Navigate to Permission Management**
   - Select your app
   - Click "Permission Management" (权限管理)
   - Search for: `im:message`
   - Hover over "Related API Events" (相关API事件)
   - Select: **【API】Send Message** (【API】发送消息)
   - Click: **"Go to API Debug Console"** (前往API调试台)

3. **Copy Your OpenID**
   - Find the blue link "Quick Copy open_id" (快速复制 open_id)
   - Click it
   - Select your account from the dropdown
   - Click "Copy"
   - Your OpenID looks like: `ou_xxxxxxxxxxxxxxxx`

**Step 2: Grant Transfer Ownership Permission**

⚠️ **CRITICAL: You must publish the app after granting permission!**

1. **Go to Permission Management**
   - In your app, click "Permission Management" (权限管理)

2. **Search and Enable**
   - Search: `docs:permission.member:transfer`
   - Find: "Transfer cloud document ownership" (转移云文档的所有权)
   - Click "Enable" (开通)

3. **Publish New Version** ⚠️
   - Click "Publish" (发布) button in top right
   - Wait for "Published" status
   - **Without publishing, the permission won't work!**

**Step 3: Configure the Skill**

Run the configure command:
```
/feishu-smart-doc-writer configure
openid: ou_your_openid_here
permission_checked: true
```

Your configuration is saved to `user_config.json` and will be used for all future documents.

#### 📖 Usage Examples

**Create a Document:**
```
/feishu-smart-doc-writer write_smart
title: My Project Report
content: # Introduction

This is my project report...
```

The skill will:
1. Create the document
2. Write content in chunks (auto-split if long)
3. Transfer ownership to you automatically
4. Add to your local index with tags

**Search Documents:**
```
/feishu-smart-doc-writer search_docs
keyword: AI technology
```

**List Documents by Tag:**
```
/feishu-smart-doc-writer list_docs
tag: E-commerce
```

#### 🔍 Auto-Tagging System

Documents are automatically tagged based on content:
- **AI Technology**: AI, artificial intelligence, model, GPT, LLM
- **OpenClaw**: OpenClaw, skill, agent
- **Feishu**: Feishu, document, docx
- **E-commerce**: E-commerce, TikTok, Alibaba, toy
- **Health & Sports**: Garmin, Strava, cycling, health
- **Daily Archive**: Conversation, archive, chat log

#### 🐛 Fixed Issues

- Fixed table parsing for 8-column index format
- Improved error handling during ownership transfer
- Enhanced chunking algorithm for better content preservation

#### 📁 Files Added

- `index_manager.py` - Core index management functionality
- Updated `__init__.py` - Added search_docs and list_docs tools
- Updated `SKILL.md` - Comprehensive usage documentation

#### 💡 Tips

1. **Keep user_config.json safe** - It contains your OpenID
2. **Check permissions** - If transfer fails, verify permission is published
3. **Index location** - Local index is at `memory/feishu-docs-index.md`
4. **Long documents** - Don't worry about length, auto-chunking handles it!

---

### v1.2.0 - Auto-Chunking & Ownership Transfer

- Implemented smart content chunking to avoid API limits
- Added automatic ownership transfer after document creation
- First-time user guide for OpenID configuration

### v1.1.0 - Basic Document Operations

- Basic document creation and appending
- Support for folder selection
- Simple configuration system

### v1.0.0 - Initial Release

- Basic Feishu document writing functionality
