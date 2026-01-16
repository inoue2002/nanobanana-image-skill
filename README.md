# Nano Banana Image Skill

Google Gemini API の Nano Banana 機能を使った画像生成スキル for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## 機能

- テキストから画像生成
- 画像から画像生成（image-to-image）
- 画像編集（背景変更、要素追加/削除など）
- 複数バリエーション生成
- アスペクト比・解像度指定

## インストール

```bash
claude mcp add-skill https://github.com/inoue2002/nanobanana-image-skill
```

## 前提条件

環境変数 `GEMINI_API_KEY` を設定してください。

```bash
export GEMINI_API_KEY="your-api-key"
```

APIキーは [Google AI Studio](https://aistudio.google.com/) で取得できます。

## 使い方

Claude Code で以下のような依頼をすると、このスキルが自動的に使用されます：

- 「猫の画像を生成して」
- 「この画像をアニメ風にして」
- 「横長の風景画像を作って」
- 「3パターン作って」

## ライセンス

MIT
