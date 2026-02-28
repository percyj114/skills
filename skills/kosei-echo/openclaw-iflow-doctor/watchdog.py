#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 监控守护进程
功能：
1. 监控 openclaw-gateway 进程
2. 检测到崩溃时自动调用修复技能
3. 支持日志监控和健康检查
"""

import os
import sys
import time
import json
import psutil
import subprocess
import threading
import platform
from datetime import datetime
from pathlib import Path


class OpenClawWatchdog:
    """OpenClaw 监控守护进程"""
    
    def __init__(self):
        self.running = False
        self.gateway_process = None
        self.log_file = Path.home() / ".openclaw" / "logs" / "watchdog.log"
        self.check_interval = 1  # Level 0: 1秒快速检查（KeepAlive）
        self.crash_threshold = 5  # 崩溃次数阈值（Ramsbaby标准）
        self.crash_count = 0
        self.last_restart = None
        self.max_backoff = 300  # 最大退避时间5分钟
        
        # 告警配置
        self.alert_config = self._load_alert_config()
        
        # 确保日志目录存在
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_alert_config(self):
        """加载告警配置"""
        config_file = Path.home() / ".openclaw" / "skills" / "openclaw-iflow-doctor" / "config.json"
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('alert', {})
        except:
            return {}
    
    def get_backoff_delay(self):
        """计算指数退避延迟"""
        delay = self.crash_count * 10  # 每次崩溃增加10秒
        return min(delay, self.max_backoff)
    
    def log(self, message, level="INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{level}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
        
        print(log_line.strip())
    
    def is_gateway_running(self):
        """检查 gateway 是否在运行"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if 'openclaw-gateway' in cmdline or 'openclaw' in proc.info['name']:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False
    
    def check_gateway_health(self):
        """检查 gateway 健康状态"""
        try:
            import urllib.request
            response = urllib.request.urlopen(
                'http://localhost:18789/health',
                timeout=5
            )
            return response.status == 200
        except:
            return False
    
    def call_healing_skill(self, error_msg, error_logs=""):
        """调用修复技能"""
        self.log(f"Calling healing skill for: {error_msg[:50]}...")
        
        try:
            healer_script = Path.home() / ".iflow" / "memory" / "openclaw" / "openclaw_memory.py"
            
            result = subprocess.run(
                ['python', str(healer_script), '--fix', error_msg, '--logs', error_logs],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            self.log(f"Healing result: {result.returncode}")
            if result.stdout:
                self.log(f"Output: {result.stdout[:200]}")
            
            return result.returncode == 0
            
        except Exception as e:
            self.log(f"Healing failed: {e}", "ERROR")
            return False
    
    def send_alert(self, title, message, level="WARN"):
        """发送告警通知（Level 4）"""
        self.log(f"Sending alert: {title}")
        
        # 钉钉告警
        dingtalk_webhook = self.alert_config.get('dingtalk_webhook')
        if dingtalk_webhook:
            self._send_dingtalk(dingtalk_webhook, title, message, level)
        
        # 飞书告警
        lark_webhook = self.alert_config.get('lark_webhook')
        if lark_webhook:
            self._send_lark(lark_webhook, title, message, level)
        
        # Discord 告警
        discord_webhook = self.alert_config.get('discord_webhook')
        if discord_webhook:
            self._send_discord(discord_webhook, title, message, level)
    
    def _send_dingtalk(self, webhook, title, message, level):
        """发送钉钉消息"""
        try:
            import urllib.request
            import urllib.parse
            
            color_map = {"INFO": "#1E90FF", "WARN": "#FFA500", "ERROR": "#FF4500"}
            color = color_map.get(level, "#808080")
            
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": f"OpenClaw告警: {title}",
                    "text": f"#### 🚨 {title}\n\n**级别**: {level}\n\n**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n**详情**: {message}\n"
                }
            }
            
            req = urllib.request.Request(
                webhook,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req, timeout=10)
            self.log("DingTalk alert sent")
            
        except Exception as e:
            self.log(f"Failed to send DingTalk alert: {e}", "ERROR")
    
    def _send_discord(self, webhook, title, message, level):
        """发送 Discord 消息"""
        try:
            import urllib.request
            
            color_map = {"INFO": 0x1E90FF, "WARN": 0xFFA500, "ERROR": 0xFF4500}
            color = color_map.get(level, 0x808080)
            
            data = {
                "embeds": [{
                    "title": f"🚨 {title}",
                    "description": message,
                    "color": color,
                    "timestamp": datetime.now().isoformat(),
                    "footer": {"text": f"Level: {level}"}
                }]
            }
            
            req = urllib.request.Request(
                webhook,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req, timeout=10)
            self.log("Discord alert sent")
            
        except Exception as e:
            self.log(f"Failed to send Discord alert: {e}", "ERROR")
    
    def _send_lark(self, webhook, title, message, level):
        """发送飞书消息"""
        try:
            import urllib.request
            
            color_map = {"INFO": "blue", "WARN": "orange", "ERROR": "red"}
            color = color_map.get(level, "grey")
            
            data = {
                "msg_type": "interactive",
                "card": {
                    "header": {
                        "title": {
                            "tag": "plain_text",
                            "content": f"🚨 OpenClaw告警: {title}"
                        },
                        "template": color
                    },
                    "elements": [
                        {
                            "tag": "div",
                            "text": {
                                "tag": "lark_md",
                                "content": f"**级别**: {level}\n**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n**详情**: {message}"
                            }
                        }
                    ]
                }
            }
            
            req = urllib.request.Request(
                webhook,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req, timeout=10)
            self.log("Lark alert sent")
            
        except Exception as e:
            self.log(f"Failed to send Lark alert: {e}", "ERROR")
    
    def restart_gateway(self):
        """重启 gateway（Level 0: KeepAlive）"""
        self.log("Restarting OpenClaw Gateway...")
        
        try:
            # Kill existing process
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if 'openclaw-gateway' in cmdline:
                        proc.terminate()
                        proc.wait(timeout=5)
                except:
                    pass
            
            # 指数退避等待
            backoff = self.get_backoff_delay()
            if backoff > 0:
                self.log(f"Backoff delay: {backoff}s (crash count: {self.crash_count})")
                time.sleep(backoff)
            else:
                time.sleep(2)  # 正常重启等待2秒
            
            # Start new process（三端通用）
            popen_kwargs = {
                'stdout': subprocess.DEVNULL,
                'stderr': subprocess.DEVNULL
            }
            
            # Windows 特定参数
            if platform.system().lower() == 'windows':
                popen_kwargs['creationflags'] = subprocess.CREATE_NEW_CONSOLE
            else:
                # Linux/macOS: 使用 nohup 方式启动
                popen_kwargs['start_new_session'] = True
            
            subprocess.Popen(['openclaw', 'gateway'], **popen_kwargs)
            
            self.last_restart = datetime.now()
            self.log("Gateway restarted successfully")
            return True
            
        except Exception as e:
            self.log(f"Failed to restart gateway: {e}", "ERROR")
            return False
    
    def monitor_loop(self):
        """主监控循环"""
        self.log("Watchdog started")
        self.running = True
        
        while self.running:
            try:
                # 1. 检查进程是否存在
                if not self.is_gateway_running():
                    self.crash_count += 1
                    self.log(f"Gateway not running! Crash count: {self.crash_count}", "WARN")
                    
                    if self.crash_count >= self.crash_threshold:
                        # Level 3: 调用修复技能
                        self.log("Crash threshold reached, calling healing skill...", "WARN")
                        
                        error_msg = f"Gateway crashed {self.crash_count} times"
                        healing_result = self.call_healing_skill(error_msg)
                        
                        if healing_result:
                            self.log("Healing completed, resetting crash count")
                            self.crash_count = 0
                        else:
                            # Level 4: 告警通知（所有自动化都失败了）
                            self.log("Level 4: All automation failed, alerting human...", "ERROR")
                            self.send_alert(
                                "OpenClaw Gateway 需要人工干预",
                                f"Gateway 已崩溃 {self.crash_count} 次，自动修复失败。\n"
                                f"日志文件: {self.log_file}\n"
                                f"请检查系统状态。",
                                "ERROR"
                            )
                    
                    # Level 0: 尝试重启（KeepAlive）
                    self.restart_gateway()
                
                else:
                    # 进程在运行，检查健康状态
                    if not self.check_gateway_health():
                        self.log("Gateway process exists but not responding", "WARN")
                    else:
                        # 健康，重置崩溃计数
                        if self.crash_count > 0:
                            self.log("Gateway healthy, resetting crash count")
                            self.crash_count = 0
                
                # 等待下一次检查
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                self.log("Watchdog stopped by user")
                self.running = False
            except Exception as e:
                self.log(f"Watchdog error: {e}", "ERROR")
                time.sleep(self.check_interval)
    
    def start(self):
        """启动监控"""
        self.log("="*60)
        self.log("OpenClaw Watchdog Starting...")
        self.log(f"Check interval: {self.check_interval}s")
        self.log(f"Crash threshold: {self.crash_threshold}")
        self.log("="*60)
        
        # 在后台线程运行
        monitor_thread = threading.Thread(target=self.monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return monitor_thread
    
    def stop(self):
        """停止监控"""
        self.running = False
        self.log("Watchdog stopping...")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw Watchdog")
    parser.add_argument('--start', action='store_true', help='Start monitoring')
    parser.add_argument('--stop', action='store_true', help='Stop monitoring')
    parser.add_argument('--status', action='store_true', help='Check status')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    
    args = parser.parse_args()
    
    watchdog = OpenClawWatchdog()
    
    if args.start or args.daemon:
        if args.daemon:
            # 后台运行
            watchdog.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                watchdog.stop()
        else:
            # 前台运行
            watchdog.monitor_loop()
    
    elif args.status:
        running = watchdog.is_gateway_running()
        healthy = watchdog.check_gateway_health() if running else False
        print(f"Gateway running: {running}")
        print(f"Gateway healthy: {healthy}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
