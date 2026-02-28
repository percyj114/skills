# Deep Scout 🛰️

A multi-stage intelligence pipeline for OpenClaw. It performs deep web research by escalating through a tiered toolchain: Search → Filter → Fetch (Fast/Deep/Browser) → Synthesize.

## 🚀 One-Step Install

If you are running OpenClaw, just say to your agent:
> "Install the Deep Scout skill"

Or manually:
```bash
clawhub install deep-scout
```

## 🛠️ How it Works

Deep Scout doesn't just give you links; it automates the entire research workflow:

1.  **Search**: Queries Brave/Perplexity with your parameters.
2.  **Filter**: Uses LLM to score snippets for relevance and authority, dropping the noise.
3.  **Fetch (Tiered)**:
    *   **Tier 1**: `web_fetch` (Fast, static HTML).
    *   **Tier 2**: `Firecrawl` (Deep, JS-rendered).
    *   **Tier 3**: `Browser` tool (Fallback for paywalls/protected sites).
4.  **Synthesize**: Compiles all data into a structured report with hard citations.

## 📖 Usage

```bash
/deep-scout "Compare the top 3 agent memory frameworks of 2026" --style comparison
```

### Options
- `--depth N`: Number of pages to deep-fetch (default 5).
- `--freshness`: `pd` (day), `pw` (week), `pm` (month), `py` (year).
- `--style`: `report`, `comparison`, `bullets`, `timeline`.

---
*Created by Jony Jing & WenWen · Powered by OpenClaw*
