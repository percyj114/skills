# 📝 ClawHub 发布指南

## 🔐 步骤 1：获取 ClawHub Token

### 访问 ClawHub
1. 打开浏览器
2. 访问：https://clawhub.ai/
3. 登录你的 GitHub 账号

### 生成 Token
1. 登录后，点击右上角头像
2. 选择 **Settings**（设置）
3. 找到 **API Tokens** 或 **CLI Tokens**
4. 点击 **Generate New Token**
5. 复制生成的 Token（格式：`clh_xxxxxxxx`）

---

## 🚀 步骤 2：配置 Token

### 方式 1：环境变量（推荐）
```bash
export CLAWDHUB_TOKEN="clh_你的 token"
```

### 方式 2：配置文件
```bash
mkdir -p ~/.clawhub
echo "CLAWDHUB_TOKEN=clh_你的 token" > ~/.clawhub/.env
```

---

## 📦 步骤 3：发布技能

### 验证登录
```bash
clawdhub whoami
```

看到用户名 ✅ 登录成功

### 发布技能
```bash
cd /root/.openclaw/skills/openclaw-iflow-doctor

clawdhub publish . \
  --slug openclaw-iflow-doctor \
  --name "OpenClaw iFlow Doctor" \
  --version 1.0.0 \
  --changelog "Initial release: AI-powered auto-repair system" \
  --tags "latest,ai,self-healing,iflow"
```

---

## ✅ 步骤 4：验证发布

访问：https://clawhub.ai/skills/openclaw-iflow-doctor

---

## 📋 快速命令

```bash
# 设置 Token
export CLAWDHUB_TOKEN="clh_你的 token"

# 验证
clawdhub whoami

# 发布
cd /root/.openclaw/skills/openclaw-iflow-doctor
clawdhub publish . --slug openclaw-iflow-doctor --name "OpenClaw iFlow Doctor" --version 1.0.0 --changelog "Initial release" --tags "latest"
```

---

## ❓ 遇到问题？

### Token 过期
重新生成 Token 并更新环境变量

### 权限错误
确保 Token 有发布权限

### 网络错误
检查网络连接

---

**Made with 🦞 by OpenClaw Community**
