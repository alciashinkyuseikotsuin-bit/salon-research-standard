"""
キャッチコピー自動生成モジュール（ルールベース）

Obsidian知識ベース:
- 3つの脳モデル: 爬虫類脳(恐怖)→哺乳類脳(共感)→人間脳(論理)
- 影響力の武器: 希少性、社会的証明、権威性、返報性
- 脳科学マーケティング: アンカリング、損失回避、単純接触効果
- プリンセスマーケティング: 「本来の自分に戻る」物語
- 売れるコピー言い換え図鑑: 抽象→具体、静的→動的、メリット→損失
- DotCom Secrets: フック・ストーリー・オファー
- 3つのNot: 読まない・信じない・行動しない

10個のキャッチコピーを生成:
1. 損失回避型（爬虫類脳に訴求）
2. 具体数字型（信頼性）
3. 好奇心フック型（情報の空白）
4. 社会的証明型（権威・実績）
5. 体感変換型（五感表現）
6. 回帰型（本来の自分に戻る）
7. 専門特化型（ニッチ宣言）
8. 二者択一型（損得分類）
9. 否定形フック型（禁止で注意喚起）
10. 共感ストーリー型（感情脳に訴求）
"""

import random
from typing import List, Dict, Optional


# ============================================================
# コピー生成テンプレート（10タイプ）
# ============================================================

COPY_TEMPLATES = {
    'loss_aversion': {
        'label': '損失回避型',
        'brain': '爬虫類脳（本能）',
        'principle': '「得る喜び」より「失う痛み」が2倍強い（プロスペクト理論）',
        'templates': [
            '放置すると{years}年後、{negative_future}になるかもしれません',
            'その{symptom}、我慢し続けると{negative_consequence}',
            '「まだ大丈夫」が一番危険。{symptom}を放置した末路とは',
            '{symptom}を{years}年放置した人の{percentage}%が{negative_outcome}に',
            'あなたの{symptom}、実は{hidden_cause}が原因かもしれません',
        ],
    },
    'specific_number': {
        'label': '具体数字型',
        'brain': '人間脳（論理）',
        'principle': '具体的な数字が入ると「信じない」の壁を突破できる',
        'templates': [
            '{number}人の{symptom}に悩む方が笑顔を取り戻しました',
            'たった{sessions}回で{percentage}%の方が変化を実感',
            '{years}年間で{number}人が選んだ{area}No.1の{service}',
            '施術{minutes}分で、{effect}を実感する方が続出',
            '満足度{satisfaction}%。{symptom}専門の{service}',
        ],
    },
    'curiosity_hook': {
        'label': '好奇心フック型',
        'brain': '爬虫類脳（本能）',
        'principle': '情報の空白を作り「知りたい」欲求を刺激する',
        'templates': [
            'なぜ、{wrong_approach}では{symptom}は治らないのか？',
            '{symptom}の本当の原因は「{real_cause}」だった',
            '医師も驚いた。{symptom}が{short_period}で改善した理由',
            '{common_belief}は間違い？{symptom}の新常識',
            'あの{famous_method}では届かない{symptom}の根本原因とは',
        ],
    },
    'social_proof': {
        'label': '社会的証明型',
        'brain': '人間脳（論理）',
        'principle': '「みんなが選んでいる」安心感。権威性で信頼を担保する',
        'templates': [
            '口コミ評価{rating}。「ここに来てよかった」の声が止まりません',
            '{area}で「{symptom}なら{shop_name}」と言われる理由',
            'リピート率{repeat_rate}%。一度来ると分かる本物の技術',
            '「もっと早く来ればよかった」当院で最も多い感想です',
            '{media}にも取り上げられた{symptom}専門の施術法',
        ],
    },
    'sensory': {
        'label': '体感変換型',
        'brain': '哺乳類脳（感情）',
        'principle': '五感・体感表現で潜在意識に訴えかける',
        'templates': [
            'まるで{body_part}が羽のように軽くなる感覚、味わいませんか？',
            '朝起きた瞬間の「あ、{positive_feeling}」を取り戻しませんか',
            '施術後、思わず「{exclamation}」と声が出る{number}分間',
            '{body_part}がスーッと伸びていく。あの感覚を体験してください',
            '鏡を見るのが楽しくなる。そんな{time_period}後の自分を想像してください',
        ],
    },
    'return_to_self': {
        'label': '回帰型（本来の自分へ）',
        'brain': '哺乳類脳（感情）',
        'principle': 'プリンセスマーケティング：「変身」ではなく「本来の自分に戻る」物語',
        'templates': [
            '本来のあなたの{natural_quality}を取り戻しませんか',
            '{symptom}に奪われた「あの頃の自分」を取り戻す{duration}',
            'あなたはもともと{positive_state}だった。それを思い出すお手伝いをします',
            '{symptom}さえなければ。その「もし」を現実にする場所',
            '頑張っているあなたへ。{body_part}の悲鳴、聞こえていますか？',
        ],
    },
    'specialist': {
        'label': '専門特化型',
        'brain': '人間脳（論理）',
        'principle': '対象を限定して専門性を演出。「あなた専用」感を出す',
        'templates': [
            '{target_person}専門。{symptom}を根本から整える{service}',
            '{area}で唯一の{symptom}専門{service_type}',
            '{target_person}の{symptom}に特化して{years}年。だから結果が違います',
            '{symptom}×{related_issue}の両方を同時に解決できる唯一のサロン',
            'お医者さんに「様子を見ましょう」と言われた{symptom}の方へ',
        ],
    },
    'two_choices': {
        'label': '二者択一型',
        'brain': '爬虫類脳（本能）',
        'principle': '「自分はどちら？」と考えさせ、自分事化させる',
        'templates': [
            '{symptom}で{positive_action}人、{negative_action}人。あなたはどちら？',
            'その{symptom}、「治る人」と「治らない人」の決定的な違い',
            '{years}後に{positive_future}か、{negative_future}か。決めるのは今です',
            '{symptom}を「我慢する人生」と「解決する人生」、どちらを選びますか？',
            '同じ{symptom}なのに、改善する人としない人の差は「{difference}」だけ',
        ],
    },
    'negative_hook': {
        'label': '否定形フック型',
        'brain': '爬虫類脳（本能）',
        'principle': '禁止・否定で注意を惹き、「読まない」の壁を突破する',
        'templates': [
            '{symptom}の方、絶対に{wrong_action}しないでください',
            'まだ{wrong_approach}で{symptom}を誤魔化しますか？',
            '{symptom}に{wrong_product}は逆効果。その理由とは',
            '知らないと損する{symptom}の{number}つの真実',
            '{symptom}が治らない人がやりがちな{number}つの間違い',
        ],
    },
    'empathy_story': {
        'label': '共感ストーリー型',
        'brain': '哺乳類脳（感情）',
        'principle': 'ストーリーで脳波を同調（ニューラルカップリング）させ共感を生む',
        'templates': [
            '「{symptom}さえなければ」そう思い続けた{years}年間。でも{turning_point}',
            '何をしても改善しなかった{symptom}。最後に見つけた答えは「{answer}」でした',
            '「もう諦めようかな」そんなあなたにこそ、知ってほしいことがあります',
            'かつて私も{symptom}で{suffering}。だからわかります、あなたの辛さが',
            '「先生、{happy_voice}」この言葉を聞くために、私はこの仕事をしています',
        ],
    },
}

