---
name: nanobanana-image
description: Nano Banana (Google Gemini API) を使って画像を生成するスキル。「画像を生成して」「イラストを作って」「○○の絵を描いて」「画像を作成」「この画像を編集して」「この画像をもとに○○を作って」などの依頼があった場合に使用。テキストからの生成、参照画像からの生成、画像編集に対応。
---

# Nano Banana Image Generation

Google Gemini APIのNano Banana機能を使用した画像生成・編集スキル。

## 前提条件

環境変数 `GEMINI_API_KEY` が設定されていること。
未設定の場合は [Google AI Studio](https://aistudio.google.com/) で取得を依頼。

## 利用可能なモデル

| モデル | ID | 特徴 |
|--------|-----|------|
| Nano Banana | `flash` | 高速・効率重視 |
| Nano Banana Pro | `pro` (デフォルト) | 高品質・推論強化・4K対応 |

## ワークフロー

画像生成後は `open` コマンドでプレビューを提案すること：

```bash
python scripts/generate_image.py "プロンプト" -o image.png && open image.png
```

ユーザーが確認したい場合に備え、生成完了後に「`open image.png` で開きますか？」と提案する。

## 基本的な使い方

### テキストから画像生成

```bash
python scripts/generate_image.py "夕焼けのビーチで遊ぶ犬" -o dog.png
# 生成後: open dog.png
```

### 画像から画像生成（image-to-image）

参照画像をもとに新しい画像を生成：

```bash
python scripts/generate_image.py "この画像をアニメ風にして" -i reference.png -o anime.png
```

複数の参照画像を使用：

```bash
python scripts/generate_image.py "これらの画像を組み合わせて新しいロゴを作成" -i logo1.png -i logo2.png -o new_logo.png
```

### 画像編集

既存の画像を編集：

```bash
python scripts/generate_image.py "背景を宇宙に変更して" -i photo.png -o space_photo.png
python scripts/generate_image.py "人物を削除して" -i group.png -o empty.png
python scripts/generate_image.py "色をもっと鮮やかにして" -i dull.png -o vivid.png
```

### 複数バリエーション生成

```bash
python scripts/generate_image.py "かわいい猫" -n 3 -o cat.png
# → cat_1.png, cat_2.png, cat_3.png
```

### オプション指定

```bash
# アスペクト比指定（16:9横長）
python scripts/generate_image.py "横長の風景" --aspect 16:9 -o landscape.png

# 高解像度出力（Pro のみ 4K 対応）
python scripts/generate_image.py "詳細な建築物" --size 4K -o building.png

# モデル選択
python scripts/generate_image.py "素早く生成" -m flash -o quick.png
```

## コマンドオプション一覧

| オプション | 説明 |
|------------|------|
| `-o, --output` | 出力ファイルパス（デフォルト: output.png） |
| `-m, --model` | モデル選択: `flash` / `pro`（デフォルト: pro） |
| `-i, --input` | 参照画像パス（複数指定可） |
| `-n, --count` | 生成する画像の数 |
| `--aspect` | アスペクト比: 1:1, 16:9, 9:16, 4:3, 3:4 等 |
| `--size` | 画像サイズ: 1K, 2K, 4K |

## プロンプトのコツ

- **具体的に**: 「猫」→「窓辺で日向ぼっこする白い猫」
- **スタイル指定**: 「写実的」「アニメ風」「油絵風」「ミニマリスト」「水彩画」
- **構図指定**: 「クローズアップ」「俯瞰」「正面から」「横顔」
- **照明指定**: 「自然光」「ゴールデンアワー」「ドラマチック」「スタジオ照明」
- **編集時**: 「〇〇を追加して」「〇〇を削除して」「〇〇を変更して」と明確に

## エラー対応

| エラー | 対処 |
|--------|------|
| 401 Unauthorized | APIキーを確認・再取得 |
| 429 Rate Limit | 少し待って再試行 |
| コンテンツポリシー違反 | プロンプトを修正（暴力・成人向け等を避ける） |
| 画像が生成されない | プロンプトをより具体的に |
