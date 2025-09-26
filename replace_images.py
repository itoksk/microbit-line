#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Google Drive image URLs with their captions
images = [
    ("1vQeKyEqZ-ztDkGPm0_WsqGxJcGlCp_r2", "信号機擬似体験サンプルプログラム例"),
    ("1fUmhVUGHrxwTu0zSg2oo3F2KBYz3QcRj", "microbit記号信号機例"),
    ("1bOQZFgjajMYbpuIvhWXGBB0yJTdCGcVc", "スリットへの挿し方"),
    ("1_sL8a4VD7hJI6bRXAeKOL4GwDy5LbXu5", "シニアmicrobitサンプル"),
    ("12C0nxUCMKPmfMOeZ5e-Qu7XlcRGFzgPX", "ダウンロード２"),
    ("1-2B9v2vlgGVp2iUYzj7u0DbA4CQdojhP", "ケーブルとの接続"),
    ("1R2ZQAKqEQbfJeCFGvJBhQQ37UZuUdqEc", "10までおくれ最初から"),
    ("1MRU0qtWXP5bQLEr3s5kqOzGF5D-i3Dv2", "入力くりかえし"),
    ("1B7A1s3tCcSUH9aLECx7JIKAJCYPXAmm8", "点数による分岐"),
    ("1B5o4k1qkMl_VmfKJQ8pnzYZx01kgPdQ9", "プロジェクト"),
    ("1mJLQFrHLHrP3UYajK97uqBAkOHo7-gJ0", "シニアカーリング得点方法２"),
    ("1CHiXGzHJWGYO4ufhLDQ3V3XxTJe-wIUs", "シニアカーリング得点"),
    ("1RJCHsOPPD1FKJR0hDfvkAQYxEodxeAQl", "変数に追加"),
    ("1_nJ3sjxQOSCu8FCWE8pRJQUnvPHt4BxA", "ポイントし発表"),
    ("15QG0fGOdPGBZfBhJQx5Hm0OiDdRPfLgZ", "ダウンロード３")
]

# Read the HTML file
with open('/Users/keisuke/git/microbit-line/lesson-microbit-curling.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all base64 images with empty placeholders first
# This regex matches image tags with base64 data
base64_pattern = r'<img src="data:image/[^"]*">'
placeholders = []

def replace_with_placeholder(match):
    placeholders.append(match.group(0))
    return f"<!--IMAGE_PLACEHOLDER_{len(placeholders)-1}-->"

content = re.sub(base64_pattern, replace_with_placeholder, content)

# Find all figure panels
figure_pattern = r'<figure class="image-panel">\s*<!--IMAGE_PLACEHOLDER_(\d+)-->\s*</figure>'
figure_matches = list(re.finditer(figure_pattern, content))

print(f"Found {len(figure_matches)} figure panels with base64 images")
print(f"Have {len(images)} replacement images")

# Replace each figure panel with the corresponding Google Drive image
for i, match in enumerate(figure_matches):
    if i < len(images):
        file_id, caption = images[i]
        new_figure = f'''<figure class="image-panel">
                    <img src="https://drive.google.com/thumbnail?id={file_id}&sz=w1000" alt="{caption}">
                    <figcaption>{caption}</figcaption>
                </figure>'''
        content = content[:match.start()] + new_figure + content[match.end():]
        # Recalculate matches after replacement
        figure_matches = list(re.finditer(figure_pattern, content))

# Save the updated HTML
with open('/Users/keisuke/git/microbit-line/lesson-microbit-curling.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Replacement complete!")