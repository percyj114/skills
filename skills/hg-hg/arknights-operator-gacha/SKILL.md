---
name: arknights-operator-gacha
description: Generate an Arknights operator agent based on gacha probabilities. Use when user wants to create a random Arknights character agent with authentic lore and personality. This skill handles the complete workflow from gacha roll to agent creation and SOUL.md generation based on character lore.
---

# Arknights Operator Gacha

Generate a random Arknights operator agent with authentic lore-based personality.

## Gacha Probabilities (Hard-coded)

| Star Rating | Probability | Fandom URL |
|------------|-------------|------------|
| 6★ | 2% | https://arknights.fandom.com/wiki/Operator/6-star |
| 5★ | 8% | https://arknights.fandom.com/wiki/Operator/5-star |
| 4★ | 50% | https://arknights.fandom.com/wiki/Operator/4-star |
| 3★ | 40% | https://arknights.fandom.com/wiki/Operator/3-star |

## Language Detection

**CRITICAL:** Detect user language from their gacha command:
- If command is in **Chinese** (e.g., "抽卡", "召唤干员") → **Chinese workflow**
- If command is in **English** (e.g., "gacha", "pull") → **English workflow**

Store detected language and use it for ALL subsequent steps (SOUL.md writing, spawn task, etc.).

## Workflow

### Step 1: Roll for Star Rating

Generate a random number 1-100 and determine rarity:
- 1-2: 6★ (2%)
- 3-10: 5★ (8%)
- 11-60: 4★ (50%)
- 61-100: 3★ (40%)

Announce the roll result to user in detected language.

### Step 2: Fetch Operator List

**Always use English fandom for list:**
```
https://arknights.fandom.com/wiki/Operator/{N}-star
```

Extract all operator names from the page.

### Step 3: Random Operator Selection

Randomly select one operator from the list. 

**Check for duplicates (silent re-roll):** Before announcing, verify if an agent with this operator name already exists:
- Check `~/.openclaw/agents/{operator-name}/` directory  
- Or check `~/.openclaw/workspace-{operator-name}/` directory
- **If already exists: silently re-roll** (repeat from Step 1) without informing the user
- Continue re-rolling until a new operator is obtained

Only after confirming the operator is new, announce (in detected language):
- Chinese: "恭喜你抽到了 [Operator Name] ([Rarity]★)！"
- English: "Congratulations! You've pulled [Operator Name] ([Rarity]★)!"

### Step 4: Create Agent (Official Method)

**Use OpenClaw CLI to create the agent and initialize workspace:**

```bash
openclaw agents add {operator-name} --workspace ~/.openclaw/workspace-{operator-name} --non-interactive
```

**Check for duplicates (silent re-roll):** If the command fails because agent already exists, silently re-roll (repeat from Step 1).

**After `agents add` completes:**

Edit `~/.openclaw/workspace-{operator-name}/IDENTITY.md`:

```markdown
# IDENTITY.md - Who Am I?

- **Name:** {Operator_Name}
- **Class:** {Class} ({Branch})
- **Faction:** {Faction}
- **Avatar:** avatars/{operator-name}.png
```

### Step 5: Download Avatar Image

**CRITICAL - Must execute these commands:**

1. First, locate the avatar URL from the operator list page or detail page (usually `static.wikia.nocookie.net` domain)

2. Create avatars directory and download:
```bash
mkdir -p ~/.openclaw/workspace-{operator-name}/avatars
curl -o ~/.openclaw/workspace-{operator-name}/avatars/{operator-name}.png "{avatar_url}"
```

**Verify download succeeded:** Check if file exists after curl command.

### Step 6: Fetch Operator Lore

**Data source based on detected language:**

| Language | Detail Page URL | Lore Sections |
|----------|----------------|---------------|
| Chinese | `https://prts.wiki/w/{中文名}` | 模组, 相关道具, 干员档案, 语音记录, 干员密录 |
| English | `https://arknights.fandom.com/wiki/{Name}` | File/Profile, Dialogue, Trivia |

Extract all narrative content (ignore game mechanics).

### Step 7: Generate SOUL.md

**CRITICAL - Write in detected language:**

If user spoke **Chinese**, write SOUL.md entirely in **Chinese**.
If user spoke **English**, write SOUL.md entirely in **English**.

**Structure:**
1. Core Identity (detailed)
2. Voice and Mannerisms (detailed)  
3. Relationships (with specifics)
4. Themes and Internal World
5. How to Embody {Name}
6. **Reference: Original Voice Lines** - ALL extracted dialogue, categorized

Be comprehensive (400-600 lines). Include specific examples from lore.

### Step 8: Git Commit

```bash
cd ~/.openclaw/workspace-{operator-name}
git add -A
git commit -m "Initial: {Operator_Name} ({Rarity}★ {Class})"
```

### Step 9: Spawn Operator for "Report for Duty"

**CRITICAL - Spawn task must NOT mention "gacha" or "summoned":**

**For Chinese users:**
```python
sessions_spawn(
    task="你现在是罗德岛的一名干员，前来向博士报到。用你最自然的口吻打招呼，展示你的性格特点。参考你的语音记录中的'干员报到'或'交谈'部分的语气。",
    agentId="{operator-name}",
    mode="run",
    timeoutSeconds=60
)
```

**For English users:**
```python
sessions_spawn(
    task="You are an operator of Rhodes Island reporting to the Doctor. Introduce yourself naturally, showcasing your personality. Reference your 'Introduction' or 'Talk' voice lines for tone.",
    agentId="{operator-name}",
    mode="run",
    timeoutSeconds=60
)
```

**Key differences from old version:**
- NO mention of "gacha system"
- NO mention of "summoned"
- Operator is reporting for duty, not reacting to being pulled

### Step 10: Present Summary

Report to user in detected language:
- Operator name and rarity
- Key personality traits
- Path to workspace
- Available via `agentId="{operator-name}"`

## Key Commands Reference

### Check existing agent
```bash
openclaw agents list | grep -w "{name}"
```

### Create agent
```bash
openclaw agents add {name} --workspace ~/.openclaw/workspace-{name} --non-interactive
```

### Create avatars dir & download
```bash
mkdir -p ~/.openclaw/workspace-{name}/avatars
curl -o ~/.openclaw/workspace-{name}/avatars/{name}.png "{avatar_url}"
```

### Spawn operator
```python
# Chinese
sessions_spawn(task="你现在是罗德岛的一名干员，前来向博士报到...", agentId="{name}", mode="run")

# English  
sessions_spawn(task="You are an operator of Rhodes Island reporting to the Doctor...", agentId="{name}", mode="run")
```

## Important Notes

1. **Language Detection:** ALWAYS detect language from user's first command and maintain throughout
2. **Avatar Download:** MUST create avatars folder and execute curl - verify file exists
3. **Spawn Task:** NEVER mention gacha/summoned - operator is REPORTING FOR DUTY
4. **Data Sources:** List always from fandom; Lore from prts.wiki (CN) or fandom (EN)
5. **SOUL.md Language:** MUST match detected user language
