import http.server
import socketserver
import webbrowser
import os

PORT = 8000

# スクリプトのあるディレクトリを取得
web_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(web_dir)  # サーバのワーキングディレクトリを変更

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"サーバーがポート {PORT} で起動しています。")
webbrowser.open(f"http://localhost:{PORT}/static/index.html")  # ブラウザでtest.htmlファイルを開く

httpd.serve_forever()  # サーバーを永続的に起動