# テンプレート変数のバリエーション（カテゴリ別）
COPY_VARIABLES = {
    'pain': {
        'symptoms': ['腰痛', '肩こり', '頭痛', '膝の痛み', '坐骨神経痛'],
        'body_parts': ['腰', '肩', '首', '背中', '体全体'],
        'negative_futures': ['歩けなくなる', '手術が必要になる', '寝たきりになる'],
        'negative_consequences': ['日常生活に支障が出ます', '仕事を続けられなくなるかも'],
        'negative_outcomes': ['慢性化', '重症化'],
        'hidden_causes': ['姿勢の歪み', '骨盤のズレ', 'インナーマッスルの衰え'],
        'wrong_approaches': ['湿布と痛み止め', 'マッサージだけ', 'ストレッチだけ'],
        'wrong_actions': ['我慢し続ける', '痛み止めに頼り続ける'],
        'wrong_products': ['湿布', 'コルセット', '市販の痛み止め'],
        'real_causes': ['骨盤の歪み', 'インナーマッスルの弱化', '背骨のアライメント'],
        'common_beliefs': ['「年のせい」', '「運動不足」', '「筋力低下」'],
        'famous_methods': ['マッサージ', '整形外科', 'ストレッチ'],
        'positive_feelings': ['痛くない', '軽い', 'スッキリ'],
        'exclamations': ['うわ、軽い！', '全然違う！', 'えっ、痛くない！'],
        'natural_qualities': ['痛みのない日常', '自由に動ける体', '朝スッキリ起きられる毎日'],
        'positive_states': ['痛みなく自由に動けていた', '何の不安もなく過ごしていた'],
        'target_persons': ['デスクワーカー', '産後ママ', '立ち仕事の方', '40代以上の女性'],
        'related_issues': ['姿勢改善', '骨盤矯正', 'インナーマッスル強化'],
        'positive_actions': ['根本解決する', '原因を見つけて改善する'],
        'negative_actions': ['我慢し続ける', '痛み止めで誤魔化す'],
        'positive_futures': ['痛みのない毎日', '自由に動ける体'],
        'differences': ['根本原因にアプローチするかどうか'],
        'turning_points': ['根本原因が分かった瞬間、全てが変わりました'],
        'answers': ['原因へのアプローチ', '骨盤から整えること'],
        'sufferings': ['仕事を休んだことも', '夜眠れない日もありました'],
        'happy_voices': ['久しぶりに朝までぐっすり眠れました', '子供と走り回れるようになりました'],
        'areas': ['地域', '当エリア'],
        'service_types': ['整体院', '施術院', '治療院'],
    },
    'beauty': {
        'symptoms': ['たるみ', 'ほうれい線', 'シワ', '肌荒れ', 'むくみ', 'エラ張り'],
        'body_parts': ['お顔', 'フェイスライン', '肌', '目元'],
        'negative_futures': ['見た目年齢+10歳', '戻せないほどのたるみ'],
        'negative_consequences': ['年齢より老けて見られ続けます', '自信を失い続けます'],
        'negative_outcomes': ['進行', '老化加速'],
        'hidden_causes': ['筋膜の癒着', '血流不良', '骨格の歪み'],
        'wrong_approaches': ['高級化粧品だけ', 'セルフマッサージだけ'],
        'wrong_actions': ['化粧で隠し続ける', '諦めてしまう'],
        'wrong_products': ['美顔ローラー', '高額クリーム'],
        'real_causes': ['表情筋の衰え', '頭蓋骨の歪み', 'リンパの滞り'],
        'common_beliefs': ['「年だから仕方ない」', '「化粧品で何とかなる」'],
        'famous_methods': ['化粧品', 'セルフケア', '美容クリニック'],
        'positive_feelings': ['ハリがある', '若返った', 'ツヤがある'],
        'exclamations': ['え、小さくなってる！', 'リフトアップしてる！', '肌がツルツル！'],
        'natural_qualities': ['ハリのある肌', 'すっきりしたフェイスライン', '自信のある笑顔'],
        'positive_states': ['自信を持って笑えていた', '写真を撮るのが好きだった'],
        'target_persons': ['30代からの女性', '産後ママ', '接客業の方'],
        'related_issues': ['小顔矯正', 'リフトアップ', '肌質改善'],
        'positive_actions': ['根本からケアする', 'プロの手で整える'],
        'negative_actions': ['化粧で隠し続ける', '高額化粧品に頼る'],
        'positive_futures': ['自信を持ったすっぴん', '鏡が好きになる毎日'],
        'differences': ['内側からアプローチするかどうか'],
        'turning_points': ['骨格から整えたら、全てが変わりました'],
        'answers': ['骨格×筋膜のアプローチ'],
        'sufferings': ['鏡を見るのが嫌でした', '人に会うのが億劫でした'],
        'happy_voices': ['友達に「何かした？」って聞かれました', 'すっぴんに自信が持てるようになりました'],
        'areas': ['地域', '当エリア'],
        'service_types': ['サロン', 'エステ', 'フェイシャルサロン'],
    },
}

