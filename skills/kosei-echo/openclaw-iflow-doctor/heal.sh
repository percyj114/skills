#!/bin/bash
# OpenClaw Self-Healing Script for Linux/macOS
# 一键修复脚本

set -e

echo "========================================"
echo "  OpenClaw iFlow Doctor - Linux/macOS"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 python3${NC}"
    echo "请先安装 Python 3:"
    echo "  Ubuntu/Debian: sudo apt install python3"
    echo "  CentOS/RHEL:   sudo yum install python3"
    echo "  macOS:         brew install python3"
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查主程序
if [ ! -f "openclaw_memory.py" ]; then
    echo -e "${RED}错误: 未找到 openclaw_memory.py${NC}"
    exit 1
fi

# 显示菜单
echo "请选择修复选项:"
echo ""
echo "  1) 自动诊断并修复"
echo "  2) 仅诊断 (不执行修复)"
echo "  3) 生成修复脚本"
echo "  4) 查看修复记录"
echo "  5) 清除所有记录"
echo "  0) 退出"
echo ""
read -p "请输入选项 [0-5]: " choice

case $choice in
    1)
        echo -e "${YELLOW}正在执行自动诊断和修复...${NC}"
        python3 openclaw_memory.py --auto-fix
        ;;
    2)
        echo -e "${YELLOW}正在执行诊断...${NC}"
        python3 openclaw_memory.py --diagnose-only
        ;;
    3)
        echo -e "${YELLOW}正在生成修复脚本...${NC}"
        python3 openclaw_memory.py --generate-scripts
        ;;
    4)
        echo -e "${YELLOW}修复记录:${NC}"
        RECORDS_FILE="$HOME/.openclaw/skills/openclaw-iflow-doctor/records.json"
        if [ -f "$RECORDS_FILE" ]; then
            cat "$RECORDS_FILE" | python3 -m json.tool 2>/dev/null || cat "$RECORDS_FILE"
        else
            echo "暂无修复记录"
        fi
        ;;
    5)
        read -p "确定要清除所有记录吗? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            rm -f "$HOME/.openclaw/skills/openclaw-iflow-doctor/records.json" "$HOME/.openclaw/skills/openclaw-iflow-doctor/call_logs.json"
            echo -e "${GREEN}记录已清除${NC}"
        else
            echo "已取消"
        fi
        ;;
    0)
        echo "再见!"
        exit 0
        ;;
    *)
        echo -e "${RED}无效选项${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}操作完成!${NC}"
read -p "按 Enter 键继续..."
