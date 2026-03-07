"""
松竹梅 商品設計モジュール（ルールベース）

Obsidian知識ベース:
- 売上 = 新規数 x 客単価 x リピート回数
- LTVを最速で上げる: 客単価とリピート回数をセットで売る
- 18万〜50万円のコース設計が基本
- 梅（ダウンセル）: 1ヶ月お試し or 3回お試し
- 竹（メイン）: 本命商品。一番売りたい内容と金額
- 松（アンカリング）: 竹が安く見えるための高額商品
- アンカリング: 提示金額の約3倍の合計金額を見せる
- 月3万円が心理的限界値（サブスク）
- 「財布を開いた直後」が最もバックエンドを売りやすい

商品構造:
  松: アンカリング用。竹の2〜3倍の価格。VIP・完全カスタム
  竹: メイン商品。一番売りたい。回数券 or コース
  梅: ダウンセル。お試し1ヶ月 or 3回体験。竹への導線
"""

from typing import Dict, List, Optional


# ============================================================
# 業種別 商品テンプレート
# ============================================================

PRODUCT_TEMPLATES = {
    'pain': {
        'service_name': '根本改善プログラム',
        'pine': {  # 松
            'name': 'プレミアム完全改善コース',
            'sessions': '24回（6ヶ月）',
            'duration': '6ヶ月',
            'price_multiplier': 2.5,  # 竹の何倍か
            'features': [
                '週2回の施術（月8回）',
                '完全オーダーメイドの施術プラン',
                'LINEでの毎日の経過サポート',
                'セルフケア動画（専用撮影）',
                '姿勢・歩行分析レポート（月1回）',
                '再発防止メンテナンスプラン付き',
                '優先予約枠の確保',
                '家族1名の初回施術無料',
            ],
            'guarantee': '改善が見られない場合、追加施術を無料で提供',
            'anchor_description': '本気で根本から改善したい方のための最上位プラン',
        },
        'bamboo': {  # 竹（メイン）
            'name': '集中改善コース',
            'sessions': '12回（3ヶ月）',
            'duration': '3ヶ月',
            'price_base': 180000,  # 基本価格
            'features': [
                '週1回の施術（月4回）',
                'カスタマイズ施術プラン',
                'LINEでの質問サポート',
                'セルフケア指導（来院時）',
                '中間チェック＆プラン調整',
            ],
            'guarantee': '3ヶ月で改善を実感できなければ追加3回無料',
            'selling_points': [
                '一番人気のコース',
                '多くの方がこのコースで改善を実感',
                '費用対効果が最も高い',
            ],
        },
        'plum': {  # 梅（ダウンセル）
            'name': '体験お試しコース',
            'sessions_options': [
                {'sessions': '3回', 'duration': '3週間', 'price_ratio': 0.15},
                {'sessions': '1ヶ月（4回）', 'duration': '1ヶ月', 'price_ratio': 0.22},
            ],
            'features': [
                '原因特定のための検査・カウンセリング',
                '施術体験',
                '改善プランのご提案',
            ],
            'purpose': '竹コースの良さを体感してもらうための導線',
        },
    },
    'posture': {
        'service_name': '姿勢改善プログラム',
        'pine': {
            'name': 'トータルボディメイクコース',
            'sessions': '24回（6ヶ月）',
            'duration': '6ヶ月',
            'price_multiplier': 2.5,
            'features': [
                '週2回の施術＆トレーニング',
                'AI姿勢分析（月1回）',
                'パーソナルトレーニング指導',
                'LINEでの姿勢チェック（写真添削）',
                '洋服の選び方アドバイス',
                'ビフォーアフター写真撮影',
                'メンテナンスプラン付き',
            ],
            'guarantee': '目標姿勢に到達するまでサポート継続',
            'anchor_description': '見た目も体の中身も完全に生まれ変わるプラン',
        },
        'bamboo': {
            'name': '姿勢矯正集中コース',
            'sessions': '12回（3ヶ月）',
            'duration': '3ヶ月',
            'price_base': 150000,
            'features': [
                '週1回の施術',
                '姿勢分析レポート',
                'セルフケアエクササイズ指導',
                '中間チェック',
            ],
            'guarantee': '3ヶ月で姿勢の変化を実感できなければ追加施術無料',
            'selling_points': [
                '一番選ばれているコース',
                '3ヶ月で目に見える変化を実感',
            ],
        },
        'plum': {
            'name': '姿勢チェック＆お試し体験',
            'sessions_options': [
                {'sessions': '3回', 'duration': '3週間', 'price_ratio': 0.15},
                {'sessions': '1ヶ月（4回）', 'duration': '1ヶ月', 'price_ratio': 0.22},
            ],
            'features': [
                '姿勢の歪みチェック',
                '施術体験',
                '改善プランの提案',
            ],
            'purpose': '自分の姿勢の問題を可視化し、改善への意欲を高める',
        },
    },
    'beauty': {
        'service_name': '美容改善プログラム',
        'pine': {
            'name': 'プレミアムビューティーコース',
            'sessions': '24回（6ヶ月）',
            'duration': '6ヶ月',
            'price_multiplier': 2.5,
            'features': [
                '週2回の施術',
                'フェイシャル＆ボディのトータルケア',
                'ホームケア化粧品セット付き',
                'LINEでのスキンケア相談',
                'メイクアドバイス',
                'ビフォーアフター写真撮影',
                '食事・生活習慣アドバイス',
            ],
            'guarantee': '満足いただけなければ残り回数分を返金',
            'anchor_description': '内面からも外面からも本来の美しさを取り戻すプラン',
        },
        'bamboo': {
            'name': '集中ビューティーコース',
            'sessions': '12回（3ヶ月）',
            'duration': '3ヶ月',
            'price_base': 200000,
            'features': [
                '週1回の施術',
                '肌・体質分析',
                'ホームケアアドバイス',
                '経過チェック',
            ],
            'guarantee': '3ヶ月で変化を実感できなければ追加施術無料',
            'selling_points': [
                '一番人気のコース',
                '多くの方が3ヶ月で変化を実感',
            ],
        },
        'plum': {
            'name': 'お試しビューティー体験',
            'sessions_options': [
                {'sessions': '3回', 'duration': '3週間', 'price_ratio': 0.12},
                {'sessions': '1ヶ月（4回）', 'duration': '1ヶ月', 'price_ratio': 0.18},
            ],
            'features': [
                'カウンセリング＆肌分析',
                '施術体験',
                '改善プランのご提案',
            ],
            'purpose': '施術の効果を実感してもらい、集中コースへの導線にする',
        },
    },
    'mental': {
        'service_name': '心身バランス回復プログラム',
        'pine': {
            'name': 'トータルリカバリーコース',
            'sessions': '24回（6ヶ月）',
            'duration': '6ヶ月',
            'price_multiplier': 2.5,
            'features': [
                '週2回の施術',
                '自律神経測定（月1回）',
                '生活習慣改善サポート',
                'LINEでの体調相談',
                'アロマ・リラクゼーションケア付き',
                '睡眠改善プログラム',
            ],
            'guarantee': '改善を実感するまでサポート継続',
            'anchor_description': '心と体の両面から根本的に立て直すプラン',
        },
        'bamboo': {
            'name': 'バランス回復コース',
            'sessions': '12回（3ヶ月）',
            'duration': '3ヶ月',
            'price_base': 180000,
            'features': [
                '週1回の施術',
                '自律神経チェック',
                'セルフケア指導',
                '経過チェック＆プラン調整',
            ],
            'guarantee': '3ヶ月で体調の変化を実感できなければ追加施術無料',
            'selling_points': [
                '一番選ばれているコース',
                '3ヶ月で「朝起きるのが楽になった」と実感する方が多数',
            ],
        },
        'plum': {
            'name': 'お試しリカバリー体験',
            'sessions_options': [
                {'sessions': '3回', 'duration': '3週間', 'price_ratio': 0.15},
                {'sessions': '1ヶ月（4回）', 'duration': '1ヶ月', 'price_ratio': 0.22},
            ],
            'features': [
                '自律神経チェック＆カウンセリング',
                '施術体験',
                '改善プランのご提案',
            ],
            'purpose': '自分の体の状態を客観的に知ってもらう',
        },
    },
}

