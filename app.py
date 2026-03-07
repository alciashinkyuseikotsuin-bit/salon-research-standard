#!/usr/bin/env python3
"""
サロン向け 商品設計サポートツール（スタンダード版）

機能:
1. Yahoo!知恵袋リサーチ（シンプル版と同様）
2. ペルソナ5人自動生成
3. 松竹梅 商品設計
4. 目標金額→価格逆算
5. キャッチコピー10個生成
"""

import json
import os
import re
import sys

from flask import Flask, request, jsonify, send_from_directory

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scraper import search_and_fetch
from analyzer import analyze_results, analyze_concern
from persona_generator import generate_personas
from product_designer import design_products
from price_calculator import calculate_pricing
from copywriter import generate_catchcopy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'static'))

PORT = int(os.environ.get('PORT', 8080))


# ========== ページ配信 ==========

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)


# ========== API: リサーチ ==========

@app.route('/api/search')
def api_search():
    """キーワード検索API"""
    keyword = request.args.get('keyword', '').strip()

    if not keyword:
        return jsonify({'error': 'キーワードを入力してください'}), 400

    try:
        import time as _time
        start = _time.time()
        print(f"[search] キーワード: {keyword}")

        raw_results = search_and_fetch(keyword, max_details=100)
        elapsed = _time.time() - start
        print(f"[search] {len(raw_results)}件の投稿を取得 ({elapsed:.1f}秒)")

        analyzed = analyze_results(raw_results)
        total_elapsed = _time.time() - start
        print(f"[search] 分析完了 (合計{total_elapsed:.1f}秒)")

        return jsonify({
            'keyword': keyword,
            'results': analyzed,
            'count': len(analyzed),
        })

    except Exception as e:
        print(f"[search] エラー: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """テキスト分析API"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip() if data else ''

        if not text:
            return jsonify({'error': 'テキストを入力してください'}), 400

        segments = re.split(r'\n{2,}|_{3,}|-{3,}|={3,}', text)
        segments = [s.strip() for s in segments if len(s.strip()) > 20]

        if not segments:
            segments = [text]

        results = []
        for segment in segments:
            analysis = analyze_concern(segment)
            results.append({
                'title': segment[:80] + ('...' if len(segment) > 80 else ''),
                'url': '',
                'full_text': segment,
                'snippet': '',
                'analysis': analysis,
            })

        results.sort(key=lambda x: x['analysis']['total_score'], reverse=True)

        return jsonify({
            'results': results,
            'count': len(results),
        })

    except Exception as e:
        print(f"[analyze] エラー: {e}")
        return jsonify({'error': str(e)}), 500


# ========== API: ペルソナ生成 ==========

@app.route('/api/persona', methods=['POST'])
def api_persona():
    """ペルソナ5人生成API"""
    try:
        data = request.get_json()
        keyword = data.get('keyword', '').strip() if data else ''
        target_symptom = data.get('target_symptom', '').strip() if data else ''
        search_results = data.get('search_results', []) if data else []

        if not keyword:
            return jsonify({'error': 'キーワードを入力してください'}), 400

        print(f"[persona] キーワード: {keyword}, 症状: {target_symptom}")

        personas = generate_personas(
            keyword=keyword,
            target_symptom=target_symptom,
            search_results=search_results,
            count=5,
        )

        print(f"[persona] {len(personas)}人のペルソナを生成")

        return jsonify({
            'keyword': keyword,
            'personas': personas,
            'count': len(personas),
        })

    except Exception as e:
        print(f"[persona] エラー: {e}")
        return jsonify({'error': str(e)}), 500


# ========== API: 松竹梅商品設計 ==========

@app.route('/api/product', methods=['POST'])
def api_product():
    """松竹梅商品設計API"""
    try:
        data = request.get_json()
        keyword = data.get('keyword', '').strip() if data else ''
        target_symptom = data.get('target_symptom', '').strip() if data else ''
        bamboo_price = data.get('bamboo_price', 0) if data else 0

        if not keyword:
            return jsonify({'error': 'キーワードを入力してください'}), 400

        print(f"[product] キーワード: {keyword}, 竹価格: {bamboo_price}")

        products = design_products(
            keyword=keyword,
            target_symptom=target_symptom,
            bamboo_price=bamboo_price,
        )

        print(f"[product] 商品設計完了")

        return jsonify(products)

    except Exception as e:
        print(f"[product] エラー: {e}")
        return jsonify({'error': str(e)}), 500


# ========== API: 価格逆算 ==========

@app.route('/api/pricing', methods=['POST'])
def api_pricing():
    """目標金額→価格逆算API"""
    try:
        data = request.get_json()

        monthly_target = data.get('monthly_target', 1000000) if data else 1000000
        working_days = data.get('working_days', 22) if data else 22
        slots_per_day = data.get('slots_per_day', 6) if data else 6
        bamboo_price = data.get('bamboo_price', 180000) if data else 180000
        bamboo_months = data.get('bamboo_months', 3) if data else 3
        plum_price = data.get('plum_price', 27000) if data else 27000

        print(f"[pricing] 目標: {monthly_target:,}円/月")

        result = calculate_pricing(
            monthly_target=monthly_target,
            working_days=working_days,
            slots_per_day=slots_per_day,
            bamboo_price=bamboo_price,
            bamboo_months=bamboo_months,
            plum_price=plum_price,
        )

        print(f"[pricing] 計算完了")

        return jsonify(result)

    except Exception as e:
        print(f"[pricing] エラー: {e}")
        return jsonify({'error': str(e)}), 500


# ========== API: キャッチコピー生成 ==========

@app.route('/api/copywrite', methods=['POST'])
def api_copywrite():
    """キャッチコピー10個生成API"""
    try:
        data = request.get_json()
        keyword = data.get('keyword', '').strip() if data else ''
        target_symptom = data.get('target_symptom', '').strip() if data else ''
        personas = data.get('personas', []) if data else []

        if not keyword:
            return jsonify({'error': 'キーワードを入力してください'}), 400

        print(f"[copywrite] キーワード: {keyword}")

        copies = generate_catchcopy(
            keyword=keyword,
            target_symptom=target_symptom,
            personas=personas,
            count=10,
        )

        print(f"[copywrite] {len(copies)}個のコピーを生成")

        return jsonify({
            'keyword': keyword,
            'copies': copies,
            'count': len(copies),
        })

    except Exception as e:
        print(f"[copywrite] エラー: {e}")
        return jsonify({'error': str(e)}), 500


# ========== 起動 ==========

if __name__ == '__main__':
    print(f"""
╔══════════════════════════════════════════════════╗
║   商品設計サポートツール（スタンダード版）          ║
║                                                  ║
║   ブラウザで以下にアクセスしてください:             ║
║   → http://localhost:{PORT}                       ║
║                                                  ║
║   終了: Ctrl+C                                   ║
╚══════════════════════════════════════════════════╝
""")
    app.run(host='0.0.0.0', port=PORT, debug=False)
