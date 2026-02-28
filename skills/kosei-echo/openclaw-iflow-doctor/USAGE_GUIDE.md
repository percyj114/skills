# 🦞 OpenClaw iFlow Doctor - 完整使用指南

> **AI 驱动的 OpenClaw 自我修复系统**  
> 版本：v1.0.0 | 适用：OpenClaw 用户（新手友好）

---

## 📖 目录

1. [这是什么？](#这是什么)
2. [使用前准备](#使用前准备)
3. [安装步骤](#安装步骤)
4. [使用方法](#使用方法)
5. [常见问题](#常见问题)
6. [升级指南](#升级指南)
7. [技术支持](#技术支持)

---

## 这是什么？

**OpenClaw iFlow Doctor** 是一个智能自我修复技能，能让你的 OpenClaw 在出问题时**自动诊断和修复**。

### 它能做什么？

✅ **自动修复** - 80% 的常见问题自动解决  
✅ **智能诊断** - 识别 8 种问题类型（记忆、网关、配置、网络等）  
✅ **案例库匹配** - 10 个预置解决方案，越用越聪明  
✅ **iflow 集成** - 复杂问题自动调用 iflow CLI 协助  
✅ **跨平台** - Windows、macOS、Linux 都支持

### 工作原理

```
OpenClaw 出错
    ↓
自动捕获错误
    ↓
搜索案例库 → 找到匹配方案 → 自动修复 ✓
    ↓
找不到方案 → 生成诊断报告 → 提示调用 iflow
    ↓
iflow CLI 协助 → 修复完成 → 保存到案例库
```

---

## 使用前准备

### 前提条件

请确保你已经完成以下步骤：

#### 1. ✅ 安装 OpenClaw

**检查 OpenClaw 是否已安装**：
```bash
openclaw --version
```

**如果未安装**，访问官网安装：
- 官网：https://docs.openclaw.ai
- GitHub: https://github.com/openclaw/openclaw

#### 2. ✅ 配置 OpenClaw

确保 OpenClaw 能正常运行：
```bash
# 检查配置
openclaw config list

# 启动网关测试
openclaw gateway start
```

如果网关能正常启动，说明配置完成 ✅

#### 3. ✅ 安装 iflow（可选但推荐）

iflow 是一个 AI 助手，用于处理复杂问题：

```bash
# 检查 iflow 是否安装
iflow --version

# 如果未安装，执行：
npm install -g iflow

# 登录 iflow
iflow login
```

**注意**：iflow 是可选的，但安装后能获得更好的修复体验。

---

## 安装步骤

### 方式 1：从 GitHub 安装（推荐）

#### 步骤 1：复制安装命令

```bash
openclaw skills install https://github.com/kosei-echo/openclaw-iflow-doctor
```

#### 步骤 2：在终端执行

打开终端（命令提示符/PowerShell/终端），粘贴上面的命令并回车。

#### 步骤 3：等待安装完成

你会看到类似输出：
```
✓ Downloading skill...
✓ Installing files...
✓ Skill installed successfully!
✓ Location: ~/.openclaw/skills/openclaw-iflow-doctor
```

#### 步骤 4：验证安装

```bash
# 检查技能是否安装成功
openclaw skills list | grep iflow-doctor

# 测试技能功能
cd ~/.openclaw/skills/openclaw-iflow-doctor
python3 openclaw_memory.py --stats
```

看到统计信息说明安装成功 ✅

### 方式 2：本地安装（无网络时）

如果你已经下载了技能文件：

```bash
# 复制技能文件到 OpenClaw 技能目录
cp -r /path/to/openclaw-iflow-doctor \
      ~/.openclaw/skills/openclaw-iflow-doctor

# 验证安装
openclaw skills list | grep iflow-doctor
```

---

## 使用方法

### 自动模式（推荐）

安装后**无需任何配置**，技能会自动工作！

#### 场景 1：OpenClaw 网关崩溃

```
[系统] OpenClaw gateway crashed
[系统] iFlow Doctor: 检测到网关崩溃
[系统] iFlow Doctor: 正在搜索案例库...
[系统] iFlow Doctor: 找到匹配方案 (CASE-002)
[系统] iFlow Doctor: 正在重启网关服务...
[系统] ✓ 网关已重启
[系统] 修复报告：~/.openclaw/skills/openclaw-iflow-doctor/reports/修复报告_20260228.txt
```

**你需要做的**：查看报告，无需操作 ✅

#### 场景 2：记忆功能损坏

```
[系统] Memory search failed
[系统] iFlow Doctor: 检测到记忆搜索失败
[系统] iFlow Doctor: 正在搜索案例库...
[系统] iFlow Doctor: 找到匹配方案 (CASE-001)
[系统] iFlow Doctor: 正在重置记忆索引...
[系统] ✓ 记忆索引已重置
[系统] 功能已恢复
```

#### 场景 3：复杂问题（需要 iflow 协助）

```
[系统] Configuration file corrupted
[系统] iFlow Doctor: 检测到配置文件损坏
[系统] iFlow Doctor: 搜索案例库... 无匹配
[系统] iFlow Doctor: 搜索历史记录... 无匹配
[系统] iFlow Doctor: ✗ 无法自动修复
[系统] iFlow Doctor: 已生成诊断报告
[系统] iFlow Doctor: 💡 建议：双击桌面上的"打开 iFlow 寻求帮助.bat"
[系统]          或运行：iflow
```

**你需要做的**：
1. 双击桌面上的 `打开 iFlow 寻求帮助.bat`（Windows）
2. 或在终端输入 `iflow`
3. 描述问题，iflow 会协助修复

### 手动模式

#### 查看技能统计

```bash
cd ~/.openclaw/skills/openclaw-iflow-doctor
python3 openclaw_memory.py --stats
```

输出示例：
```
=== OpenClaw Memory Statistics ===
Total cases: 10
Total records: 0
Total calls: 0
```

#### 查看维修案例库

```bash
python3 openclaw_memory.py --list-cases
```

输出示例：
```
=== Repair Case Library ===
[CASE-001] Memory Search Function Broken
   Success Rate: 85%
   Keywords: memory, search, broken

[CASE-002] Gateway Service Not Starting
   Success Rate: 90%
   Keywords: gateway, start, crash
...
```

#### 手动诊断问题

```bash
python3 openclaw_memory.py --fix "网关启动失败"
```

#### 检查配置

```bash
python3 openclaw_memory.py --check-config
```

---

## 常见问题

### Q1: 安装后没反应？

**A**: 技能是自动触发的，只有 OpenClaw 出错时才会激活。

你可以手动测试：
```bash
cd ~/.openclaw/skills/openclaw-iflow-doctor
python3 openclaw_memory.py --stats
```

### Q2: 如何知道技能是否在工作？

**A**: 查看日志文件：
```bash
# Linux/macOS
tail -f ~/.openclaw/skills/openclaw-iflow-doctor/watchdog.log

# Windows (PowerShell)
Get-Content ~/.openclaw/skills/openclaw-iflow-doctor/watchdog.log -Tail 50 -Wait
```

### Q3: iflow 是什么？必须安装吗？

**A**: iflow 是一个 AI 助手，用于处理复杂问题。

- **简单问题**：技能自动修复（无需 iflow）
- **复杂问题**：技能会提示你调用 iflow 协助

**推荐安装**，但不是必须的。

### Q4: 技能会修改我的配置文件吗？

**A**: 会，但很安全：

1. 修改前会**自动备份**
2. 只修改有问题的配置项
3. 所有修改都会记录在修复报告中

### Q5: 如何关闭自动修复？

**A**: 编辑配置文件：
```bash
# 打开配置
nano ~/.openclaw/skills/openclaw-iflow-doctor/config.json

# 修改这一行：
{
  "auto_heal": false
}
```

### Q6: 技能支持哪些操作系统？

**A**: 全平台支持：
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu, CentOS, Debian 等)

### Q7: 如何更新技能？

**A**: 见下方 [升级指南](#升级指南)

---

## 升级指南

### 从旧版本升级

如果你之前安装过旧版本（如 v0.x），建议**先备份再升级**：

#### 步骤 1：备份现有数据

```bash
# 备份维修记录
cp ~/.openclaw/skills/openclaw-iflow-doctor/records.json \
   ~/backup-records-$(date +%Y%m%d).json

# 备份配置
cp ~/.openclaw/skills/openclaw-iflow-doctor/config.json \
   ~/backup-config-$(date +%Y%m%d).json
```

#### 步骤 2：卸载旧版本

```bash
openclaw skills uninstall openclaw-iflow-doctor
```

#### 步骤 3：安装新版本

```bash
openclaw skills install https://github.com/kosei-echo/openclaw-iflow-doctor
```

#### 步骤 4：恢复数据（可选）

如果你想保留旧的维修记录：
```bash
cp ~/backup-records-*.json \
   ~/.openclaw/skills/openclaw-iflow-doctor/records.json
```

### 从 GitHub 更新

如果技能已安装，更新到最新版本：

```bash
cd ~/.openclaw/skills/openclaw-iflow-doctor
git pull origin main
```

---

## 技术支持

### 遇到问题？

#### 1. 查看官方文档

- GitHub 仓库：https://github.com/kosei-echo/openclaw-iflow-doctor
- 问题反馈：https://github.com/kosei-echo/openclaw-iflow-doctor/issues

#### 2. 使用 iflow 求助

```bash
# Windows
双击桌面上的 "打开 iFlow 寻求帮助.bat"

# macOS/Linux
iflow
```

#### 3. 联系社区

- OpenClaw Discord: https://discord.gg/clawd
- 社区论坛：https://clawhub.com

### 提交问题报告

在 GitHub 提交 Issue 时，请提供以下信息：

1. **问题描述**：详细说明了什么问题
2. **错误日志**：`~/.openclaw/logs/gateway.log`
3. **修复报告**：`~/.openclaw/skills/openclaw-iflow-doctor/reports/`
4. **系统信息**：
   ```bash
   openclaw --version
   python3 --version
   iflow --version  # 如果安装了
   ```

---

## 附录：文件结构

```
~/.openclaw/skills/openclaw-iflow-doctor/
├── SKILL.md              # 技能定义
├── openclaw_memory.py    # 主程序
├── config.json           # 配置文件
├── cases.json            # 维修案例库
├── records.json          # 维修记录
├── watchdog.py           # 健康监控
├── config_checker.py     # 配置检查器
├── iflow_bridge.py       # iflow 集成
├── notify.py             # 通知模块
├── install.py            # 安装脚本
├── heal.sh / heal.bat    # 快速启动
├── README.md             # 使用说明
└── templates/            # 系统模板
    ├── ai.openclaw.gateway.plist    # macOS
    ├── openclaw-gateway.service     # Linux
    └── gateway-keepalive.bat        # Windows
```

---

## 版本历史

### v1.0.0 (2026-02-28) - 初始发布

- ✅ AI 自动诊断修复
- ✅ 10 个预置维修案例
- ✅ 跨平台支持（Windows/macOS/Linux）
- ✅ iflow 深度集成
- ✅ 4 层恢复架构

---

**Made with 🦞 by OpenClaw Community**

**许可证**: MIT  
**最后更新**: 2026-02-28