# デフォルト
DEFAULT_PRODUCT = PRODUCT_TEMPLATES['pain']


def design_products(
    keyword: str,
    target_symptom: str = '',
    bamboo_price: int = 0,
    category: str = '',
) -> Dict:
    """
    松竹梅の商品を設計する

    Args:
        keyword: キーワード
        target_symptom: ターゲット症状
        bamboo_price: 竹の価格（0の場合はテンプレートのデフォルト）
        category: カテゴリ（空の場合はキーワードから自動判定）

    Returns:
        松竹梅の商品設計
    """
    # カテゴリ判定
    if not category:
        category_keywords = {
            'pain': ['痛', '腰', '肩', '首', '膝', 'ヘルニア', '神経痛', '頭痛'],
            'posture': ['猫背', 'O脚', '骨盤', '姿勢', '歪み', '反り腰'],
            'beauty': ['小顔', 'エラ', 'たるみ', 'シワ', 'ニキビ', '肌', '美容', '痩'],
            'mental': ['自律神経', '不眠', 'ストレス', 'うつ', '疲労', 'めまい'],
        }
        best_cat = 'pain'
        best_score = 0
        for cat, words in category_keywords.items():
            score = sum(len(w) for w in words if w in keyword)
            if score > best_score:
                best_score = score
                best_cat = cat
        category = best_cat

    template = PRODUCT_TEMPLATES.get(category, DEFAULT_PRODUCT)
    symptom = target_symptom if target_symptom else keyword

    # 竹の価格
    bp = bamboo_price if bamboo_price > 0 else template['bamboo']['price_base']

    # 松の価格（竹の2.5倍）
    pine_price = int(bp * template['pine']['price_multiplier'])

    # 梅の価格（竹の15〜22%）
    plum_options = []
    for opt in template['plum']['sessions_options']:
        plum_options.append({
            'sessions': opt['sessions'],
            'duration': opt['duration'],
            'price': int(bp * opt['price_ratio']),
        })

    # アンカリング効果の説明
    total_value = int(pine_price * 1.2)  # 松の1.2倍を「本来の価値」として提示
    anchoring_text = f'本来 {total_value:,}円相当の内容を、{pine_price:,}円でご提供'

    result = {
        'category': category,
        'service_name': template['service_name'],
        'symptom': symptom,

        'pine': {
            'rank': '松',
            'name': template['pine']['name'].replace('改善', f'{symptom}改善') if symptom not in template['pine']['name'] else template['pine']['name'],
            'price': pine_price,
            'price_display': f'{pine_price:,}円',
            'sessions': template['pine']['sessions'],
            'duration': template['pine']['duration'],
            'features': template['pine']['features'],
            'guarantee': template['pine']['guarantee'],
            'description': template['pine']['anchor_description'],
            'role': 'アンカリング商品：竹コースが「お得」に見える基準を作る',
            'anchoring_text': anchoring_text,
        },

        'bamboo': {
            'rank': '竹',
            'name': template['bamboo']['name'].replace('改善', f'{symptom}改善') if symptom not in template['bamboo']['name'] else template['bamboo']['name'],
            'price': bp,
            'price_display': f'{bp:,}円',
            'sessions': template['bamboo']['sessions'],
            'duration': template['bamboo']['duration'],
            'features': template['bamboo']['features'],
            'guarantee': template['bamboo']['guarantee'],
            'selling_points': template['bamboo']['selling_points'],
            'role': 'メイン商品：一番売りたい商品。費用対効果が最も高い',
            'per_session': f'{int(bp / 12):,}円/回',
            'per_day': f'{int(bp / 90):,}円/日',
        },

        'plum': {
            'rank': '梅',
            'name': template['plum']['name'],
            'options': plum_options,
            'features': template['plum']['features'],
            'purpose': template['plum']['purpose'],
            'role': 'ダウンセル：「まずはお試し」から始めて竹への導線を作る',
        },

        'sales_tips': {
            'presentation_order': '松→竹→梅の順に提示（アンカリング効果）',
            'closing_phrase': '「どちらのコースが良いと思いましたか？」（二者択一法）',
            'objection_handling': {
                'expensive': f'1日あたりに換算すると{int(bp / 90):,}円の投資です',
                'uncertain': '改善を実感できなければ追加施術を無料で提供します',
                'time': '週1回60分、たった3ヶ月の投資で何年もの悩みが解決します',
            },
        },
    }

    return result
