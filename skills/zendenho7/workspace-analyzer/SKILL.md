---
name: workspace-analyzer
description: "Analyzes OpenClaw workspace structure and content to identify maintenance needs, bloat, duplicates, and organization issues. Outputs a JSON report for the agent to review and act upon."
version: "1.0.0"
metadata:
  {"openclaw":{"emoji":"📊","requires":{"bins":["python3"]}, "tags":["workspace", "maintenance", "analysis", "health"]}}
---

# Workspace Analyzer

> "Scans, analyzes, and reports. The agent decides."

---

## Overview

A self-improving agent needs a clean workspace. This skill analyzes any OpenClaw workspace to:
1. **Detect** core files dynamically (adapts to workspace changes)
2. **Analyze** content for issues (bloat, duplicates, broken links)
3. **Report** actionable insights for the agent to act upon

**Key Principle:** The script analyzes → the agent decides → the agent acts.

---

## Installation

```bash
# Clone or copy to your skills folder
cp -r workspace-analyzer/ ~/.openclaw/workspace/skills/
```

---

## Usage

### Run Analysis

```bash
# Full analysis (default)
python3 skills/workspace-analyzer/scripts/analyzer.py

# Quick scan (structure only, no content analysis)
python3 skills/workspace-analyzer/scripts/analyzer.py --quick

# Specific workspace
python3 skills/workspace-analyzer/scripts/analyzer.py --root /path/to/workspace

# Output to file
python3 skills/workspace-analyzer/scripts/analyzer.py --output report.json
```

---

## Output Format

```json
{
  "scan_info": {
    "root": "/home/user/.openclaw/workspace",
    "timestamp": "2026-02-21T18:00:00Z",
    "files_scanned": 291
  },
  "core_files_detected": {
    "kai_core": {
      "files": ["SOUL.md", "OPERATING.md", ...],
      "count": 11
    },
    "mission_control": {...},
    "agent_cores": {...},
    "skills": {...}
  },
  "analysis": {
    "SOUL.md": {
      "category": "kai_core",
      "line_count": 450,
      "sections": [...],
      "wiki_links": [...],
      "issues": [...]
    }
  },
  "recommendations": [
    {"action": "REVIEW_BLOAT", "file": "OPERATING.md", "severity": "WARN"},
    {"action": "CHECK_DUPLICATE", "severity": "WARN"},
    {"action": "CHECK_BROKEN_LINK", "severity": "INFO"}
  ],
  "summary": {
    "total_files": 291,
    "total_issues": 17,
    "total_recommendations": 25
  }
}
```

---

## Features

### Dynamic Core File Detection

Automatically detects core files based on location patterns:

