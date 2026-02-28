# 🚀 5 分钟快速入门

> OpenClaw iFlow Doctor - 让 OpenClaw 自我修复！

---

## 第一步：检查前提条件

### 1. 确认 OpenClaw 已安装

```bash
openclaw --version
```

看到版本号 ✅ 继续下一步  
看不到 ❌ 先安装 OpenClaw：https://docs.openclaw.ai

### 2. 确认 OpenClaw 能运行

```bash
openclaw gateway start
```

能启动 ✅ 继续下一步  
不能启动 ❌ 先配置好 OpenClaw

### 3. 检查 iflow（可选）

```bash
iflow --version
```

看到版本号 ✅ 太好了！  
看不到 ❌ 没关系，技能也能工作（推荐安装：`npm install -g iflow`）

---

## 第二步：安装技能

### 一行命令搞定：

```bash
openclaw skills install https://github.com/kosei-echo/openclaw-iflow-doctor
```

### 等待安装完成

你会看到：
```
✓ Downloading skill...
✓ Installing files...
✓ Skill installed successfully!
```

### 验证安装成功

```bash
openclaw skills list | grep iflow-doctor
```

看到 `openclaw-iflow-doctor` ✅ 安装成功！

---

## 第三步：什么都不用做！

技能会**自动工作**，无需配置！

### 当 OpenClaw 出问题时：

**简单问题** → 技能自动修复 → 你收到修复报告 ✅

**复杂问题** → 技能生成诊断报告 → 提示你调用 iflow → iflow 协助修复 ✅

---

## 常用命令

### 查看技能状态

```bash
cd ~/.openclaw/skills/openclaw-iflow-doctor
python3 openclaw_memory.py --stats
```

### 查看维修案例

```bash
python3 openclaw_memory.py --list-cases
```

### 手动诊断问题

```bash
python3 openclaw_memory.py --fix "描述你的问题"
```

### 查看修复报告

```bash
ls -lh ~/.openclaw/skills/openclaw-iflow-doctor/reports/
```

---

## 遇到问题？

### 1. 查看日志

```bash
tail -f ~/.openclaw/skills/openclaw-iflow-doctor/watchdog.log
```

### 2. 调用 iflow 求助

```bash
iflow
```

### 3. 提交 Issue

https://github.com/kosei-echo/openclaw-iflow-doctor/issues

---

## 技能能修复什么？

| 问题类型 | 自动修复 | 成功率 |
|---------|---------|--------|
| 记忆搜索失败 | ✅ | 85% |
| 网关启动失败 | ✅ | 90% |
| API 额度超限 | ❌ 需充值 | - |
| 配置文件损坏 | ✅ | 85% |
| 网络连接问题 | ✅ | 80% |
| Agent 生成失败 | ✅ | 80% |
| 权限错误 | ✅ | 85% |

---

## 升级技能

```bash
cd ~/.openclaw/skills/openclaw-iflow-doctor
git pull origin main
```

---

**就这么简单！** 🎉

技能会自动保护你的 OpenClaw，让你睡个安稳觉～

---

**Made with 🦞 by OpenClaw Community**
