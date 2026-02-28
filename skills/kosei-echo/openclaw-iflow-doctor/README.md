# 🦞 OpenClaw iFlow Doctor - 智能自我修复系统

> **AI 驱动的 OpenClaw 自动修复工具**  
> 版本：v1.0.0 | 跨平台 | 零配置 | 新手友好

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/kosei-echo/openclaw-iflow-doctor/releases)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#安装)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

---

## 🚀 5 分钟快速开始

### 前提条件

1. ✅ **已安装 OpenClaw** - 检查：`openclaw --version`
2. ✅ **OpenClaw 能正常运行** - 测试：`openclaw gateway start`
3. ⭐ **iflow CLI**（可选）- 安装：`npm install -g iflow`

### 安装

```bash
openclaw skills install https://github.com/kosei-echo/openclaw-iflow-doctor
```

### 验证

```bash
openclaw skills list | grep iflow-doctor
```

看到 `openclaw-iflow-doctor` ✅ 安装成功！

### 使用

**无需配置，自动工作！**

当 OpenClaw 出问题时，技能会自动：
1. 捕获错误
2. 搜索解决方案
3. 自动修复 或 提示调用 iflow

---

## 🎯 这是什么？

**OpenClaw iFlow Doctor** 是一个智能自我修复技能，能让你的 OpenClaw 在出问题时**自动诊断和修复**。

### 核心能力

| 功能 | 说明 | 状态 |
|------|------|------|
| **自动修复** | 80% 常见问题自动解决 | ✅ |
| **智能诊断** | 识别 8 种问题类型 | ✅ |
| **案例库** | 10 个预置解决方案 | ✅ |
| **iflow 集成** | 复杂问题调用 iflow 协助 | ✅ |
| **跨平台** | Windows/macOS/Linux | ✅ |
| **零配置** | 安装即用 | ✅ |

### 能修复什么？

| 问题类型 | 自动修复 | 成功率 |
|---------|---------|--------|
| 🧠 记忆搜索失败 | ✅ 重置索引 | 85% |
| 🚪 网关启动失败 | ✅ 重启服务 | 90% |
| 🔌 API 额度超限 | ❌ 需充值 | - |
| ⚙️ 配置文件损坏 | ✅ 从备份恢复 | 85% |
| 🌐 网络连接问题 | ✅ 检查连接 | 80% |
| 🤖 Agent 生成失败 | ✅ 重新加载 | 80% |
| 🔐 权限错误 | ✅ 修复权限 | 85% |
| 📦 安装损坏 | ⚠️ 需重装 | - |

---

## 🏗️ 工作原理

```
OpenClaw 出错
    ↓
自动捕获错误
    ↓
搜索案例库 (10 个预置方案)
    ↓
找到匹配 → 自动修复 ✓
    ↓
找不到 → 生成诊断报告 + BAT 工具
           ↓
      提示调用 iflow
           ↓
      iflow 协助修复 → 保存到案例库
```

### 4 层恢复架构

```
Level 1: KeepAlive ⚡ (0-30s)    → 即时重启
Level 2: Watchdog 🔍 (3-5min)    → 健康检查 + 指数退避
Level 3: AI Doctor 🧠 (5-30min)  → 基于案例的诊断
Level 4: Human Alert 🚨          → iflow/人工通知
```

---

## 📦 安装

### 方式 1：从 GitHub 安装（推荐）

```bash
openclaw skills install https://github.com/kosei-echo/openclaw-iflow-doctor
```

### 方式 2：本地安装

```bash
# 复制技能文件
cp -r openclaw-iflow-doctor ~/.openclaw/skills/

# 验证
openclaw skills list | grep iflow-doctor
```

### 方式 3：手动安装

1. 下载本仓库所有文件
2. 复制到 `~/.openclaw/skills/openclaw-iflow-doctor/`
3. 验证：`openclaw skills list`

---

## 💡 使用

### 自动模式（推荐）

**安装后无需配置，技能会自动工作！**

#### 场景 1：简单问题（自动修复）

```
[系统] OpenClaw gateway crashed
[系统] iFlow Doctor: 检测到网关崩溃
[系统] iFlow Doctor: 搜索案例库... 找到 CASE-002
[系统] iFlow Doctor: 正在重启网关...
[系统] ✓ 网关已重启
[系统] 修复报告：~/.../reports/修复报告_20260228.txt
```

**你需要做的**：查看报告，无需操作 ✅

#### 场景 2：复杂问题（需要 iflow）

```
[系统] Configuration corrupted
[系统] iFlow Doctor: ✗ 无法自动修复
[系统] iFlow Doctor: 已生成诊断报告
[系统] iFlow Doctor: 💡 建议：运行 iflow
```

**你需要做的**：
1. 运行 `iflow`
2. 描述问题
3. iflow 协助修复 ✅

