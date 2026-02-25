---
name: audiomind
description: A comprehensive, intelligent audio toolkit. One skill to rule them all: TTS, SFX, Music, and more. Just describe the sound you need.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🧠"
    tags: ["audio", "ai", "tts", "sfx", "music", "elevenlabs", "mcp"]
---

# AudioMind: Your Intelligent Audio Co-Pilot

**AudioMind** is a single, powerful skill that gives your AI agent a complete suite of audio generation capabilities. It bundles a full-featured MCP server with an intelligent dispatcher, allowing you to generate **Text-to-Speech, Sound Effects, and Music** from a single, unified interface. Just describe the sound you need, and AudioMind handles the rest.

This skill is the result of merging `audio-conductor` and `elevenlabs-mcp-server` into one easy-to-use package, following user feedback for a simpler, more powerful solution.

## When to Use

Load this skill into your agent's environment to give it a comprehensive understanding of and ability to create audio. It's the only audio skill you'll need.

- **User says**: "Create a background track for my video."
- **User says**: "I need a sound effect of a door creaking."
- **User says**: "Generate a voice-over for this script."

## How It Works

AudioMind combines two powerful functions into one seamless workflow:

1.  **Auto-Starting MCP Server**: When loaded, the skill automatically runs the `tools/start_server.sh` script. This launches a background MCP server that exposes **24 powerful audio tools** from ElevenLabs to the agent.
2.  **Intelligent Dispatcher**: The skill's core logic analyzes your natural language request to determine the `audio_type` (music, sfx, tts).
3.  **Tool Execution**: It then calls the appropriate MCP tool (now locally available) to generate the audio.

```
+----------------------------------------------------+
|                    AudioMind Skill                   |
|                                                    |
|  +-----------------------+   +-------------------+   |
|  | Intelligent Dispatcher|   |  MCP Server       |   |
|  | (Analyzes Request)    |-->| (Provides Tools)  |   |
|  +-----------------------+   +-------------------+   |
|                                |                     |
+--------------------------------|---------------------+
                                 |
                                 v
                         [ ElevenLabs API ]
```

## Core Features

-   **All-in-One**: No need to install multiple skills. One skill provides both the tools and the intelligence to use them.
-   **Zero Configuration**: The MCP server starts automatically. Just provide your `ELEVENLABS_API_KEY` as an environment variable.
-   **Model Agnostic (by design)**: While currently powered by ElevenLabs, the skill's architecture allows for future integration of other models without changing the user-facing interface.
-   **24+ Audio Tools**: From simple TTS to complex voice cloning and music composition, a full professional audio suite is at your agent's disposal.

## Getting Started

1.  **Install the Skill**:
    ```bash
    npx clawhub@latest install audiomind
    ```
2.  **Set API Key**: Make sure the `ELEVENLABS_API_KEY` environment variable is set in your agent's environment.
3.  **Use It**: Simply ask your agent for any kind of audio.

## References

-   **[tool_list.md](references/tool_list.md)**: A complete list of all 24 tools provided by the internal MCP server.
-   **[start_server.sh](tools/start_server.sh)**: The script responsible for launching the MCP server.
