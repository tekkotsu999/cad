import os
from datetime import datetime
import pyperclip

# 同一ディレクトリにあるすべての.jsと.htmlと.pyファイルを読み込む
files = [f for f in os.listdir('.') if os.path.isfile(f) and (f.endswith('.js') or f.endswith('.html') or f.endswith('.py') )]

merged_content = ''

# 各ファイルを読み込み、内容を一つの文字列にまとめる
for file in files:
    # ファイルの拡張子によって、言語を決定
    lang = file.split('.')[-1]

    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # マークダウンのコードブロックに変換
    merged_content += f'## File: {file} \n```{lang}\n{content}\n```\n\n'

# 現在のタイムスタンプを取得
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

# 結果を新たなファイルに書き込む
with open(f'{timestamp}_merged_code.md', 'w', encoding='utf-8') as f:
    f.write(merged_content)

# マージしたテキストをクリップボードにコピー
pyperclip.copy(merged_content)