### 手动模式

#### 查看技能统计

```bash
cd ~/.openclaw/skills/openclaw-iflow-doctor
python3 openclaw_memory.py --stats
```

#### 查看维修案例

```bash
python3 openclaw_memory.py --list-cases
```

#### 手动诊断

```bash
python3 openclaw_memory.py --fix "网关启动失败"
```

#### 检查配置

```bash
python3 openclaw_memory.py --check-config
```

---

## 🔧 配置

编辑配置文件：`~/.openclaw/skills/openclaw-iflow-doctor/config.json`

```json
{
  "version": "1.0.0",
  "auto_heal": true,           // 是否自动修复
  "enable_bat_generation": true, // 生成 BAT 工具
  "similarity_threshold": 0.85,  // 案例匹配阈值
  "iflow_memory": {
    "enabled": true,            // 启用 iflow 记忆
    "save_repair_records": true  // 保存维修记录
  }
}
```

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [QUICKSTART.md](QUICKSTART.md) | 5 分钟快速入门 |
| [USAGE_GUIDE.md](USAGE_GUIDE.md) | 完整使用指南 |
| [INSTALL_LINUX.md](INSTALL_LINUX.md) | Linux 安装指南 |
| [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) | Windows 安装指南 |
| [README_UPGRADE.md](README_UPGRADE.md) | 升级指南 |
| [PROJECT_PLAN.md](PROJECT_PLAN.md) | 项目方案（中文） |

---

## ❓ 常见问题

### Q: 安装后没反应？

**A**: 技能是自动触发的，只有 OpenClaw 出错时才会激活。

手动测试：
```bash
python3 openclaw_memory.py --stats
```

### Q: iflow 是什么？必须安装吗？

**A**: iflow 是 AI 助手，用于处理复杂问题。

- **简单问题**：技能自动修复（无需 iflow）
- **复杂问题**：技能提示调用 iflow

**推荐但不强制**。

### Q: 如何关闭自动修复？

**A**: 编辑 `config.json`：
```json
{
  "auto_heal": false
}
```

### Q: 支持哪些系统？

**A**: 全平台支持：
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu, CentOS, Debian 等)

### Q: 如何更新？

**A**: 
```bash
cd ~/.openclaw/skills/openclaw-iflow-doctor
git pull origin main
```

### Q: 旧版本用户升级需要清空数据吗？

**A**: **不需要！**

技能会自动：
- 保留你的维修记录（`records.json`）
- 保留你的配置（`config.json`）
- 兼容旧版本数据

建议备份（可选）：
```bash
cp ~/.openclaw/skills/openclaw-iflow-doctor/records.json ~/backup-records.json
```

---

## 🔄 升级指南

### 从 v0.x 升级到 v1.0.0

**无需清空数据！** 直接覆盖安装：

```bash
# 方式 1：Git 更新（推荐）
cd ~/.openclaw/skills/openclaw-iflow-doctor
git pull origin main

# 方式 2：重新安装
openclaw skills uninstall openclaw-iflow-doctor
openclaw skills install https://github.com/kosei-echo/openclaw-iflow-doctor
```

**数据会自动保留**：
- ✅ `records.json` - 维修记录
- ✅ `config.json` - 你的配置
- ✅ `cases.json` - 自定义案例

### 备份（可选但推荐）

```bash
cp -r ~/.openclaw/skills/openclaw-iflow-doctor \
      ~/backup-iflow-doctor-$(date +%Y%m%d)
```

---

## 🐛 问题反馈

### 1. 查看日志

```bash
tail -f ~/.openclaw/skills/openclaw-iflow-doctor/watchdog.log
```

### 2. 提交 Issue

访问：https://github.com/kosei-echo/openclaw-iflow-doctor/issues

提供以下信息：
- 问题描述
- 错误日志
- 系统信息（`openclaw --version`, `python3 --version`）

### 3. 社区支持

- Discord: https://discord.gg/clawd
- ClawHub: https://clawhub.com

---

## 📊 项目统计

- **代码量**: 7730 行
- **文件数**: 32 个
- **案例库**: 10 个预置方案
- **支持平台**: Windows/macOS/Linux
- **许可证**: MIT

---

## 🛣️ 路线图

### v1.0.0 (当前)
- ✅ AI 自动诊断修复
- ✅ 10 个预置案例
- ✅ 跨平台支持
- ✅ iflow 集成

### v1.1.0 (计划中)
- ⏳ 更多维修案例
- ⏳ 通知功能增强
- ⏳ Web 界面
- ⏳ 云端案例同步

---

## 🙏 致谢

- OpenClaw 社区
- iflow CLI 团队
- 所有贡献者

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

**Made with 🦞 by OpenClaw Community**

**最后更新**: 2026-02-28  
**版本**: v1.0.0
