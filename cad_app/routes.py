from flask import render_template
from . import app  # __init__.pyからFlaskアプリケーションインスタンスをインポート

from flask import jsonify, request
from .src.optimize import run_optimization

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    
    # run_optimization関数を呼び出して最適化問題を解く
    result = run_optimization(data)

    # 結果をJSON形式で返す
    return jsonify(result)