# デフォルト変数（他カテゴリのフォールバック）
DEFAULT_COPY_VARS = COPY_VARIABLES['pain']


def _fill_template(template: str, variables: Dict, keyword: str) -> str:
    """テンプレートに変数を埋め込む"""
    result = template

    # 各変数を置換
    replacements = {
        '{symptom}': keyword,
        '{years}': str(random.choice([3, 5, 7, 10])),
        '{number}': str(random.choice([847, 1200, 2847, 3500, 5000])),
        '{percentage}': str(random.choice([87, 89, 92, 95, 97])),
        '{sessions}': str(random.choice([3, 5, 8, 10, 12])),
        '{minutes}': str(random.choice([30, 40, 50, 60])),
        '{satisfaction}': str(random.choice([94, 96, 97, 98])),
        '{rating}': str(random.choice(['4.8', '4.9', '5.0'])),
        '{repeat_rate}': str(random.choice([89, 92, 95, 97])),
        '{duration}': random.choice(['3ヶ月', '90日間', '12回']),
        '{time_period}': random.choice(['3ヶ月', '1ヶ月', '半年']),
        '{short_period}': random.choice(['3回', '1ヶ月', '2週間']),
        '{service}': random.choice(['施術', '整体', 'ケア']),
        '{media}': random.choice(['テレビ', '雑誌', 'メディア']),
        '{shop_name}': '当院',
        '{area}': random.choice(['地域', 'エリア', '口コミ']),
    }

    # カテゴリ別変数
    list_keys = {
        '{body_part}': 'body_parts',
        '{negative_future}': 'negative_futures',
        '{negative_consequence}': 'negative_consequences',
        '{negative_outcome}': 'negative_outcomes',
        '{hidden_cause}': 'hidden_causes',
        '{wrong_approach}': 'wrong_approaches',
        '{wrong_action}': 'wrong_actions',
        '{wrong_product}': 'wrong_products',
        '{real_cause}': 'real_causes',
        '{common_belief}': 'common_beliefs',
        '{famous_method}': 'famous_methods',
        '{positive_feeling}': 'positive_feelings',
        '{exclamation}': 'exclamations',
        '{natural_quality}': 'natural_qualities',
        '{positive_state}': 'positive_states',
        '{target_person}': 'target_persons',
        '{related_issue}': 'related_issues',
        '{positive_action}': 'positive_actions',
        '{negative_action}': 'negative_actions',
        '{positive_future}': 'positive_futures',
        '{difference}': 'differences',
        '{turning_point}': 'turning_points',
        '{answer}': 'answers',
        '{suffering}': 'sufferings',
        '{happy_voice}': 'happy_voices',
        '{service_type}': 'service_types',
    }

    for placeholder, key in list_keys.items():
        if placeholder in result and key in variables:
            result = result.replace(placeholder, random.choice(variables[key]))

    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)

    return result


