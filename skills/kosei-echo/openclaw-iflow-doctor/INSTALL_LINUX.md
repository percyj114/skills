# OpenClaw iFlow Doctor - Linux/macOS 安装指南

## 📋 系统要求

- Python 3.8 或更高版本
- OpenClaw CLI 已安装
- Bash shell (Linux/macOS)

## 🚀 快速安装

### 1. 下载并解压

```bash
# 进入下载目录
cd /tmp

# 解压 (如果使用 zip)
unzip openclaw-iflow-doctor.zip -d openclaw-iflow-doctor

# 或解压 tar.gz
tar -xzf openclaw-iflow-doctor.tar.gz
```

### 2. 运行安装脚本

```bash
cd /tmp/openclaw-iflow-doctor

# 方式1: 使用交互式安装
python3 install.py

# 方式2: 直接运行 (无需安装)
python3 openclaw_memory.py
```

### 3. 添加到 PATH (可选)

```bash
# 创建符号链接到 /usr/local/bin
sudo ln -sf /tmp/openclaw-iflow-doctor/openclaw_memory.py /usr/local/bin/openclaw-doctor
sudo chmod +x /usr/local/bin/openclaw-doctor

# 现在可以直接运行
openclaw-doctor --help
```

## 🔧 手动安装

如果自动安装失败，可以手动安装:

```bash
# 1. 创建目录
mkdir -p ~/.openclaw/skills/openclaw-iflow-doctor

# 2. 复制文件
cp -r /tmp/openclaw-iflow-doctor/* ~/.openclaw/skills/openclaw-iflow-doctor/

# 3. 添加执行权限
chmod +x ~/.openclaw/skills/openclaw-iflow-doctor/heal.sh

# 4. 创建快捷方式
ln -sf ~/.openclaw/skills/openclaw-iflow-doctor/heal.sh ~/bin/openclaw-heal 2>/dev/null || \
    echo "alias openclaw-heal='~/.openclaw/skills/openclaw-iflow-doctor/heal.sh'" >> ~/.bashrc
```

## 🎯 使用方法

### 方式1: 使用 heal.sh (推荐)

```bash
# 进入目录
cd /tmp/openclaw-iflow-doctor

# 运行修复脚本
./heal.sh
```

### 方式2: 直接使用 Python

```bash
cd /tmp/openclaw-iflow-doctor

# 自动诊断并修复
python3 openclaw_memory.py --auto-fix

# 仅诊断
python3 openclaw_memory.py --diagnose-only

# 生成修复脚本
python3 openclaw_memory.py --generate-scripts

# 查看帮助
python3 openclaw_memory.py --help
```

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `openclaw_memory.py` | 主程序 |
| `heal.sh` | Linux/macOS 一键修复脚本 |
| `cases.json` | 修复案例库 |
| `config.json` | 配置文件 |
| `records.json` | 修复记录 (自动生成) |

## 🔧 支持的修复场景

- **CASE-001**: 记忆搜索功能损坏
- **CASE-002**: Gateway 服务无法启动
- **CASE-003**: API 速率限制
- **CASE-004**: Agent 启动失败
- **CASE-005**: 频道配置错误
- **CASE-006**: 模型提供商连接失败
- **CASE-007**: 配置文件损坏
- **CASE-008**: 多 Agent 冲突
- **CASE-009**: 权限被拒绝
- **CASE-010**: 日志文件过大

## 🐛 故障排除

### Python 未找到

```bash
# 检查 Python 版本
python3 --version

# 如果未安装
# Ubuntu/Debian:
sudo apt update && sudo apt install python3

# CentOS/RHEL:
sudo yum install python3

# macOS:
brew install python3
```

### 权限问题

```bash
# 添加执行权限
chmod +x heal.sh
chmod +x openclaw_memory.py

# 修复目录权限
chmod -R u+rw ~/.openclaw
```

### 依赖缺失

```bash
# 安装常见依赖
pip3 install --user requests
```

## 📝 配置说明

编辑 `config.json`:

```json
{
  "enable_bat_generation": false,
  "enable_txt_report": true,
  "similarity_threshold": 0.85,
  "watchdog": {
    "enabled": true,
    "check_interval": 1,
    "crash_threshold": 5
  },
  "alert": {
    "enabled": false,
    "dingtalk_webhook": "",
    "lark_webhook": "",
    "discord_webhook": ""
  },
  "iflow_memory": {
    "enabled": true,
    "save_repair_records": true
  }
}
```

**配置说明：**
- `watchdog.enabled` - 是否启用进程监控
- `watchdog.check_interval` - 检查间隔（秒，默认1秒）
- `watchdog.crash_threshold` - 崩溃阈值（默认5次）
- `alert.enabled` - 是否启用告警通知
- `alert.dingtalk_webhook` - 钉钉机器人 Webhook 地址
- `alert.lark_webhook` - 飞书机器人 Webhook 地址
- `alert.discord_webhook` - Discord Webhook 地址
- `iflow_memory.enabled` - 是否启用 iFlow 记忆功能
- `iflow_memory.save_repair_records` - 是否保存修复记录

## 🆘 获取帮助

```bash
# 查看帮助
python3 openclaw_memory.py --help

# 查看版本
python3 openclaw_memory.py --version

# 测试运行 (不执行实际修复)
python3 openclaw_memory.py --dry-run
```

## 📄 日志位置

- 修复记录: `./records.json`
- 调用日志: `./call_logs.json`
- 报告文件: `./repair_report_*.txt`

## 🔄 卸载

```bash
# 删除安装目录
rm -rf /tmp/openclaw-iflow-doctor
rm -rf ~/.openclaw/skills/openclaw-iflow-doctor

# 删除快捷方式
rm -f /usr/local/bin/openclaw-doctor
rm -f ~/bin/openclaw-heal

# 从 .bashrc 移除别名
sed -i '/openclaw-heal/d' ~/.bashrc
```

## 📞 联系支持



如有问题，请提交 GitHub Issues:

- https://github.com/kosei-echo/openclaw-self-healing/issues




