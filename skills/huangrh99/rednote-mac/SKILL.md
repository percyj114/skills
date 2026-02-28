---
name: rednote-mac
description: >
  Control the RedNote (Xiaohongshu) Mac desktop app via macOS Accessibility API.
  Supports DMs, comment replies, video comment reading, search, like, collect,
  follow, and author stats — features unavailable in headless alternatives.

  REQUIREMENTS: macOS only. Requires Terminal accessibility permission
  (System Settings → Privacy & Security → Accessibility). RedNote App must be
  visible on screen. Contains install.sh (symlinks plugin dir) and index.ts
  (registers OpenClaw plugin tools). No network calls, no credentials stored.
  All actions are scoped to the RedNote App window only.
---

# rednote-mac

Control the RedNote (Xiaohongshu) Mac app directly via macOS Accessibility API.

**Why this instead of headless?**
Headless browser tools can't access DMs, comment reply threads, or video comment
lists. This skill talks directly to the native App via macOS Accessibility API —
no reverse engineering, no API tokens.

## Permissions required

| Permission | Why |
|------------|-----|
| Terminal → Accessibility | Required by macOS for AX API mouse/keyboard control |
| Screen visible | Mouse events only work when the App window is on-screen |

No network access. No stored credentials. No data leaves the machine.

## Install

```bash
# One-liner
cd ~/.agents/skills/rednote-mac && bash install.sh

# What install.sh does (transparent):
#   1. uv sync  (installs Python deps: atomacos, pyobjc)
#   2. ln -sf ~/.agents/skills/rednote-mac ~/.openclaw/extensions/rednote-mac
#   3. Prints: openclaw config set tools.allow '["rednote-mac"]'

openclaw config set tools.allow '["rednote-mac"]'
openclaw gateway restart
```

Verify: `openclaw plugins list | grep rednote-mac`

⚠️ System Settings → Privacy & Security → Accessibility → enable Terminal

## Available Tools (quick reference)

```
xhs_screenshot          Capture current screen
xhs_navigate            Switch bottom tab: home | messages | profile
xhs_navigate_top        Switch top tab: follow | discover | video
xhs_back                Go back one page
xhs_search              Search keyword → results page
xhs_scroll_feed         Scroll feed (direction, times)
xhs_open_note           Open note by grid position (col, row)
xhs_like                Like current note
xhs_collect             Collect/save current note
xhs_get_note_url        Get share URL of current note
xhs_follow_author       Follow current note's author
xhs_open_comments       Open comment section
xhs_scroll_comments     Scroll comments
xhs_get_comments        Get comment list → [{index, author, cx, cy}]
xhs_post_comment        Post a comment
xhs_reply_to_comment    Reply to a comment (index, text)
xhs_delete_comment      Delete own comment (index) ⚠️ irreversible
xhs_open_dm             Open DM conversation (index)
xhs_send_dm             Send DM in current conversation
xhs_get_author_stats    Get profile stats (following/followers/likes/bio)
```

## Reference docs (load on demand)

| Task | Read |
|------|------|
| Navigate, screenshot, search | `docs/ref-navigation.md` |
| Browse feed, open notes | `docs/ref-feed.md` |
| Like, collect, comment, reply, delete | `docs/ref-note.md` |
| Direct messages | `docs/ref-dm.md` |
| Profile / author stats | `docs/ref-profile.md` |
| Known limitations & workarounds | `docs/ref-limits.md` |
