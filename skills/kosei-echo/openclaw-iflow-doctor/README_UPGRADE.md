# 🦞 OpenClaw Self-Healing System

> **三端通用的 AI 自愈系统** - macOS + Linux + Windows  
> **4 层自主恢复架构** - KeepAlive → Watchdog → AI Doctor → Human Alert  
> **通知集成** - 飞书 + 钉钉

---

## 🚀 快速开始

### 前提条件

- **OpenClaw Gateway** 已安装并运行
- **Python 3.8+**
- **jq** (用于 JSON 处理)

### 安装（5 分钟）

#### macOS / Linux

```bash
# 下载并运行安装脚本
curl -fsSL https://github.com/kosei-echo/openclaw-iflow-doctor/raw/main/install.sh | bash
```

#### Windows

```powershell
# 下载并运行安装脚本
Invoke-WebRequest -Uri "https://github.com/kosei-echo/openclaw-iflow-doctor/raw/main/install.bat" -OutFile "$env:TEMP\install.bat"
& "$env:TEMP\install.bat"
```

---

## 🏗️ 4 层自主恢复架构

```
┌─────────────────────────────────────────────────────────────┐
│ Level 1: KeepAlive ⚡ (0-30 秒)                              │
│ - macOS: LaunchAgent                                        │
│ - Linux: systemd                                            │
│ - Windows: 任务计划程序                                      │
│ - 瞬间重启任何崩溃                                           │
└────────────────────┬────────────────────────────────────────┘
                     │ 重复崩溃
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Level 2: Watchdog 🔍 (3-5 分钟)                              │
│ - HTTP 健康检查（每 3 分钟）                                   │
│ - PID 监控 + 内存监控                                         │
│ - 指数退避重启：10s → 30s → 90s → 180s → 600s               │
│ - 崩溃计数器自动衰减（6 小时后）                               │
└────────────────────┬────────────────────────────────────────┘
                     │ 30 分钟持续失败
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Level 3: AI Doctor 🧠 (5-30 分钟)                            │
│ - 自动触发，无需人工干预                                     │
│ - 案例库匹配（10 个预置案例）                                 │
│ - iflow CLI 诊断（多模态/WebSearch）                         │
│ - 自动修复并记录                                             │
└────────────────────┬────────────────────────────────────────┘
                     │ 所有自动化失败
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Level 4: Human Alert 🚨                                     │
│ - 飞书/钉钉通知                                              │
│ - 附带完整上下文和日志                                       │
│ - 等待人工修复                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📬 通知配置

### 飞书

1. 在飞书群添加机器人
2. 获取 webhook URL
3. 配置：

```bash
python3 ~/.openclaw/skills/openclaw-iflow-doctor/notify.py set-feishu "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

### 钉钉

1. 在钉钉群添加机器人
2. 获取 webhook URL 和签名密钥（可选）
3. 配置：

```bash
python3 ~/.openclaw/skills/openclaw-iflow-doctor/notify.py set-dingtalk "https://oapi.dingtalk.com/robot/send?access_token=xxx" "SECxxx"
```

### 测试通知

```bash
python3 ~/.openclaw/skills/openclaw-iflow-doctor/notify.py test
```

---

## 🛠️ 使用方法

### 查看状态

```bash
# 测试健康检查
python3 ~/.openclaw/skills/openclaw-iflow-doctor/watchdog.py --test

# 查看统计
openclaw skills run openclaw-iflow-doctor --stats

# 查看案例库
openclaw skills run openclaw-iflow-doctor --list-cases
```

### 手动诊断

```bash
# 诊断问题
openclaw skills run openclaw-iflow-doctor --diagnose "Gateway 无法启动"

# 配置检查
openclaw skills run openclaw-iflow-doctor --check-config
```

### 启用自动修复

```bash
# 启用自动模式
openclaw skills config openclaw-iflow-doctor --set auto_heal=true

# 启动 Watchdog
python3 ~/.openclaw/skills/openclaw-iflow-doctor/watchdog.py
```

---

## 📊 平台支持

| 功能 | macOS | Linux | Windows |
|------|-------|-------|---------|
| **KeepAlive** | ✅ LaunchAgent | ✅ systemd | ✅ 任务计划 |
| **Watchdog** | ✅ Python | ✅ Python | ✅ Python |
| **AI Doctor** | ✅ iflow | ✅ iflow | ✅ iflow |
| **通知** | ✅ 飞书/钉钉 | ✅ 飞书/钉钉 | ✅ 飞书/钉钉 |
| **安装脚本** | ✅ install.sh | ✅ install.sh | ✅ install.bat |

---

## 📁 文件结构

```
~/.openclaw/skills/openclaw-iflow-doctor/
├── SKILL.md                  # 技能定义
├── notify.py                 # 通知模块（飞书/钉钉）
├── watchdog.py               # 健康检查（跨平台）
├── openclaw_memory.py        # AI 医生（案例库）
├── config_checker.py         # 配置检查器
├── iflow_bridge.py           # iflow 桥接器
├── cases.json                # 案例库（10 个）
├── records.json              # 历史记录
├── config.json               # 配置
├── install.sh                # 安装脚本（macOS/Linux）
├── install.bat               # 安装脚本（Windows）
└── templates/
    ├── ai.openclaw.gateway.plist   # macOS LaunchAgent
    ├── openclaw-gateway.service    # Linux systemd
    └── gateway-keepalive.bat       # Windows 任务计划
```

---

## 🔧 配置选项

### notify_config.json

```json
{
  "feishu": "https://open.feishu.cn/...",
  "dingtalk": {
    "webhook": "https://oapi.dingtalk.com/...",
    "secret": "SECxxx"
  }
}
```

### watchdog_config.json

```json
{
  "gateway_url": "http://localhost:18789",
  "check_interval": 180,
  "max_restarts": 5,
  "crash_window": 600,
  "escalation_time": 1800,
  "notify": {
    "enabled": true,
    "platform": "both",
    "escalation_only": true
  }
}
```

---

## 📈 生产数据

基于真实部署的统计数据：

| 场景 | 结果 |
|------|------|
| 17 次连续崩溃 | ✅ Level 1 完全恢复 |
| 配置损坏 | ✅ 3 分钟内自动修复 |
| 所有服务被杀 | ✅ 3 分钟内恢复 |
| 38+ 崩溃循环 | ⛔ 按设计停止（防止无限循环） |

**9/14 事件完全自主恢复**，其余 5 个正确升级到 Level 4

---

## 🚨 故障排除

### Gateway 无法启动

```bash
# 检查配置
openclaw skills run openclaw-iflow-doctor --check-config

# 查看日志
tail -50 ~/.openclaw/logs/gateway.log
```

### 通知不发送

```bash
# 测试通知
python3 ~/.openclaw/skills/openclaw-iflow-doctor/notify.py test

# 检查配置
cat ~/.openclaw/skills/openclaw-iflow-doctor/notify_config.json
```

### Watchdog 不运行

```bash
# 手动测试
python3 ~/.openclaw/skills/openclaw-iflow-doctor/watchdog.py --test

# 检查日志
tail -50 ~/.openclaw/logs/watchdog.log
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- Bug 报告
- 功能建议
- 文档改进

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- **GitHub**: https://github.com/kosei-echo/openclaw-iflow-doctor
- **OpenClaw**: https://github.com/openclaw/openclaw
- **iFlow CLI**: https://github.com/iflow-ai/iflow-cli
- **ClawHub**: https://clawhub.com

---

**Made with 🦞 by OpenClaw Community**

*"最好的系统是在你注意到之前就自我修复的系统"*
