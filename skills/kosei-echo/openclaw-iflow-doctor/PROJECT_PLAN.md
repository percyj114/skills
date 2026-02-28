# 🦞 OpenClaw Self-Healing System 项目方案

> **三端通用的 AI 自愈系统** - 让 OpenClaw 自己修复自己  
> **版本**: 1.0.0  
> **日期**: 2026-02-28  
> **作者**: OpenClaw Community

---

## 📋 目录

1. [项目概述](#1-项目概述)
2. [核心架构](#2-核心架构)
3. [功能模块](#3-功能模块)
4. [技术实现](#4-技术实现)
5. [安装部署](#5-安装部署)
6. [使用指南](#6-使用指南)
7. [运维监控](#7-运维监控)
8. [开发计划](#8-开发计划)
9. [风险评估](#9-风险评估)
10. [总结](#10-总结)

---

## 1. 项目概述

### 1.1 项目背景

OpenClaw 作为 AI 助手框架，在生产环境中会遇到以下问题：

1. **网关崩溃** - API 限额、配置错误、内存溢出
2. **配置损坏** - JSON 语法错误、字段缺失
3. **模型故障** - 连接失败、响应超时
4. **人工干预** - 需要手动重启、诊断、修复

**痛点**：
- 凌晨 3 点网关崩溃，被电话叫醒重启
- 配置错误导致服务不可用，排查耗时
- 重复性问题反复出现，没有经验积累

### 1.2 项目目标

**构建一个三端通用的 AI 自愈系统**：

1. ✅ **自动恢复** - 80% 的问题自动修复，无需人工干预
2. ✅ **三端支持** - macOS + Linux + Windows 统一体验
3. ✅ **智能诊断** - 基于案例库和 iflow CLI 的智能诊断
4. ✅ **通知集成** - 飞书/钉钉自动通知，国内友好
5. ✅ **经验积累** - 修复记录自动沉淀，越用越聪明

### 1.3 核心价值

| 价值维度 | 具体收益 |
|----------|----------|
| **减少停机时间** | 从小时级降至分钟级 |
| **降低运维成本** | 减少 80% 人工干预 |
| **提升稳定性** | 4 层防护架构，故障隔离 |
| **知识沉淀** | 案例库持续积累，团队共享 |

### 1.4 竞品对比

| 功能 | Ramsbaby/openclaw-self-healing | 我们的方案 | 优势 |
|------|-------------------------------|------------|------|
| **平台支持** | macOS + Linux | **macOS + Linux + Windows** | ✅ +1 平台 |
| **通知渠道** | Discord + Telegram | **飞书 + 钉钉** | ✅ 国内友好 |
| **通知配置** | 独立 webhook | **自动同步 OpenClaw** | ✅ 零配置 |
| **案例库** | ❌ 无 | **✅ 10 个预置案例** | ✅ 智能诊断 |
| **AI 引擎** | Claude CLI | **iflow CLI** | ✅ 多模态 |
| **生产验证** | ✅ 14 个事件 | ⚠️ 待验证 | ❌ 待完善 |

---

## 2. 核心架构

### 2.1 4 层自主恢复架构

```
┌─────────────────────────────────────────────────────────────┐
│ Level 1: KeepAlive ⚡ (0-30 秒)                              │
│ - 瞬间重启任何崩溃                                           │
│ - macOS: LaunchAgent                                        │
│ - Linux: systemd                                            │
│ - Windows: 任务计划程序                                      │
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

### 2.2 数据流架构

```
┌─────────────────────────────────────────────────────────────┐
│ OpenClaw Gateway                                            │
│ (被监控的服务)                                                │
└────────┬────────────────────────────────────────────────────┘
         │ 崩溃/异常
         ▼
┌─────────────────────────────────────────────────────────────┐
│ KeepAlive (Level 1)                                         │
│ - 操作系统级重启                                             │
│ - 0-30 秒响应                                                 │
└────────┬────────────────────────────────────────────────────┘
         │ 持续崩溃
         ▼
┌─────────────────────────────────────────────────────────────┐
│ Watchdog (Level 2)                                          │
│ - 健康检查脚本                                               │
│ - 指数退避重启                                               │
└────────┬────────────────────────────────────────────────────┘
         │ 30 分钟失败
         ▼
┌─────────────────────────────────────────────────────────────┐
│ AI Doctor (Level 3)                                         │
│ - 读取日志                                                    │
│ - 匹配案例库                                                  │
│ - iflow CLI 诊断                                              │
│ - 执行修复                                                    │
└────────┬────────────────────────────────────────────────────┘
         │ 修复失败
         ▼
┌─────────────────────────────────────────────────────────────┐
│ Human Alert (Level 4)                                       │
│ - 飞书/钉钉通知                                               │
│ - 附带诊断报告                                                │
│ - 等待人工干预                                                │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 文件结构

```
~/.openclaw/skills/openclaw-iflow-doctor/
├── SKILL.md                      # 技能定义（OpenClaw 识别）
├── notify.py                     # 通知模块（飞书/钉钉）
├── watchdog.py                   # 健康检查（跨平台）
├── openclaw_memory.py            # AI 医生（核心诊断）
├── config_checker.py             # 配置检查器
├── iflow_bridge.py               # iflow CLI 桥接器
├── cases.json                    # 案例库（10 个预置案例）
├── records.json                  # 历史记录（经验积累）
├── config.json                   # 技能配置
├── install.sh                    # 安装脚本（macOS/Linux）
├── install.bat                   # 安装脚本（Windows）
├── README.md                     # 用户文档
├── README_UPGRADE.md             # 升级指南
└── templates/
    ├── ai.openclaw.gateway.plist   # macOS LaunchAgent
    ├── openclaw-gateway.service    # Linux systemd
    └── gateway-keepalive.bat       # Windows 任务计划
```

---

## 3. 功能模块

### 3.1 KeepAlive 模块

**功能**：操作系统级的瞬间重启

| 平台 | 实现方式 | 响应时间 |
|------|----------|----------|
| macOS | LaunchAgent (.plist) | 0-10 秒 |
| Linux | systemd (.service) | 0-10 秒 |
| Windows | 任务计划程序 (.bat) | 0-30 秒 |

**配置示例**（macOS）：
```xml
<key>KeepAlive</key>
<dict>
    <key>Crashed</key>
    <true/>
    <key>SuccessfulExit</key>
    <false/>
</dict>
```

### 3.2 Watchdog 模块

**功能**：健康检查 + 指数退避重启

**核心逻辑**：
```python
# 健康检查
def check_gateway_health(self):
    response = requests.get("http://localhost:18789/health", timeout=5)
    return response.status_code == 200

# 指数退避
restart_delays = [10, 30, 90, 180, 600]  # 秒
```

**崩溃计数衰减**：
- 6 小时内连续崩溃 → 触发升级
- 6 小时无崩溃 → 计数器清零

### 3.3 AI Doctor 模块

**功能**：智能诊断 + 自动修复

**工作流程**：
```
1. 读取错误日志
2. 提取错误特征（error_signature）
3. 匹配案例库（cases.json）
4. 应用修复方案
5. 记录修复结果（records.json）
```

**案例库结构**：
```json
{
  "id": "CASE-002",
  "title": "Gateway Service Not Starting",
  "error_code": "GATEWAY_START_FAILED",
  "keywords": ["gateway", "start", "failed", "crash"],
  "solution": "1) 检查配置 2) 验证端口 3) 查看日志 4) 重启",
  "commands": [
    "openclaw config validate",
    "lsof -i :18789",
    "tail -50 ~/.openclaw/logs/gateway.log",
    "pkill -f openclaw-gateway; nohup openclaw gateway &"
  ],
  "success_rate": 0.90
}
```

### 3.4 通知模块

**功能**：自动检测 + 多渠道通知

**自动检测逻辑**：
```python
def check_channels(self):
    """检查 OpenClaw 渠道配置"""
    config = load_openclaw_config()
    return {
        "feishu": "feishu" in config.get("channels", {}),
        "dingtalk": "dingtalk" in config.get("channels", {})
    }

# 使用逻辑
if available["feishu"] or available["dingtalk"]:
    send_alert(...)  # 有配置才发送
else:
    pass  # 静默跳过，不报错
```

**通知模板**：
```markdown
## 🚨 OpenClaw Gateway 连续崩溃

**时间**: 2026-02-28 03:30:00
**级别**: CRITICAL

**详情**:
- 连续故障时间：35.2 分钟
- 崩溃次数：7 次（600 秒内）
- 最后成功检查：2026-02-28 02:55:00

**自动操作**:
1. 已尝试重启 Gateway
2. 已记录详细日志
3. 等待 AI 诊断修复

---
*OpenClaw Self-Healing System*
```

### 3.5 配置检查器

**功能**：启动前验证配置

**检查项**：
1. ✅ 配置文件存在
2. ✅ JSON 语法正确
3. ✅ 必需字段完整（支持新旧格式）
4. ✅ 模型可连接性
5. ✅ 端口可用性

**新旧格式兼容**：
```python
# 旧版格式
{
  "models": {
    "default": "volcengine/ark-code-latest"
  }
}

# 新版格式
{
  "models": {
    "mode": "merge",
    "providers": {
      "volcengine": { ... }
    }
  }
}

# 检查逻辑
has_old_format = config.get("models.default")
has_new_format = config.get("models.providers")
if not (has_old_format or has_new_format):
    error("缺少模型配置")
```

---

## 4. 技术实现

### 4.1 技术栈

| 组件 | 技术选型 | 说明 |
|------|----------|------|
| **核心语言** | Python 3.8+ | 跨平台兼容 |
| **KeepAlive** | LaunchAgent/systemd/任务计划 | 操作系统原生 |
| **健康检查** | requests + subprocess | HTTP + 进程监控 |
| **AI 诊断** | iflow CLI | 多模态/WebSearch |
| **通知** | OpenClaw message 工具 | 自动同步配置 |
| **配置管理** | JSON | 轻量易读 |

### 4.2 关键算法

#### 4.2.1 案例匹配算法

```python
def match_case(error_logs, cases):
    """匹配最相似的案例"""
    
    # 1. 提取错误特征
    error_signature = extract_signature(error_logs)
    
    # 2. 精确匹配（error_signature）
    for case in cases:
        if case["error_signature"] == error_signature:
            return case, 1.0
    
    # 3. 关键词匹配
    keywords = extract_keywords(error_logs)
    best_match = None
    best_score = 0
    
    for case in cases:
        score = len(set(keywords) & set(case["keywords"]))
        if score > best_score:
            best_score = score
            best_match = case
    
    # 4. 阈值判断
    if best_score >= SIMILARITY_THRESHOLD:
        return best_match, best_score / len(keywords)
    
    return None, 0
```

#### 4.2.2 指数退避算法

```python
def get_restart_delay(crash_count):
    """计算重启延迟（指数退避）"""
    
    delays = [10, 30, 90, 180, 600]  # 秒
    
    if crash_count >= len(delays):
        return delays[-1]  # 最大延迟
    
    return delays[crash_count]
```

#### 4.2.3 崩溃计数衰减

```python
def decay_crash_count(crash_times, window_seconds=21600):
    """衰减崩溃计数（6 小时窗口）"""
    
    now = datetime.now()
    cutoff = now - timedelta(seconds=window_seconds)
    
    # 只保留窗口内的崩溃记录
    return [t for t in crash_times if t > cutoff]
```

### 4.3 跨平台实现

#### 4.3.1 平台检测

```python
import sys

def detect_platform():
    if sys.platform == "darwin":
        return "macos"
    elif sys.platform == "win32":
        return "windows"
    else:
        return "linux"
```

#### 4.3.2 平台特定代码

```python
def restart_gateway(platform):
    if platform == "macos":
        subprocess.run(["launchctl", "kickstart", "-k", "ai.openclaw.gateway"])
    elif platform == "linux":
        subprocess.run(["systemctl", "restart", "openclaw-gateway"])
    elif platform == "windows":
        subprocess.run(["taskkill", "/F", "/IM", "node.exe"])
        subprocess.Popen(["openclaw", "gateway"])
```

---

## 5. 安装部署

### 5.1 前提条件

| 条件 | macOS | Linux | Windows |
|------|-------|-------|---------|
| **OpenClaw** | ✅ 已安装 | ✅ 已安装 | ✅ 已安装 |
| **Python** | 3.8+ | 3.8+ | 3.8+ |
| **jq** | 可选 | 可选 | 可选 |
| **权限** | 用户权限 | sudo | 管理员 |

### 5.2 安装步骤

#### macOS / Linux

```bash
# 1. 下载并运行安装脚本
curl -fsSL https://github.com/kosei-echo/openclaw-iflow-doctor/raw/main/install.sh | bash

# 2. 按提示配置通知（可选）
# - 飞书 webhook
# - 钉钉 webhook

# 3. 验证安装
python3 ~/.openclaw/skills/openclaw-iflow-doctor/notify.py test
python3 ~/.openclaw/skills/openclaw-iflow-doctor/watchdog.py --test
```

#### Windows

```powershell
# 1. 下载安装脚本
Invoke-WebRequest -Uri "https://github.com/kosei-echo/openclaw-iflow-doctor/raw/main/install.bat" -OutFile "$env:TEMP\install.bat"

# 2. 运行安装脚本
& "$env:TEMP\install.bat"

# 3. 验证安装
python %USERPROFILE%\.openclaw\skills\openclaw-iflow-doctor\notify.py test
```

### 5.3 配置说明

#### 通知配置（可选）

**方式 1：安装时配置**
```bash
# 安装脚本会提示
请输入飞书 webhook URL: https://open.feishu.cn/...
```

**方式 2：手动配置**
```bash
python3 ~/.openclaw/skills/openclaw-iflow-doctor/notify.py set-feishu "https://..."
```

**方式 3：自动同步**
```
无需配置！自动读取 OpenClaw 的 channels 配置
```

#### Watchdog 配置

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

## 6. 使用指南

### 6.1 日常使用

**查看状态**：
```bash
# 测试健康检查
python3 ~/.openclaw/skills/openclaw-iflow-doctor/watchdog.py --test

# 查看统计
openclaw skills run openclaw-iflow-doctor --stats

# 查看案例库
openclaw skills run openclaw-iflow-doctor --list-cases
```

**手动诊断**：
```bash
# 诊断问题
openclaw skills run openclaw-iflow-doctor --diagnose "Gateway 无法启动"

# 配置检查
openclaw skills run openclaw-iflow-doctor --check-config
```

### 6.2 故障处理流程

#### 场景 1：Gateway 崩溃

```
[系统] Gateway 崩溃
  ↓
[Level 1] KeepAlive 自动重启（0-30 秒）
  ↓
[成功] ✅ 服务恢复
```

#### 场景 2：配置损坏

```
[系统] Gateway 崩溃
  ↓
[Level 1] KeepAlive 重启 → 失败（配置错误）
  ↓
[Level 2] Watchdog 检测 → 尝试重启 5 次 → 失败
  ↓
[Level 3] AI Doctor 诊断 → 匹配 CASE-007 → 从备份恢复配置
  ↓
[成功] ✅ 服务恢复
```

#### 场景 3：未知错误

```
[系统] Gateway 崩溃
  ↓
[Level 1] KeepAlive → 失败
  ↓
[Level 2] Watchdog → 失败
  ↓
[Level 3] AI Doctor → 无匹配案例 → 失败
  ↓
[Level 4] 飞书/钉钉通知 → 等待人工干预
  ↓
[人工] 手动修复 → 记录到案例库
  ↓
[成功] ✅ 服务恢复 + 案例库更新
```

### 6.3 最佳实践

#### 1. 启用自动修复
```bash
openclaw skills config openclaw-iflow-doctor --set auto_heal=true
```

#### 2. 定期查看统计
```bash
# 每周查看
openclaw skills run openclaw-iflow-doctor --stats
```

#### 3. 积累案例
```bash
# 修复新问题后
openclaw skills run openclaw-iflow-doctor --add-case
```

#### 4. 配合 iflow 使用
```bash
# 复杂问题调用 iflow
iflow -p "分析这个错误日志：$(cat ~/.openclaw/logs/gateway.error.log)"
```

---

## 7. 运维监控

### 7.1 监控指标

| 指标 | 阈值 | 告警级别 |
|------|------|----------|
| **Gateway 响应时间** | > 5 秒 | Warning |
| **崩溃频率** | > 5 次/小时 | Error |
| **连续失败时间** | > 30 分钟 | Critical |
| **内存使用** | > 1GB | Warning |

### 7.2 日志位置

```
~/.openclaw/logs/
├── gateway.log              # Gateway 运行日志
├── gateway.error.log        # Gateway 错误日志
├── watchdog.log             # Watchdog 日志
├── notify_feishu.log        # 飞书通知记录
└── notify_dingtalk.log      # 钉钉通知记录
```

### 7.3 告警配置

**飞书告警**：
- 触发条件：Level 4 升级
- 通知内容：错误详情 + 诊断报告
- 通知对象：运维群/个人

**钉钉告警**：
- 触发条件：Level 4 升级
- 通知内容：错误详情 + 诊断报告
- 通知对象：运维群/个人

---

## 8. 开发计划

### 8.1 已完成（v1.0.0）

- ✅ 4 层自主恢复架构
- ✅ 三端支持（macOS/Linux/Windows）
- ✅ 飞书/钉钉通知集成
- ✅ 案例库系统（10 个预置案例）
- ✅ 配置检查器
- ✅ 安装脚本

### 8.2 待开发（v1.1.0）

| 功能 | 优先级 | 预计工时 |
|------|--------|----------|
| Docker 镜像 | P1 | 2 天 |
| Grafana 仪表盘 | P2 | 3 天 |
| Prometheus 指标 | P2 | 2 天 |
| 多节点支持 | P3 | 5 天 |

### 8.3 长期规划（v4.0.0）

- Kubernetes Operator
- AI 预测性维护
- 自动扩容
- 多集群管理

---

## 9. 风险评估

### 9.1 技术风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| **误判导致误操作** | 低 | 高 | 人工确认开关 |
| **通知失败** | 中 | 中 | 本地日志记录 |
| **案例库匹配错误** | 中 | 中 | 相似度阈值 |
| **跨平台兼容性** | 低 | 中 | 充分测试 |

### 9.2 运维风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| **无限重启循环** | 低 | 高 | 崩溃计数衰减 |
| **资源耗尽** | 低 | 高 | 资源限制 |
| **配置覆盖** | 中 | 中 | 备份机制 |

### 9.3 应对措施

#### 无限重启循环保护
```python
# 最大重启次数限制
MAX_RESTARTS = 5

# 崩溃窗口衰减
crash_times = decay_crash_count(crash_times, window_seconds=21600)

# 达到阈值后停止自动重启
if len(crash_times) >= MAX_RESTARTS:
    trigger_escalation()  # 升级到人工干预
```

#### 配置备份机制
```bash
# 修复前自动备份
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d%H%M%S)
```

---

## 10. 总结

### 10.1 项目亮点

1. **三端通用** - macOS + Linux + Windows 统一体验
2. **智能自愈** - 4 层架构，80% 问题自动修复
3. **国内友好** - 飞书/钉钉集成，无需魔法
4. **零配置** - 自动同步 OpenClaw 配置
5. **经验积累** - 案例库持续学习，越用越聪明

### 10.2 核心价值

```
Before: 凌晨 3 点被电话叫醒 → 手动重启 → 排查 1 小时 → 疲惫不堪

After:  凌晨 3 点网关崩溃 → 自动修复 → 早上收到通知 → 继续睡觉 😴
```

### 10.3 下一步行动

1. **生产验证** - 在真实环境部署，积累数据
2. **文档完善** - 补充 CHANGELOG 和详细文档
3. **社区发布** - 发布到 ClawHub，收集反馈
4. **持续迭代** - 根据反馈优化功能

---

## 附录

### A. 快速命令参考

```bash
# 安装
curl -fsSL https://.../install.sh | bash

# 测试
python3 ~/.openclaw/skills/openclaw-iflow-doctor/notify.py test
python3 ~/.openclaw/skills/openclaw-iflow-doctor/watchdog.py --test

# 诊断
openclaw skills run openclaw-iflow-doctor --diagnose "问题描述"

# 统计
openclaw skills run openclaw-iflow-doctor --stats

# 配置检查
openclaw skills run openclaw-iflow-doctor --check-config
```

### B. 故障排查清单

```bash
# 1. 检查 Gateway 状态
curl http://localhost:18789/health

# 2. 查看日志
tail -50 ~/.openclaw/logs/gateway.log

# 3. 测试通知
python3 ~/.openclaw/skills/openclaw-iflow-doctor/notify.py test

# 4. 检查配置
python3 ~/.openclaw/skills/openclaw-iflow-doctor/config_checker.py

# 5. 手动重启
pkill -f openclaw-gateway; nohup openclaw gateway &
```

### C. 相关链接

- **GitHub**: https://github.com/kosei-echo/openclaw-iflow-doctor
- **OpenClaw**: https://github.com/openclaw/openclaw
- **iFlow CLI**: https://github.com/iflow-ai/iflow-cli
- **ClawHub**: https://clawhub.com

---

**文档版本**: 1.0  
**最后更新**: 2026-02-28  
**维护者**: OpenClaw Community

*"最好的系统是在你注意到之前就自我修复的系统"*
