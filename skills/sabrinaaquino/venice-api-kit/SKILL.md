---
name: venice-api-kit
description: Complete Venice AI API toolkit - image generation, upscaling, editing, background removal, text-to-speech, embeddings, and video generation. Privacy-focused inference with zero data retention.
homepage: https://venice.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "🏛️",
        "requires": { "bins": ["uv"], "env": ["VENICE_API_KEY"] },
        "primaryEnv": "VENICE_API_KEY",
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

# Venice API Kit

Complete toolkit for Venice AI's API - image generation, upscaling, editing, background removal, text-to-speech, embeddings, and video generation. All endpoints tested and working.

**API Base URL:** `https://api.venice.ai/api/v1`
**Documentation:** [docs.venice.ai](https://docs.venice.ai)

## Setup

1. Get your API key from [venice.ai](https://venice.ai) → Settings → API Keys
2. Set the environment variable:

```bash
export VENICE_API_KEY="your_api_key_here"
```

Or configure in `~/.openclaw/openclaw.json`:

```json5
{
  skills: {
    entries: {
      "venice-ai": {
        apiKey: "your_api_key_here"
      }
    }
  }
}
```

---

## Image Generation

Generate images using Venice's image models. Returns base64 image data.

**Generate an image:**

```bash
uv run {baseDir}/scripts/image_generate.py --prompt "a serene mountain landscape at sunset"
```

**Options:**

- `--prompt` (required): Description of the image (max 7500 chars, model-dependent)
- `--output`: Output filename (default: auto-generated timestamp)
- `--model`: Model ID (default: `flux-2-max`)
- `--size`: Image size: `1024x1024`, `1536x1024`, `1024x1536`, `1792x1024`, `1024x1792` (default: `1024x1024`)
- `--style-id`: Style preset ID (use `--list-styles` to see available)
- `--negative-prompt`: What to avoid in the image
- `--seed`: Seed for reproducible generation

**List available styles:**

```bash
uv run {baseDir}/scripts/image_generate.py --list-styles
```

---

## Image Upscaling

Upscale images 1-4x with optional AI enhancement. Returns binary PNG.

```bash
uv run {baseDir}/scripts/image_upscale.py --image input.png --scale 2
```

**Options:**

- `--image` (required): Input image path or URL
- `--output`: Output filename (default: `upscaled-{timestamp}.png`)
- `--scale`: Scale factor 1-4 (default: `2`). Scale of 1 requires `--enhance`
- `--enhance`: Enable AI enhancement during upscaling
- `--enhance-creativity`: How much AI can change (0-1, higher = more creative)
- `--enhance-prompt`: Style to apply (e.g., "gold", "marble", "cinematic")
- `--replication`: Preserve original lines/noise (0-1, higher = less hallucination)

**Example with enhancement:**

```bash
uv run {baseDir}/scripts/image_upscale.py --image photo.png --scale 2 --enhance --enhance-prompt "cinematic lighting"
```

---

## Image Editing

Edit images with AI using text prompts. Returns binary PNG.

```bash
uv run {baseDir}/scripts/image_edit.py --image photo.png --prompt "add sunglasses"
```

**Options:**

- `--image` (required): Input image path or URL
- `--prompt` (required): Edit instructions (e.g., "remove the tree", "change sky to sunset")
- `--output`: Output filename (default: `edited-{timestamp}.png`)
- `--model`: Edit model (default: `qwen-edit`). Available: `qwen-edit`, `flux-2-max-edit`, `gpt-image-1-5-edit`, `nano-banana-pro-edit`, `seedream-v4-edit`
- `--aspect-ratio`: Output aspect ratio: `auto`, `1:1`, `3:2`, `16:9`, `21:9`, `9:16`, `2:3`, `3:4`

---

## Background Removal

Remove backgrounds from images. Returns binary PNG with transparency.

```bash
uv run {baseDir}/scripts/image_background_remove.py --image photo.png
```

**Options:**

- `--image` (required): Input image path or URL
- `--output`: Output filename (default: `no-background-{timestamp}.png`)

---

## Text-to-Speech

Convert text to speech with multiple voices and formats. Returns binary audio.

```bash
uv run {baseDir}/scripts/audio_speech.py --text "Hello, welcome to Venice AI"
```

**Options:**

- `--text` (required): Text to convert (max 4096 characters)
- `--output`: Output filename (default: `speech-{timestamp}.{format}`)
- `--voice`: Voice ID (default: `af_nicole`)
- `--model`: TTS model (default: `tts-kokoro`)
- `--speed`: Speed multiplier 0.25-4.0 (default: `1.0`)
- `--format`: Audio format: `mp3`, `opus`, `aac`, `flac`, `wav`, `pcm` (default: `mp3`)
- `--streaming`: Stream audio sentence by sentence

**Available voices:**

- American Female: `af_alloy`, `af_aoede`, `af_bella`, `af_heart`, `af_jadzia`, `af_jessica`, `af_kore`, `af_nicole`, `af_nova`, `af_river`, `af_sarah`, `af_sky`
- American Male: `am_adam`, `am_echo`, `am_eric`
- British Female: `bf_emma`, `bf_isabella`, `bf_alice`
- British Male: `bm_george`, `bm_lewis`, `bm_daniel`

---

## Embeddings

Generate vector embeddings for RAG applications.

```bash
uv run {baseDir}/scripts/embeddings.py --text "Your text to embed"
```

**Options:**

- `--text`: Text to embed (use this OR `--file`)
- `--file`: Read text from file
- `--output`: Save embeddings to JSON file
- `--model`: Embedding model (default: `text-embedding-3-small`)

---

## Video Generation

Generate videos from text prompts. Some models require a reference image. Async with polling.

**Text-to-video:**

```bash
uv run {baseDir}/scripts/video_generate.py --prompt "a cat playing piano"
```

**Image-to-video (requires reference image):**

```bash
uv run {baseDir}/scripts/video_generate.py --prompt "a cat playing piano" --image reference.png
```

**Options:**

- `--prompt` (required): Video description (max 2500 characters)
- `--image`: Reference image (path or URL) - required for image-to-video models
- `--output`: Output filename (default: `venice-video-{timestamp}.mp4`)
- `--model`: Video model (default: `wan-2.6-image-to-video`). Also: `wan-2.6-text-to-video`, `wan-2.6-flash-image-to-video`
- `--duration`: Video duration: `5s` or `10s` (default: `5s`)
- `--resolution`: Resolution: `480p`, `720p`, `1080p` (default: `720p`)
- `--aspect-ratio`: Aspect ratio (e.g., `16:9`, `9:16`, `1:1`)
- `--negative-prompt`: What to avoid in the video
- `--max-wait`: Max seconds to wait for completion (default: `600`)

---

## Runtime Note

This skill uses `uv run` which automatically installs Python dependencies (httpx) via [PEP 723](https://peps.python.org/pep-0723/) inline script metadata. No manual Python package installation required - `uv` handles everything.

---

## Security Notes

- **Privacy:** All inference is private—no logging, no training on your data
- **API Key:** Store securely, never commit to version control
- **Data:** Venice does not retain request/response data
- **Trust:** Verify you trust Venice.ai before sending sensitive data

## API Reference

| Endpoint | Description | Response |
|----------|-------------|----------|
| `/image/generate` | Full image generation | JSON with base64 images |
| `/images/generations` | OpenAI-compatible generation | JSON with base64 |
| `/image/upscale` | Image upscaling with enhancement | Binary PNG |
| `/image/edit` | AI image editing | Binary PNG |
| `/image/background-remove` | Background removal | Binary PNG (transparent) |
| `/audio/speech` | Text-to-speech | Binary audio |
| `/embeddings` | Vector embeddings | JSON |
| `/video/queue` | Queue video generation | JSON with queue_id |
| `/video/retrieve` | Retrieve completed video | Binary MP4 or JSON status |

Full API docs: [docs.venice.ai](https://docs.venice.ai)
