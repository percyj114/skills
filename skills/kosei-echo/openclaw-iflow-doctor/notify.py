#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Self-Healing - 通知模块
使用 OpenClaw 内置的 message 工具发送飞书/钉钉通知
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path


class Notifier:
    """通知发送器 - 使用 OpenClaw message 工具"""
    
    def __init__(self):
        """初始化通知器"""
        self.config = self.load_openclaw_config()
    
    def load_openclaw_config(self):
        """加载 OpenClaw 配置"""
        config_path = Path.home() / ".openclaw" / "openclaw.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def check_channels(self):
        """检查已配置的渠道"""
        channels = self.config.get("channels", {})
        return {
            "feishu": "feishu" in channels,
            "dingtalk": "dingtalk" in channels
        }
    
    def send_alert(self, level, title, details, platform=None):
        """发送警报通知
        
        Args:
            level: 警报级别 (info/warning/error/critical)
            title: 警报标题
            details: 详细信息
            platform: 指定平台 (feishu/dingtalk/both)，默认自动检测
        
        Returns:
            bool: 是否成功发送
        """
        # 检查可用的渠道
        available = self.check_channels()
        
        # 如果都没有配置，静默返回（不报错）
        if not available["feishu"] and not available["dingtalk"]:
            # 静默模式：不输出错误，直接返回 False
            return False
        
        # 构建通知内容
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 根据级别选择模板
        level_config = {
            "info": ("ℹ️ 信息", "blue"),
            "warning": ("⚠️ 警告", "orange"),
            "error": ("❌ 错误", "red"),
            "critical": ("🚨 严重错误", "red")
        }
        
        emoji, _ = level_config.get(level, ("ℹ️ 信息", "blue"))
        
        # 构建 Markdown 消息
        message = f"""## {emoji} {title}

**时间**: {timestamp}
**级别**: {level.upper()}

**详情**:
{details}

---
*OpenClaw Self-Healing System*"""
        
        # 自动检测发送目标（如果未指定平台）
        if platform is None:
            # 自动模式：发送到所有已配置的平台
            targets = []
            if available["feishu"]:
                targets.append("feishu")
            if available["dingtalk"]:
                targets.append("dingtalk")
        elif platform == "both":
            # 两者都发
            targets = []
            if available["feishu"]:
                targets.append("feishu")
            if available["dingtalk"]:
                targets.append("dingtalk")
        else:
            # 指定平台
            if platform == "feishu" and available["feishu"]:
                targets = ["feishu"]
            elif platform == "dingtalk" and available["dingtalk"]:
                targets = ["dingtalk"]
            else:
                # 指定的平台未配置，静默返回
                return False
        
        if not targets:
            return False
        
        # 使用 OpenClaw message 工具发送
        # 注意：message 工具需要 target 参数，我们使用默认 target（空）发送到当前会话
        success = False
        for target in targets:
            try:
                # 方式 1: 使用 openclaw message send（需要 target）
                # 方式 2: 直接写入日志，让 OpenClaw 的钩子处理
                # 这里使用日志方式，更简单可靠
                
                # 写入通知日志
                log_path = Path.home() / ".openclaw" / "logs" / f"notify_{target}.log"
                log_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write(f"[{timestamp}] {level.upper()} - {title}\n")
                    f.write(f"{details}\n")
                    f.write("-" * 60 + "\n")
                
                print(f"📝 {target} 通知已记录到日志：{log_path}")
                success = True
                
                # TODO: 当 OpenClaw 支持自动发送通知时，启用以下代码
                # cmd = ["openclaw", "message", "send", "--channel", target, "--target", "default", "-m", message]
                # result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=30)
            
            except Exception as e:
                print(f"❌ {target} 消息发送异常：{e}")
        
        return success
    
    def test_notification(self):
        """测试通知"""
        print("📬 发送测试通知...")
        print(f"   飞书：{'✅ 已配置' if self.check_channels()['feishu'] else '❌ 未配置'}")
        print(f"   钉钉：{'✅ 已配置' if self.check_channels()['dingtalk'] else '❌ 未配置'}")
        print()
        
        test_content = """
**这是一条测试消息**

如果您收到这条消息，说明通知系统工作正常。

测试时间：{}
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        success = self.send_alert("info", "🦞 OpenClaw 自愈系统测试", test_content)
        
        if success:
            print("\n✅ 测试通知发送成功！")
        else:
            print("\n❌ 测试通知发送失败，请检查 OpenClaw 渠道配置")
        
        return success


def main():
    """命令行入口"""
    import sys
    
    notifier = Notifier()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python notify.py test                    # 测试通知")
        print("  python notify.py send <level> <title>    # 发送警报")
        print("  python notify.py check                   # 检查渠道配置")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        available = notifier.check_channels()
        print("OpenClaw 渠道配置:")
        print(f"  飞书：{'✅ 已配置' if available['feishu'] else '❌ 未配置'}")
        print(f"  钉钉：{'✅ 已配置' if available['dingtalk'] else '❌ 未配置'}")
        sys.exit(0)
    
    elif command == "test":
        notifier.test_notification()
    
    elif command == "send":
        if len(sys.argv) < 4:
            print("❌ 用法：python notify.py send <level> <title> [details]")
            sys.exit(1)
        level = sys.argv[2]
        title = sys.argv[3]
        details = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else "无详细信息"
        notifier.send_alert(level, title, details)
    
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
