---
name: nanobanana-image
description: Google Gemini APIのNano Banana機能を使って画像を生成するスキル。「画像を生成して」「イラストを作って」「○○の絵を描いて」「画像を作成」などの依頼があった場合に使用。PNG/JPEG形式で出力可能。
---

# Nano Banana Image Generation

Google Gemini APIのNano Banana機能を使用して、テキストプロンプトから画像を生成する。

## 前提条件

- 環境変数 `GEMINI_API_KEY` または `GOOGLE_API_KEY` が設定されていること
- APIキーは [Google AI Studio](https://aistudio.google.com/) で取得

## 画像生成ワークフロー

### 1. APIキー確認

```bash
echo ${GEMINI_API_KEY:-$GOOGLE_API_KEY}
```

未設定の場合はユーザーに設定を依頼。

### 2. 画像生成実行

`scripts/generate_image.py` を使用：

```bash
python scripts/generate_image.py "プロンプト" --output output.png
```

または直接curlで実行：

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key=${GEMINI_API_KEY:-$GOOGLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{
    "contents": [{"parts": [{"text": "プロンプト"}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
  }' | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 -d > output.png
```

## プロンプトのコツ

- **具体的に**: 「猫」→「窓辺で日向ぼっこする白い猫」
- **スタイル指定**: 「写実的」「アニメ風」「油絵風」「ミニマリスト」
- **構図指定**: 「クローズアップ」「俯瞰」「正面から」
- **照明指定**: 「自然光」「ゴールデンアワー」「ドラマチック」

## エラー対応

| エラー | 対処 |
|--------|------|
| 401 Unauthorized | APIキーを確認・再取得 |
| 429 Rate Limit | 少し待って再試行 |
| コンテンツポリシー違反 | プロンプトを修正 |
