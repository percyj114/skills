#!/bin/bash
# OpenClaw Self-Healing System - 安装脚本 (macOS/Linux)
# 支持：三端通用（macOS + Linux + Windows）

set -e

echo "============================================================"
echo "🦞 OpenClaw Self-Healing System 安装脚本"
echo "============================================================"
echo ""

# 检测操作系统
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
echo "📌 检测到操作系统：$OS"
echo ""

# 检查前提条件
echo "🔍 检查前提条件..."

# 检查 OpenClaw
if ! command -v openclaw &> /dev/null; then
    echo "❌ OpenClaw 未安装，请先安装 OpenClaw"
    exit 1
fi
echo "✅ OpenClaw 已安装"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi
echo "✅ Python3 已安装"

# 检查 jq
if ! command -v jq &> /dev/null; then
    echo "⚠️  jq 未安装，尝试安装..."
    if [[ "$OS" == "macos" ]]; then
        brew install jq
    else
        sudo apt-get install -y jq || sudo yum install -y jq
    fi
fi
echo "✅ jq 已安装"

echo ""

# 创建目录
echo "📁 创建目录..."
SKILL_DIR="$HOME/.openclaw/skills/openclaw-iflow-doctor"
mkdir -p "$SKILL_DIR"
mkdir -p "$HOME/.openclaw/logs"
echo "✅ 目录已创建"
echo ""

# 配置通知
echo "📬 配置通知..."
echo ""
echo "请选择通知方式:"
echo "  1) 飞书"
echo "  2) 钉钉"
echo "  3) 两者都配置"
echo "  4) 跳过（稍后配置）"
echo ""
read -p "请输入选项 (1-4): " notify_choice

if [[ "$notify_choice" == "1" || "$notify_choice" == "3" ]]; then
    read -p "请输入飞书 webhook URL: " feishu_webhook
    python3 -c "
import json
from pathlib import Path
config_path = Path.home() / '.openclaw' / 'skills' / 'openclaw-iflow-doctor' / 'notify_config.json'
config = {'feishu': '$feishu_webhook', 'dingtalk': None}
config_path.parent.mkdir(parents=True, exist_ok=True)
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print('✅ 飞书 webhook 已保存')
"
fi

if [[ "$notify_choice" == "2" || "$notify_choice" == "3" ]]; then
    read -p "请输入钉钉 webhook URL: " dingtalk_webhook
    read -p "请输入钉钉签名密钥（可选，直接回车跳过）: " dingtalk_secret
    python3 -c "
import json
from pathlib import Path
config_path = Path.home() / '.openclaw' / 'skills' / 'openclaw-iflow-doctor' / 'notify_config.json'
try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except:
    config = {'feishu': None, 'dingtalk': None}
config['dingtalk'] = {'webhook': '$dingtalk_webhook', 'secret': '$dingtalk_secret'}
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print('✅ 钉钉 webhook 已保存')
"
fi

echo ""

# 安装 KeepAlive
echo "🔄 配置 KeepAlive..."

if [[ "$OS" == "macos" ]]; then
    # macOS: LaunchAgent
    PLIST_DIR="$HOME/Library/LaunchAgents"
    mkdir -p "$PLIST_DIR"
    
    # 复制并替换 plist 文件
    USER_NAME=$(whoami)
    sed "s/{{USER}}/$USER_NAME/g" "$SKILL_DIR/templates/ai.openclaw.gateway.plist" > "$PLIST_DIR/ai.openclaw.gateway.plist"
    
    # 加载 LaunchAgent
    launchctl unload "$PLIST_DIR/ai.openclaw.gateway.plist" 2>/dev/null || true
    launchctl load "$PLIST_DIR/ai.openclaw.gateway.plist"
    
    echo "✅ macOS LaunchAgent 已配置"

elif [[ "$OS" == "linux" ]]; then
    # Linux: systemd
    USER_NAME=$(whoami)
    
    # 复制并替换 service 文件
    sed "s/{{USER}}/$USER_NAME/g" "$SKILL_DIR/templates/openclaw-gateway.service" | sudo tee /etc/systemd/system/openclaw-gateway.service > /dev/null
    
    # 重载并启用服务
    sudo systemctl daemon-reload
    sudo systemctl enable openclaw-gateway
    sudo systemctl start openclaw-gateway
    
    echo "✅ Linux systemd 服务已配置"
fi

echo ""

# 测试安装
echo "🧪 测试安装..."

# 检查 Gateway 是否运行
sleep 5
if curl -s http://localhost:18789 > /dev/null 2>&1; then
    echo "✅ Gateway 运行正常"
else
    echo "⚠️  Gateway 未运行，尝试启动..."
    openclaw gateway &
    sleep 5
    if curl -s http://localhost:18789 > /dev/null 2>&1; then
        echo "✅ Gateway 已启动"
    else
        echo "❌ Gateway 启动失败，请检查日志"
    fi
fi

echo ""

# 完成
echo "============================================================"
echo "🎉 安装完成！"
echo "============================================================"
echo ""
echo "📚 使用方法:"
echo ""
echo "  # 查看自愈系统状态"
echo "  python3 $SKILL_DIR/watchdog.py --test"
echo ""
echo "  # 发送测试通知"
echo "  python3 $SKILL_DIR/notify.py test"
echo ""
echo "  # 手动诊断问题"
echo "  openclaw skills run openclaw-iflow-doctor --diagnose '问题描述'"
echo ""
echo "📝 配置文件位置:"
echo "  - 通知配置：$HOME/.openclaw/skills/openclaw-iflow-doctor/notify_config.json"
echo "  - Watchdog 配置：$HOME/.openclaw/skills/openclaw-iflow-doctor/watchdog_config.json"
echo ""
echo "🛡️  系统已激活，Gateway 将自动恢复！"
echo ""
