---
name: password-generator
description: 生成随机安全密码。支持自定义长度(默认12位)、字符类型(大小写字母、数字、符号)。当用户要求生成密码、创建密码、随机密码时使用此技能。
---

# Password Generator

生成随机安全密码的工具技能。

## Usage

当用户要求:
- "生成密码"
- "创建一个密码"
- "随机密码"
- "生成12位密码"

执行 `scripts/generate_password.py` 并将生成的密码保存到 `memory/passwords.md`。

## Options

- 默认: 12位，包含大小写+数字+符号
- 可自定义长度和字符类型

## 保存密码

将生成的密码保存到 `memory/passwords.md`，格式:
```markdown
## [日期]

- **名称**: [描述]
  - 密码: [生成的密码]
  - 长度: 12
  - 字符: 大小写字母 + 数字 + 符号
```