| Category | Pattern | Example |
|----------|---------|---------|
| KAI Core | Root *.md | SOUL.md, OPERATING.md |
| Mission Control | mission_control/*GUIDELINES.md | MISSION_CONTROL_GUIDELINES.md |
| Agent Cores | mission_control/agents/*/*.md | designer/SOUL.md |
| Skills | skills/*/SKILL.md | react-expert/SKILL.md |

### Category-Specific Thresholds

Bloat thresholds vary by category:

| Category | Warning | Critical |
|----------|---------|----------|
| kai_core | 400 | 600 |
| mission_control | 500 | 800 |
| agent_cores | 300 | 500 |
| skills | 600 | 1000 |
| memory | 500 | 800 |
| docs | 400 | 600 |

### Issue Detection

- **BLOAT_WARNING**: File exceeds warning threshold
- **BLOAT_CRITICAL**: File exceeds critical threshold
- **ORPHAN_WARNING**: File not modified in 30+ days
- **POTENTIAL_DUPLICATE**: Similar files detected
- **POTENTIAL_BROKEN_LINK**: Wiki-link may not match any file

---

## Recommendations

The analyzer generates actionable recommendations:

| Action | Severity | Description | What To Do |
|--------|----------|-------------|------------|
| REVIEW_BLOAT | WARN/CRITICAL | File is too large | Review if legitimate or split |
| REVIEW_ORPHAN | INFO | File hasn't been modified | Archive if no longer needed |
| CHECK_DUPLICATE | WARN | Potential duplicate files | Verify if intentional or merge |
| CHECK_BROKEN_LINK | INFO | Wiki-link may be broken | Verify if skill exists |
| CHECK_MISSING | WARN | Expected core files not found | Create if needed |

---

## Interpretation Guide

### How to Use Results

**Step 1: Prioritize by Severity**
```
CRITICAL → Review immediately
WARN → Review during next maintenance
INFO → Review during weekly cleanup
```

**Step 2: Understand Context**
- **BLOAT** = Informational, not all need fixing
  - Reference docs (skills/*/references/*.md) can be legitimately large
  - Research logs are consolidations - consider splitting by date
  - Session logs - archive old ones
  
- **DUPLICATES** = Check if intentional
  - IDENTITY files = Expected (agent templates)
  - REVIEW files = May need consolidation
  - LESSONS files = OK (different skills)
  
- **BROKEN LINKS** = Usually false positives
  - Links to skills like [[blogwatcher]] ARE valid
  - Skills have SKILL.md suffix - analyzer doesn't detect this
  - Only flag if link to core file is truly broken

**Step 3: Take Action**
1. Don't auto-fix - review first
2. Archive old session logs monthly
3. Split large research logs by topic
4. Keep reference docs as-is (legitimate)

---

## Integration

### With Heartbeat

Add to your HEARTBEAT.md maintenance section:

```markdown
## 7. Memory + Workspace Maintenance

### Run Workspace Analyzer
python3 skills/workspace-analyzer/scripts/analyzer.py --output /tmp/analysis.json

### Review Recommendations
- Check recommendations in output
- Prioritize by severity
- Fix issues manually
```

### Output to Memory

Save analysis results for later review:

```bash
python3 skills/workspace-analyzer/scripts/analyzer.py \
  --output memory/$(date +%Y-%m-%d)-workspace-analysis.json
```

---

## Safety & Security

### Read-Only
- Never modifies files
- Only reads and analyzes

### No Secrets
- Never reads API keys
- Never accesses credentials
- Only analyzes file metadata and content structure

### Safe Output
- Only contains: file paths, sizes, line counts, recommendations
- No sensitive data exposed

---

## Limitations

- **No auto-fix:** Script reports, agent must decide and act
- **Wiki-link false positives:** Links to external skills may appear broken
- **Date-based duplicate detection:** May miss non-date-based duplicates

---

## Examples

### Sample Output - Core Files

```json
{
  "kai_core": {
    "files": ["SOUL.md", "OPERATING.md", "AGENTS.md", ...],
    "count": 11
  },
  "agent_cores": {
    "agents": ["designer", "developer", "reviewer"],
    "count": 37
  }
}
```

### Sample Output - Recommendations

```json
[
  {
    "action": "REVIEW_BLOAT",
    "file": "OPERATING.md",
    "category": "kai_core",
    "reason": "503 lines - consider splitting (threshold: 400)",
    "severity": "WARN"
  },
  {
    "action": "CHECK_DUPLICATE",
    "name": "IDENTITY",
    "files": ["IDENTITY.md", "mission_control/agents/designer/IDENTITY.md"],
    "reason": "Found 4 files with similar name 'IDENTITY'",
    "severity": "WARN"
  }
]
```

---

## Skill Graph

This skill is related to:

- [[mcporter]] - For MCP server analysis
- [[clean-workspace]] - For actual cleanup tasks
- [[qmd]] - For memory organization

---

## Changelog

### v2.0 (2026-02-21)
- Added category-specific bloat thresholds
- Added duplicate file detection
- Added broken wiki-link detection
- Added category field to analysis output

### v1.0 (2026-02-21)
- Initial release
- Basic file analysis
- Core file detection
- Bloat detection

---

*Last updated: 2026-02-21*