def generate_catchcopy(
    keyword: str,
    target_symptom: str = '',
    personas: Optional[List[Dict]] = None,
    count: int = 10,
) -> List[Dict]:
    """
    キャッチコピーを10個生成する

    Args:
        keyword: キーワード
        target_symptom: ターゲット症状
        personas: ペルソナ情報（あればよりパーソナライズ）
        count: 生成数

    Returns:
        キャッチコピーのリスト
    """
    symptom = target_symptom if target_symptom else keyword

    # カテゴリ判定
    category = 'pain'
    for cat, vars_dict in COPY_VARIABLES.items():
        if any(s in keyword for s in vars_dict['symptoms']):
            category = cat
            break

    variables = COPY_VARIABLES.get(category, DEFAULT_COPY_VARS)

    copies = []
    template_keys = list(COPY_TEMPLATES.keys())

    for i, key in enumerate(template_keys[:count]):
        tmpl_info = COPY_TEMPLATES[key]
        template = random.choice(tmpl_info['templates'])
        copy_text = _fill_template(template, variables, symptom)

        copies.append({
            'id': i + 1,
            'type': key,
            'label': tmpl_info['label'],
            'brain_target': tmpl_info['brain'],
            'principle': tmpl_info['principle'],
            'copy': copy_text,
            'usage': _get_usage_suggestion(key),
        })

    return copies


def _get_usage_suggestion(copy_type: str) -> str:
    """コピータイプ別の使用場面を提案"""
    suggestions = {
        'loss_aversion': 'Instagram/Facebook広告のヘッドライン、LPのファーストビュー',
        'specific_number': 'LP内の実績セクション、Google広告、チラシ',
        'curiosity_hook': 'ブログ記事タイトル、SNS投稿、YouTube動画タイトル',
        'social_proof': 'LP内の口コミセクション、ポータルサイトのプロフィール',
        'sensory': 'LP のファーストビュー、体験レポート、SNS投稿',
        'return_to_self': 'LP のファーストビュー、女性向け広告、Instagram投稿',
        'specialist': 'Google広告、MEO対策、看板、名刺',
        'two_choices': 'Facebook広告、LP のファーストビュー、チラシ',
        'negative_hook': 'YouTube動画タイトル、ブログ記事、SNS広告',
        'empathy_story': 'LP のストーリーセクション、プロフィールページ、SNS投稿',
    }
    return suggestions.get(copy_type, 'LP、広告、SNS投稿')
