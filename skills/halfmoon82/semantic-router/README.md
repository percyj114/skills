# Semantic Router Skill 使用指南

## 简介

Semantic Router 是一个可配置的语义检查与模型路由技能，支持用户自定义模型池和任务类型匹配规则。

**发布地址：** https://clawhub.ai/skill/semantic-router

---

## 功能特性

- **两步检测机制**：语义连续性检查 → 任务类型匹配
- **关键词优先级**：P0(延续) > P1(开发) > P2(查询) > P3(内容) > P4(新会话)
- **强制触发**：通过 message injector 每次消息都执行语义检查
- **可配置模型池**：支持自定义主模型和 Fallback 模型
- **Fallback 回路**：Primary → Fallback1 → Fallback2，每2小时自动回切
- **自动模型切换**：根据任务类型自动选择合适的模型池
- **上下文归档**：新会话时自动归档旧上下文

---

## 安装

### 方式一：从 ClawHub 安装（推荐）

```bash
# 安装最新版本
clawhub install semantic-router

# 或指定版本
clawhub install semantic-router --version 1.2.0
```

### 方式二：手动安装

```bash
# 克隆技能文件夹到本地
cp -r semantic-router ~/.openclaw/workspace/skills/
```

---

## 强制触发配置（推荐）

通过 message injector 插件强制每次消息都触发语义检查：

```json
{
  "plugins": {
    "entries": {
      "message-injector": {
        "enabled": true,
        "trigger": "always",
        "script": "python3 ~/.openclaw/workspace/skills/semantic-router/scripts/semantic_check.py"
      }
    }
  }
}
```

**效果**：每次用户消息都会经过语义检查，不再依赖会话检测。

---

## 两步检测流程

```
用户消息
    ↓
Step 1: 语义连续性检查
    ├── 延续信号 → B分支 (保持当前池)
    └── 新会话信号 → Step 2
    
Step 2: 任务类型匹配
    ├── P0 延续关键词 → B分支
    ├── P1 开发关键词 → Intelligence 池
    ├── P2 查询关键词 → Highspeed 池
    ├── P3 内容关键词 → Humanities 池
    └── P4 新会话 → 高速池默认
```

---

## 关键词优先级

| 优先级 | 类型 | 关键词 | 目标池 |
|--------|------|--------|--------|
| P0 | 延续 | 继续、接着、刚才、下一步 | (保持) |
| P1 | 开发 | 开发、写代码、调试、修复、部署 | Intelligence |
| P2 | 查询 | 查一下、搜索、找、天气 | Highspeed |
| P3 | 内容 | 写文章、总结、解释、教育 | Humanities |
| P4 | 新会话 | hi、在吗、hello | Highspeed |

---

## 三池架构

| 池 | 任务类型 | Primary | Fallback 1 | Fallback 2 |
|---|---------|---------|------------|-------------|
| **Highspeed** | 信息检索、网页搜索 | openai/gpt-4o-mini | glm-4.7-flashx | MiniMax-M2.5 |
| **Intelligence** | 开发、自动化、系统运维 | openai-codex/gpt-5.3-codex | kimi-k2.5 | MiniMax-M2.5 |
| **Humanities** | 内容生成、多模态、问答 | openai/gpt-4o | kimi-k2.5 | MiniMax-M2.5 |

---

## Fallback 回路

所有子代理统一使用 Primary → Fallback1 → Fallback2 回路：

```
主模型失败 (429/Timeout/Error)
    ↓
Fallback 1 (同池或跨池)
    ↓
Fallback 2 (跨池)
    ↓
全部失败 → 暂停 → 报告主代理
```

**当前实现**：
- 脚本自动检测任务类型并输出 `fallback_chain`
- Agent 读取 `fallback_chain` 并自动执行切换
- 回切机制：每2小时自动回切到主模型

**回切机制**：
- 每2小时自动回切到主模型
- 记录 fallback 到 `memory/model-fallback.log`

---

## 使用方法

### 1. 基础检测

```bash
python3 ~/.openclaw/workspace/skills/semantic-router/scripts/semantic_check.py "查一下天气" "Intelligence"
```

**输出示例**：
```json
{
  "branch": "C",
  "task_type": "info_retrieval",
  "pool": "Highspeed",
  "primary_model": "openai/gpt-4o-mini",
  "fallback_chain": ["openai/gpt-4o-mini", "glm-4.7-flashx", "MiniMax-M2.5"],
  "need_switch": true,
  "declaration": "执行信息检索 新会话 应使用高速池 已切换为openai/gpt-4o-mini"
}
```

### 2. 带上下文的检测

```bash
python3 semantic_check.py "继续" "Intelligence" "帮我写个函数" "谢谢"
```

### 3. Fallback 模式

当主模型失败时，手动触发 fallback 回路：

```bash
python3 semantic_check.py --fallback openai-codex/gpt-5.3-codex kimi-k2.5 minimax-cn/MiniMax-M2.5
```

**输出示例**：
```json
{
  "attempted": ["openai-codex/gpt-5.3-codex", "kimi-k2.5"],
  "success": true,
  "current_model": "kimi-k2.5"
}
```

---

## 自定义配置

### 自定义模型池

编辑 `config/pools.json`：

```json
{
  "你的池名": {
    "name": "显示名称",
    "description": "池描述",
    "primary": "主模型ID",
    "fallback_1": "备用模型1",
    "fallback_2": "备用模型2"
  }
}
```

### 自定义任务匹配

编辑 `config/tasks.json`：

```json
{
  "任务类型名": {
    "keywords": ["关键词1", "关键词2"],
    "pool": "对应的池名"
  }
}
```

---

## 文件结构

```
semantic-router/
├── SKILL.md              # 技能说明
├── README.md             # 使用指南
├── config/
│   ├── pools.json       # 模型池配置
│   └── tasks.json       # 任务类型配置
├── scripts/
│   └── semantic_check.py # 核心脚本（含自动切换）
└── references/
    └── flow.md          # 流程图
```

---

## 版本历史

- **1.2.0** (2026-02-23): 
  - 新增 Fallback 回路自动化
  - 新增 --fallback 模式手动触发
  - 输出包含 fallback_chain 字段
  - 支持 -e 自动执行切换

- **1.1.0** (2026-02-23): 
  - 新增两步检测机制（语义连续性 + 任务类型）
  - 新增关键词优先级矩阵
  - 新增 message injector 强制触发说明
  - 新增 fallback 回路规范

- **1.0.0** (2026-02-23): 初始版本发布

---

## 作者

- 作者：DeepEye (Sir 的数字分身)
- 联系：bubushi@126.com

---

*Generated on 2026-02-23*
