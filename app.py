from flask import Flask, jsonify, request, send_from_directory
from optimize import run_optimization

app = Flask(__name__)

print("here")

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    
    # run_optimization関数を呼び出して最適化問題を解く
    result = run_optimization(data)

    # 結果をJSON形式で返す
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
