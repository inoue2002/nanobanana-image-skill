#!/usr/bin/env python3
"""Nano Banana (Gemini API) を使用して画像を生成するスクリプト"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error


def get_api_key():
    """環境変数からAPIキーを取得"""
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        print("Error: GEMINI_API_KEY または GOOGLE_API_KEY を設定してください", file=sys.stderr)
        sys.exit(1)
    return key


def generate_image(prompt: str, output_path: str) -> None:
    """Gemini APIを使用して画像を生成"""
    api_key = get_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }

    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"API Error ({e.code}): {error_body}", file=sys.stderr)
        sys.exit(1)

    # 画像データを抽出
    candidates = result.get("candidates", [])
    if not candidates:
        print("Error: 画像が生成されませんでした", file=sys.stderr)
        sys.exit(1)

    parts = candidates[0].get("content", {}).get("parts", [])
    image_data = None

    for part in parts:
        if "inlineData" in part:
            image_data = part["inlineData"]["data"]
            break

    if not image_data:
        print("Error: 画像データが見つかりません", file=sys.stderr)
        sys.exit(1)

    # Base64デコードして保存
    image_bytes = base64.b64decode(image_data)
    with open(output_path, "wb") as f:
        f.write(image_bytes)

    print(f"画像を保存しました: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Nano Banana で画像を生成")
    parser.add_argument("prompt", help="画像生成のプロンプト")
    parser.add_argument("-o", "--output", default="output.png", help="出力ファイルパス (default: output.png)")

    args = parser.parse_args()
    generate_image(args.prompt, args.output)


if __name__ == "__main__":
    main()
