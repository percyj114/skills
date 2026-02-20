---
name: publora-instagram
description: >
  Post or schedule content to Instagram using the Publora API. Use this skill
  when the user wants to publish images, carousels, or reels to Instagram via Publora.
---

# Publora — Instagram

Post and schedule Instagram content via the Publora API.

> **Prerequisite:** Install the `publora` core skill for auth setup and getting platform IDs.

## Get Your Instagram Platform ID

```bash
GET https://api.publora.com/api/v1/platform-connections
# Look for entries like "instagram-456"
```

## Post to Instagram (with Image — required)

Instagram requires media. Always upload an image or video with your post.

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Morning light ☀️ #photography #nature',
    'platforms': ['instagram-456'],
    'scheduledTime': '2026-03-16T09:00:00.000Z'
}).json()

# Step 2: Get upload URL
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'fileName': 'photo.jpg', 'contentType': 'image/jpeg',
    'type': 'image', 'postGroupId': post['postGroupId']
}).json()

# Step 3: Upload
with open('photo.jpg', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

## Schedule Instagram Video / Reel

```python
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'How we ship features in 60 seconds 🚀 #startup #buildinpublic',
    'platforms': ['instagram-456'],
    'scheduledTime': '2026-03-16T18:00:00.000Z'
}).json()

upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'fileName': 'reel.mp4', 'contentType': 'video/mp4',
    'type': 'video', 'postGroupId': post['postGroupId']
}).json()

with open('reel.mp4', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'video/mp4'}, data=f)
```

## Carousel (Multiple Images)

Upload multiple images to the same `postGroupId`:

```python
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': '5 things we learned building our product 👇',
    'platforms': ['instagram-456'],
    'scheduledTime': '2026-03-16T12:00:00.000Z'
}).json()

for filename in ['slide1.jpg', 'slide2.jpg', 'slide3.jpg', 'slide4.jpg', 'slide5.jpg']:
    upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
        'fileName': filename, 'contentType': 'image/jpeg',
        'type': 'image', 'postGroupId': post['postGroupId']
    }).json()
    with open(filename, 'rb') as f:
        requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

## Tips for Instagram

- **Media required** — text-only posts are not supported
- **Square (1:1) or portrait (4:5)** images perform best in feed
- **Reels (9:16)** get significantly more reach than static posts
- **Best times:** Tuesday–Friday, 9 AM–1 PM
- **Hashtags:** 5–10 relevant hashtags; put them in the caption or first comment
- **Caption hook:** First line shows in feed before "more" — make it count
