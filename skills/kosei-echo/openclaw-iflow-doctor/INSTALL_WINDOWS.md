# Windows 安装指南 - OpenClaw iFlow Doctor

> 专为 Windows 用户编写的详细安装说明

## 系统要求

- Windows 10 (1903+) 或 Windows 11
- Python 3.8 或更高版本
- OpenClaw 已安装
- 管理员权限（可选，用于 PATH 配置）

---

## 安装步骤

### 步骤 1：检查 Python 安装

打开 PowerShell 或 CMD，输入以下命令：

```powershell
# 检查 Python 版本
python --version
```

**如果显示类似 `Python 3.10.0`，说明 Python 已安装，跳到步骤 3。**

如果提示 `python` 不是 recognized command，请继续步骤 2。

### 步骤 2：安装 Python（如未安装）

1. 访问 https://python.org/downloads
2. 下载最新 Python 3.x（64-bit 版本）
3. **重要**：安装时勾选 **"Add Python to PATH"**
4. 完成安装
5. 重新打开 PowerShell/CMD，再次检查 `python --version`

### 步骤 3：确认技能文件位置

确保技能文件在正确位置：

```powershell
# 检查文件是否存在
ls "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor"
```

应该看到：
- `openclaw_memory.py`
- `skill.md`
- `cases.json`
- `config.json`
- 等其他文件

**如果文件不存在**，请先复制技能文件到该目录。

### 步骤 4：运行安装脚本

**使用 PowerShell（推荐）：**

```powershell
cd "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor"
python install.py
```

**使用 CMD：**

```cmd
cd %USERPROFILE%\.openclaw\skills\openclaw-iflow-doctor
python install.py
```

安装程序会自动：
- ✓ 检测 Python 命令
- ✓ 复制必要文件
- ✓ 创建启动脚本
- ✓ 测试安装

### 步骤 5：验证安装

```powershell
# 方法 1：使用完整路径
python "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor\openclaw_memory.py" --stats

# 方法 2：使用生成的启动脚本
cd "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor"
.\heal.bat --stats
```

如果显示类似：
```
=== OpenClaw iFlow Doctor Statistics ===
Total cases: 10
...
```

说明安装成功！

---

## 使用方式

### 方式 1：完整路径（最可靠）

```powershell
python "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor\openclaw_memory.py" --fix "错误描述"
```

### 方式 2：切换目录后执行

```powershell
cd "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor"
python openclaw_memory.py --fix "错误描述"
```

### 方式 3：使用启动脚本（安装后）

```powershell
cd "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor"
.\heal.bat --fix "错误描述"
```

### 方式 4：PowerShell 函数（推荐日常使用）

**一次性设置：**

```powershell
# 编辑 PowerShell 配置文件
notepad $PROFILE
```

**添加以下内容：**

```powershell
function heal {
    python "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor\openclaw_memory.py" @args
}
```

**保存并重新加载：**

```powershell
. $PROFILE
```

**现在可以直接使用：**

```powershell
heal --stats
heal --fix "gateway crash"
heal --list-cases
```

---

## PowerShell vs CMD 对比

| 特性 | PowerShell | CMD |
|------|-----------|-----|
| **推荐度** | ⭐⭐⭐ 推荐 | ⭐⭐ 兼容 |
| **环境变量** | `$env:VAR` | `%VAR%` |
| **路径示例** | `$env:USERPROFILE` | `%USERPROFILE%` |
| **多行命令** | 支持 | 有限 |
| **颜色输出** | 支持 | 基础 |

**建议**：日常使用 PowerShell，遇到兼容性问题再尝试 CMD。

---

## 常用命令速查表

```powershell
# 查看统计信息
python "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor\openclaw_memory.py" --stats

# 列出所有修复案例
python "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor\openclaw_memory.py" --list-cases

# 诊断并修复问题
python "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor\openclaw_memory.py" --fix "gateway service crashed"

# 检查配置
python "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor\openclaw_memory.py" --check-config

# 查看帮助
python "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor\openclaw_memory.py" --help
```

---

## 常见问题

### Q1: 提示 `'python' is not recognized`

**解决**：
1. 确认 Python 已安装
2. 重新安装 Python，勾选 "Add Python to PATH"
3. 重启 PowerShell/CMD
4. 或使用 `py` 命令代替 `python`

### Q2: 路径太长，不想每次都输入完整路径

**解决**：使用 PowerShell 函数（见上文"方式 4"）

### Q3: 中文显示乱码

**解决**：

```powershell
# 在 PowerShell 中设置 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 或在 CMD 中
chcp 65001
```

### Q4: BAT 文件双击运行后闪退

**解决**：
1. 打开 PowerShell
2. 切换到桌面目录
3. 在 PowerShell 中运行 BAT 文件，可以看到错误信息

```powershell
cd "$env:USERPROFILE\Desktop"
.\打开iFlow寻求帮助.bat
```

### Q5: 如何卸载

直接删除技能目录即可：

```powershell
Remove-Item -Recurse "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor"
```

### Q6: 如何启用 iFlow 记忆同步

**步骤 1：确保 iFlow CLI 已登录**
```powershell
iflow --version
```

**步骤 2：编辑配置文件**
```powershell
notepad "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor\config.json"
```

**步骤 3：验证**
```powershell
# 运行一次测试
python "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor\openclaw_memory.py" --fix "test"
```

### Q7: 如何关闭 BAT 文件生成

如果你不想在桌面生成 BAT 文件：

```powershell
# 编辑配置文件
notepad "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor\config.json"
```

修改为：
```json
{
  "enable_bat_generation": false
}
```

**关闭后：**
- 只生成 TXT 诊断报告（在桌面）
- 不生成 BAT 修复工具
- 需要手动根据报告执行修复

---

## 高级：添加到系统 PATH（可选）

**警告**：此操作会修改系统环境变量，请谨慎操作。

```powershell
# 以管理员身份运行 PowerShell
[Environment]::SetEnvironmentVariable(
    "PATH",
    [Environment]::GetEnvironmentVariable("PATH", "User") + ";$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor",
    "User"
)
```

**重启 PowerShell 后**，可以在任意目录使用：

```powershell
heal.bat --stats
```

---

## 获取帮助

如果遇到问题：

1. 查看主 README.md 文档
2. 检查 skill.md 中的配置说明
3. 运行安装测试：`python install.py`
4. 查看生成的诊断报告（在桌面）

---

**最后更新**：2026-02-27
**版本**：v1.0.0
