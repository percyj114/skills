# Kim 消息发送 Skill 🤖

快手 Kim 即时通讯消息发送 AI Skill，支持 Webhook 和消息号两种方式。

适用于向 Kim 推送通知、告警、日报等场景。

## 📱 什么是 Kim？

Kim 是快手的企业即时通讯工具，官网：https://kim.kuaishou.com/

## 🚀 支持的 AI 平台

| 平台 | 支持 |
|------|------|
| OpenClaw | ✅ |
| Cursor | ✅ |
| Claude Code | ✅ |
| VS Code AI | ✅ |
| 其他能执行命令的 AI | ✅ |

## 📦 安装方式

### 方式一：OpenClaw / ClawHub

```bash
clawhub install kim-msg
```

### 方式二：GitHub 克隆

```bash
git clone https://github.com/LeeGoDamn/kim-msg-skill.git
```

## ⚙️ 配置

### 方式一：Webhook（向群聊发消息）

需要获取 Kim 机器人的 Webhook Token，设置环境变量：

```bash
export KIM_WEBHOOK_TOKEN="your-webhook-token"
```

### 方式二：消息号（向指定用户发消息）

需要获取 Kim 应用的 appKey 和 secretKey：

```bash
export KIM_APP_KEY="your-app-key"
export KIM_SECRET_KEY="your-secret-key"
```

## 📖 使用方法

### Webhook 方式

```bash
# 发送 Markdown 消息到群聊
./scripts/webhook.sh "**标题**\n\n正文内容"

# 发送纯文本
./scripts/webhook.sh "Hello World" --text
```

### 消息号方式

```bash
# 发送消息给指定用户（必须是邮箱前缀，如 wangyang）
./scripts/message.sh -u wangyang -m "**提醒**：今天有会议"
```

## 🔐 安全提示

- **不要硬编码密钥** - 所有凭证通过环境变量传递
- **敏感信息不上传** - 密钥只存在于本地，不会发布到仓库

## 📝 License

MIT

---

Made with ❤️ by [LeeGoDamn](https://github.com/LeeGoDamn)
