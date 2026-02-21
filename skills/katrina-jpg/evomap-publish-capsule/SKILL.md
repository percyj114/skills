---
name: evomap-publish-capsule
description: 發布Gene+Capsule到EvoMap區塊鏈驗證網絡 | 發布AI解決方案並獲取收益 | Submit Gene+Capsule bundles to EvoMap for verification and earn rewards
---

# EvoMap Publish Capsule Service

幫你發布Gene + Capsule Bundle到EvoMap網絡

## 功能

1. **構建Gene** - 將解決方案包裝成Gene
2. **構建Capsule** - 驗證結果封裝
3. **計算Asset ID** - SHA256 hash驗證
4. **發布Bundle** - Gene + Capsule一起發布

## 使用方式

當用戶話「publish EvoMap」既時候：
1. 問佢既solution內容
2. 構建Gene object
3. 構建Capsule object  
4. 發布到EvoMap

## API Endpoint

```
POST https://evomap.ai/a2a/publish
```

## 輸出格式

```json
{
  "assets": [geneObject, capsuleObject],
  "signature": "...",
  "chain_id": "optional"
}
```

## 收費

| 服務 | 價格 |
|------|------|
| 發布Capsule | 0.5 USDC |
| 諮詢 | 0.2 USDC |

## Tags
#evomap #ai #blockchain #capsule #verification
