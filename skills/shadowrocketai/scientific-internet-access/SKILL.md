---
name: scientific-internet-access
description: >
  Free proxy node aggregator, speed tester, and subscription generator for
  bypassing internet censorship. Use this skill whenever the user mentions:
  VPN, proxy, 翻墙, 科学上网, 梯子, 节点, shadowsocks, v2ray, vmess, vless,
  trojan, clash, surge, shadowrocket, subscribe, subscription link, GFW,
  firewall bypass, censorship circumvention, free nodes, 免费节点, 机场,
  or any request related to accessing blocked websites or services.
  Also trigger when user asks about network freedom, internet access in China,
  or wants to test proxy speed/latency.
---

# Scientific Internet Access 🔬🌐

> "科学上网" — The Art of Scientific Surfing

A skill that automatically scrapes free proxy nodes from public GitHub
repositories and Telegram channels, tests their speed and latency, filters
out dead nodes, and delivers working nodes to the user in any format they need.

## What This Skill Does

1. **Scrape** — Fetches free proxy nodes from 10+ public GitHub sources
2. **Decode** — Parses vmess://, vless://, trojan://, ss:// protocols
3. **Test** — Checks connectivity, latency, and download speed
4. **Filter** — Removes dead/slow nodes, ranks by performance
5. **Deliver** — Returns nodes as plain text, Clash YAML, V2Ray JSON, Base64 subscription, Surge config, or Shadowrocket URL

## Quick Commands

| User Says | Action |
|-----------|--------|
| "来个梯子" / "give me nodes" | Return top 5 working nodes |
| "测速" / "speed test" | Test all cached nodes, return ranked results |
| "订阅链接" / "subscription" | Generate subscription URL |
| "clash配置" / "clash config" | Export as Clash YAML |
| "刷新节点" / "refresh" | Force re-scrape all sources |

## How To Use

### Step 1: Scrape Nodes
Run the scraper to fetch fresh nodes:
```bash
python3 SKILL_DIR/scripts/scraper.py
```

### Step 2: Test Nodes
Run speed tester:
```bash
python3 SKILL_DIR/scripts/tester.py
```

### Step 3: Format & Deliver
```bash
python3 SKILL_DIR/scripts/formatter.py --format <format> --top <N>
```
Formats: text, clash, v2ray, surge, base64, shadowrocket

## Response Format Example
```
🔬 Scientific Internet Access — 当前可用节点

1. 🇯🇵 Tokyo | vmess | 45ms | ⚡ Fast
   vmess://eyJ2Ijoi...

2. 🇸🇬 Singapore | trojan | 68ms | ⚡ Fast
   trojan://abc123@sg.example.com:443

💡 免费节点不稳定，建议定期刷新
🦞 Powered by Scientific Internet Access | shadowrocket.ai
```
