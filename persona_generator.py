"""
ペルソナ自動生成モジュール（ルールベース）

Obsidian知識ベース:
- 「水を1万円で売る」原則: 相手の緊急度・必要性で価値が変わる
- ターゲット選定の3条件: 重い悩み、緊急性、深いコンプレックス
- 市場規模が大きいほど同じ努力で多く売れる
- 脳に刷り込まれた単語に人は反応する

5人のペルソナを生成:
1. 最も深い悩みを持つ理想顧客（メインターゲット）
2. 緊急性が高い顧客
3. コンプレックスが深い顧客
4. 長期間悩んでいる顧客
5. 周囲に相談できない顧客
"""

import random
from typing import List, Dict, Optional


# ============================================================
# ペルソナ属性テンプレート
# ============================================================

# 悩みカテゴリ別の典型的な顧客属性
PERSONA_TEMPLATES = {
    'pain': {
        'age_ranges': [
            {'range': '30代後半', 'weight': 3},
            {'range': '40代', 'weight': 5},
            {'range': '50代', 'weight': 4},
            {'range': '60代', 'weight': 2},
        ],
        'genders': [
            {'gender': '女性', 'weight': 6},
            {'gender': '男性', 'weight': 4},
        ],
        'occupations': [
            'デスクワーク（事務職・IT系）',
            '立ち仕事（販売・接客）',
            '主婦・パート',
            '介護職',
            '看護師',
            '保育士',
            '配送業',
            '自営業',
        ],
        'family': [
            '夫・子供2人（小学生）',
            '独身・一人暮らし',
            '夫・高校生の子供1人',
            '夫婦二人暮らし',
            '親と同居（介護中）',
        ],
        'daily_patterns': [
            '朝起きた瞬間から痛みがある',
            '仕事中に悪化し、集中できない',
            '家事をするたびに痛みが走る',
            '子供を抱っこするのが辛い',
            '長時間座っていると動けなくなる',
        ],
        'tried_solutions': [
            '整形外科で湿布と痛み止めをもらったが改善しない',
            'マッサージに週1で通っているが一時的',
            'YouTubeのストレッチを試したが続かない',
            '接骨院に通ったが保険内では限界を感じている',
            '市販のコルセットやサポーターを使っている',
        ],
    },
    'posture': {
        'age_ranges': [
            {'range': '20代後半', 'weight': 3},
            {'range': '30代', 'weight': 5},
            {'range': '40代', 'weight': 4},
            {'range': '50代', 'weight': 2},
        ],
        'genders': [
            {'gender': '女性', 'weight': 7},
            {'gender': '男性', 'weight': 3},
        ],
        'occupations': [
            'デスクワーク（事務職・IT系）',
            '主婦',
            '営業職',
            '受付・事務',
            '在宅ワーカー',
        ],
        'family': [
            '独身・一人暮らし',
            '夫・子供1人（未就学児）',
            '夫婦二人暮らし',
            '実家暮らし',
        ],
        'daily_patterns': [
            '写真に写った自分の姿勢にショックを受けた',
            '鏡で見る自分の後ろ姿が気になる',
            '洋服が似合わなくなった気がする',
            'パートナーに姿勢を指摘された',
            '長時間デスクワークで体が固まる',
        ],
        'tried_solutions': [
            '姿勢矯正ベルトを買ったが続かない',
            'ヨガ教室に通ったが改善しない',
            'ストレッチポールを購入したが使い方がわからない',
            '整体に数回行ったが元に戻る',
        ],
    },
    'beauty': {
        'age_ranges': [
            {'range': '20代後半', 'weight': 3},
            {'range': '30代', 'weight': 5},
            {'range': '40代', 'weight': 5},
            {'range': '50代', 'weight': 3},
        ],
        'genders': [
            {'gender': '女性', 'weight': 9},
            {'gender': '男性', 'weight': 1},
        ],
        'occupations': [
            '会社員（事務・営業）',
            '主婦',
            '接客業',
            '美容関連',
            'パート・アルバイト',
        ],
        'family': [
            '独身・一人暮らし',
            '夫・子供あり',
            '夫婦二人暮らし',
            'シングルマザー',
        ],
        'daily_patterns': [
            '鏡を見るたびにため息が出る',
            'メイクでカバーしきれなくなった',
            '同年代の友人と比べて老けて見える',
            '人と会う予定があると憂鬱になる',
            'SNSに自分の写真を載せたくない',
        ],
        'tried_solutions': [
            '高額な化粧品を試したが効果を感じない',
            'エステに数回通ったが継続できない',
            '美顔器を購入したが効果がわからない',
            'サプリメントを飲んでいるが変化なし',
        ],
    },
    'mental': {
        'age_ranges': [
            {'range': '20代後半', 'weight': 2},
            {'range': '30代', 'weight': 4},
            {'range': '40代', 'weight': 5},
            {'range': '50代', 'weight': 4},
        ],
        'genders': [
            {'gender': '女性', 'weight': 7},
            {'gender': '男性', 'weight': 3},
        ],
        'occupations': [
            '会社員（ストレス高）',
            '主婦（ワンオペ育児）',
            '管理職',
            '看護師・介護職',
            '教師',
            '自営業',
        ],
        'family': [
            '夫・子供あり（家事育児の負担大）',
            '独身・一人暮らし',
            '夫婦二人暮らし',
            '親の介護中',
        ],
        'daily_patterns': [
            '朝起きた瞬間から体がだるい',
            '夜中に何度も目が覚める',
            '理由もなく涙が出ることがある',
            '休日も体が休まらない',
            '人と会うのが億劫になった',
        ],
        'tried_solutions': [
            '心療内科で薬をもらっているが根本解決しない',
            'ヨガや瞑想を試したが続かない',
            'アロマやサプリを試した',
            '休職を考えているが経済的に不安',
        ],
    },
    'women': {
        'age_ranges': [
            {'range': '20代後半', 'weight': 2},
            {'range': '30代', 'weight': 6},
            {'range': '40代', 'weight': 4},
        ],
        'genders': [
            {'gender': '女性', 'weight': 10},
        ],
        'occupations': [
            '産休・育休中',
            '主婦（専業）',
            '主婦（パート復帰予定）',
            '時短勤務中',
            '在宅ワーカー',
        ],
        'family': [
            '夫・0歳児',
            '夫・1〜2歳児',
            '夫・子供2人（幼児）',
            'シングルマザー・子供1人',
        ],
        'daily_patterns': [
            '授乳や抱っこで体がボロボロ',
            '自分の時間がまったく取れない',
            '産前の体型に戻れず落ち込む',
            '夫が育児に非協力的でストレス',
            '外出するのが億劫になった',
        ],
        'tried_solutions': [
            '骨盤ベルトを使っているが効果不明',
            '産後ヨガに行きたいが子供を預けられない',
            '実家が遠く頼れる人がいない',
            '自治体の産後ケアは予約が取れない',
        ],
    },
    'sports': {
        'age_ranges': [
            {'range': '10代後半', 'weight': 3},
            {'range': '20代', 'weight': 4},
            {'range': '30代', 'weight': 4},
            {'range': '40代', 'weight': 3},
        ],
        'genders': [
            {'gender': '女性', 'weight': 4},
            {'gender': '男性', 'weight': 6},
        ],
        'occupations': [
            '学生（部活動）',
            '会社員（趣味でスポーツ）',
            '元アスリート',
            'スポーツインストラクター',
            '週末ランナー',
        ],
        'family': [
            '独身',
            '夫婦二人暮らし',
            '実家暮らし（学生）',
        ],
        'daily_patterns': [
            '練習や試合のたびに痛みが再発する',
            '以前のようなパフォーマンスが出ない',
            '怪我が怖くて全力が出せない',
            '大会や試合が近いのに治らない焦り',
        ],
        'tried_solutions': [
            '整形外科でリハビリしたが完治しない',
            'テーピングで誤魔化しながら続けている',
            'トレーナーに相談したがストレッチしか教わらない',
        ],
    },
}

# デフォルト（カテゴリ不明時）
DEFAULT_TEMPLATE = PERSONA_TEMPLATES['pain']

# ペルソナの「心の声」テンプレート（5タイプ）
PERSONA_TYPES = [
    {
        'type': 'ideal',
        'label': '理想顧客（メインターゲット）',
        'description': '最も深い悩みを持ち、解決に投資する意思がある',
        'voice_templates': [
            'もう何年も{symptom}に悩んでいて、本当に辛い。{tried}けど全然改善しない。お金がかかってもいいから、根本的に解決してくれるところを探している。',
            '{symptom}のせいで{impact}。正直、もう限界。ちゃんと原因を見つけて、計画的に治してくれる専門家に出会いたい。',
        ],
    },
    {
        'type': 'urgent',
        'label': '緊急性が高い顧客',
        'description': '今すぐ解決しなければならない状況にいる',
        'voice_templates': [
            '来週{event}なのに、この{symptom}がどうにもならない。今すぐなんとかしてほしい。費用は二の次。',
            '{symptom}が急に悪化して、{impact}。このままだと{consequence}になってしまう。すぐに診てもらえるところを探している。',
        ],
    },
    {
        'type': 'complex',
        'label': 'コンプレックスが深い顧客',
        'description': '見た目や体の悩みで自信を失っている',
        'voice_templates': [
            '{symptom}のことが気になって、{social_impact}。誰にも相談できないし、{avoidance}ようになってしまった。',
            '周りの人は気にしすぎだと言うけど、自分にとっては深刻。{symptom}さえなければ、もっと{desire}のに。',
        ],
    },
    {
        'type': 'chronic',
        'label': '長期間悩んでいる顧客',
        'description': '何年も同じ悩みを抱え、諦めかけている',
        'voice_templates': [
            'もう{years}年以上{symptom}に悩んでいる。{tried}けど、どれも一時的。正直、もう治らないんじゃないかと諦めかけている。',
            '色々試した結果、{amount}万円以上使ったけど改善しない。最後にもう一度だけ、信頼できるところで見てもらいたい。',
        ],
    },
    {
        'type': 'isolated',
        'label': '周囲に相談できない顧客',
        'description': '悩みを打ち明けられず一人で抱えている',
        'voice_templates': [
            '{symptom}のことは家族にも言えない。{reason_secret}から。一人で調べてはため息をついている毎日。プロに相談したい。',
            '友達に話しても「大したことないよ」と言われる。でも自分にとっては{impact}。わかってくれる専門家に出会いたい。',
        ],
    },
]

# 悩み別のテンプレート変数
SYMPTOM_VARIABLES = {
    'pain': {
        'symptoms': ['腰痛', '肩こり', '頭痛', '膝の痛み', '首の痛み', '坐骨神経痛'],
        'impacts': ['仕事に集中できない', '子供と遊べない', '夜眠れない', '日常生活がままならない', '趣味を楽しめない'],
        'events': ['旅行', '子供の運動会', '大事なプレゼン', '結婚式', '引っ越し'],
        'consequences': ['仕事を辞めなければならない', '手術が必要', '歩けなくなる'],
        'social_impacts': ['周囲に迷惑をかけている気がする', '「また休むの？」と言われるのが怖い'],
        'avoidances': ['外出を避ける', '人に会うのを避ける', 'スポーツを諦めた'],
        'desires': ['自由に動ける', '旅行に行ける', '子供と全力で遊べる'],
        'years_range': [3, 5, 7, 10, 15],
        'amount_range': [10, 20, 30, 50],
        'tried': ['整形外科にも行った', 'マッサージにも通った', 'いろんなサプリも試した'],
        'reason_secrets': ['弱音を吐くのが恥ずかしい', '心配をかけたくない', '「年のせいだよ」と言われるのが嫌'],
    },
    'posture': {
        'symptoms': ['猫背', 'O脚', '骨盤の歪み', '反り腰', '巻き肩', 'ストレートネック'],
        'impacts': ['写真を撮られるのが嫌', '洋服が似合わない', '老けて見られる', '自分に自信が持てない'],
        'events': ['同窓会', '結婚式', 'デート', '面接'],
        'consequences': ['年齢より10歳老けて見える', '体の不調がどんどん悪化する'],
        'social_impacts': ['人前に出るのが恥ずかしい', '写真に写りたくない'],
        'avoidances': ['全身が映る鏡を見ない', '体のラインが出る服を着ない'],
        'desires': ['自信を持って歩ける', '好きな服を着られる', '堂々と写真に写れる'],
        'years_range': [3, 5, 10],
        'amount_range': [5, 10, 20],
        'tried': ['矯正ベルトも試した', 'ヨガにも通った', 'ストレッチも頑張った'],
        'reason_secrets': ['見た目のことで悩んでいると思われたくない', 'コンプレックスだと認めたくない'],
    },
    'beauty': {
        'symptoms': ['たるみ', 'ほうれい線', 'シワ', '肌荒れ', 'むくみ', 'エラ張り', '顔の歪み'],
        'impacts': ['鏡を見るのが辛い', '人に会いたくない', '写真に写りたくない', '自分に自信が持てない'],
        'events': ['同窓会', '結婚式', 'デート', '仕事の会議'],
        'consequences': ['もっと老けて見えるようになる', '取り返しがつかなくなる'],
        'social_impacts': ['友達と並ぶと自分だけ老けて見える', '「疲れてる？」と聞かれるのが辛い'],
        'avoidances': ['すっぴんで外出できない', '明るい場所を避ける', '自撮りをしない'],
        'desires': ['自信を持ってすっぴんで過ごせる', '年齢を聞かれて驚かれたい', '堂々と写真に写りたい'],
        'years_range': [2, 3, 5, 7],
        'amount_range': [10, 20, 30, 50],
        'tried': ['高級化粧品も試した', 'エステにも通った', '美顔器も買った'],
        'reason_secrets': ['年齢のことで悩んでいると思われたくない', '美容にお金をかけていると知られたくない'],
    },
    'mental': {
        'symptoms': ['自律神経の乱れ', '不眠', '慢性疲労', 'めまい', '動悸', '原因不明の体調不良'],
        'impacts': ['仕事に行けない日がある', '家事ができない', '笑えなくなった', '生きているのが辛い'],
        'events': ['仕事の締め切り', '子供の行事', '引っ越し', '年度替わり'],
        'consequences': ['仕事を失う', '家庭が崩壊する', '引きこもりになる'],
        'social_impacts': ['「怠けている」と思われている', '理解してもらえない'],
        'avoidances': ['人と会う約束を入れない', '新しいことを始められない'],
        'desires': ['朝スッキリ起きられる', '普通の日常を送れる', '心から笑える'],
        'years_range': [1, 2, 3, 5],
        'amount_range': [5, 10, 20],
        'tried': ['心療内科の薬を飲んでいる', 'サプリやアロマも試した', '休職も考えた'],
        'reason_secrets': ['メンタルの問題だと思われたくない', '弱い人間だと思われたくない'],
    },
    'women': {
        'symptoms': ['産後の骨盤の歪み', '産後太り', '尿漏れ', '恥骨痛', '腰痛（産後）'],
        'impacts': ['産前の体型に戻れない', '自分の体に自信が持てない', '体が辛くて育児がしんどい'],
        'events': ['仕事復帰', '幼稚園の行事', 'ママ友との集まり'],
        'consequences': ['体型が戻らないまま定着してしまう', '慢性的な不調になる'],
        'social_impacts': ['ママ友と比べてしまう', '夫に女性として見てもらえない気がする'],
        'avoidances': ['水着になれない', '産前の服が着られない'],
        'desires': ['産前の体型に戻りたい', '自信を持っておしゃれしたい', '体の不調なく育児を楽しみたい'],
        'years_range': [1, 2, 3],
        'amount_range': [5, 10, 15],
        'tried': ['骨盤ベルトをした', '産後ヨガに行きたいが時間がない', 'ダイエットしたがリバウンド'],
        'reason_secrets': ['産後の体のことを人に言いづらい', '「母親なんだからしっかり」と思われそう'],
    },
    'sports': {
        'symptoms': ['膝の痛み', '足首の不安定さ', '肩の痛み', '腰の痛み', '肉離れの後遺症'],
        'impacts': ['全力でプレーできない', '練習を休まなければならない', '大会に出られない'],
        'events': ['大会', '試合', 'マラソン', 'シーズン開幕'],
        'consequences': ['選手生命が終わる', 'レギュラーを外される', '趣味を諦めなければならない'],
        'social_impacts': ['チームメイトに迷惑をかけている', '「もう無理じゃない？」と言われる'],
        'avoidances': ['激しい動きを避けている', '試合に出るのが怖い'],
        'desires': ['全力でプレーしたい', '以前のパフォーマンスに戻りたい', '怪我を気にせず動きたい'],
        'years_range': [1, 2, 3],
        'amount_range': [5, 10, 20],
        'tried': ['整形外科でリハビリした', 'テーピングで誤魔化している', 'トレーナーに相談した'],
        'reason_secrets': ['弱い選手だと思われたくない', '怪我を理由に逃げていると思われたくない'],
    },
}

DEFAULT_VARIABLES = SYMPTOM_VARIABLES['pain']

# 名前リスト
FEMALE_NAMES = [
    '田中 美咲', '鈴木 綾香', '山田 真由美', '佐藤 恵子', '渡辺 裕子',
    '高橋 千尋', '伊藤 麻衣', '中村 由紀', '小林 智子', '加藤 美穂',
    '松本 さやか', '井上 洋子', '木村 理沙', '林 久美子', '清水 幸恵',
]
MALE_NAMES = [
    '田中 健太', '鈴木 大輔', '山田 雄一', '佐藤 和也', '渡辺 拓也',
    '高橋 誠', '伊藤 浩二', '中村 直樹', '小林 俊介', '加藤 隆',
]


def _select_weighted(items):
    """重み付き選択"""
    total = sum(item['weight'] for item in items)
    r = random.uniform(0, total)
    current = 0
    for item in items:
        current += item['weight']
        if r <= current:
            return item
    return items[-1]


def _detect_category_for_persona(keyword: str, search_results: Optional[List[Dict]] = None) -> str:
    """キーワードからカテゴリを判定"""
    keyword_lower = keyword.strip()

    category_keywords = {
        'pain': ['痛', '腰', '肩', '首', '膝', 'ヘルニア', '神経痛', '頭痛', 'しびれ', '痺れ'],
        'posture': ['猫背', 'O脚', 'X脚', '骨盤', '姿勢', '歪み', '反り腰', '巻き肩'],
        'beauty': ['小顔', 'エラ', 'たるみ', 'シワ', 'ニキビ', '肌', 'むくみ', '痩', 'ダイエット', '美容'],
        'mental': ['自律神経', '不眠', '眠れ', 'ストレス', 'うつ', '疲労', 'めまい', '動悸'],
        'women': ['産後', '骨盤矯正', '妊娠', '生理', '更年期', '尿漏れ'],
        'sports': ['スポーツ', '怪我', '捻挫', '肉離れ', 'リハビリ', '選手'],
    }

    best_cat = 'pain'
    best_score = 0
    for cat, words in category_keywords.items():
        score = sum(len(w) for w in words if w in keyword_lower)
        if score > best_score:
            best_score = score
            best_cat = cat

    return best_cat


def generate_personas(
    keyword: str,
    target_symptom: str = '',
    search_results: Optional[List[Dict]] = None,
    count: int = 5,
) -> List[Dict]:
    """
    ペルソナを自動生成する

    Args:
        keyword: 検索キーワード（例: 腰痛）
        target_symptom: ターゲットの症状（指定がなければキーワードを使用）
        search_results: 検索結果（あれば悩みの声を参考にする）
        count: 生成するペルソナ数

    Returns:
        ペルソナ情報のリスト
    """
    category = _detect_category_for_persona(keyword)
    template = PERSONA_TEMPLATES.get(category, DEFAULT_TEMPLATE)
    variables = SYMPTOM_VARIABLES.get(category, DEFAULT_VARIABLES)

    symptom = target_symptom if target_symptom else keyword

    # 検索結果から実際の悩みの声を取得
    real_voices = []
    if search_results:
        for r in search_results[:20]:
            text = r.get('full_text', '') or r.get('title', '')
            if len(text) > 30:
                real_voices.append(text[:200])

    personas = []
    used_names = set()

    for i, persona_type in enumerate(PERSONA_TYPES[:count]):
        # 性別選択
        gender_item = _select_weighted(template['genders'])
        gender = gender_item['gender']

        # 名前選択（重複なし）
        name_pool = FEMALE_NAMES if gender == '女性' else MALE_NAMES
        available = [n for n in name_pool if n not in used_names]
        if not available:
            available = name_pool
        name = random.choice(available)
        used_names.add(name)

        # 年齢選択
        age_item = _select_weighted(template['age_ranges'])
        age = age_item['range']

        # 職業選択
        occupation = random.choice(template['occupations'])

        # 家族構成
        family = random.choice(template['family'])

        # テンプレート変数の選択
        impact = random.choice(variables['impacts'])
        event = random.choice(variables['events'])
        consequence = random.choice(variables['consequences'])
        social_impact = random.choice(variables['social_impacts'])
        avoidance = random.choice(variables['avoidances'])
        desire = random.choice(variables['desires'])
        years = random.choice(variables['years_range'])
        amount = random.choice(variables['amount_range'])
        tried = random.choice(variables['tried'])
        reason_secret = random.choice(variables['reason_secrets'])
        daily = random.choice(template['daily_patterns'])
        tried_solution = random.choice(template['tried_solutions'])

        # 心の声を生成
        voice_template = random.choice(persona_type['voice_templates'])
        voice = voice_template.format(
            symptom=symptom,
            impact=impact,
            event=event,
            consequence=consequence,
            social_impact=social_impact,
            avoidance=avoidance,
            desire=desire,
            years=years,
            amount=amount,
            tried=tried,
            reason_secret=reason_secret,
        )

        # 実際の検索結果からの声があれば追加
        real_voice = ''
        if real_voices and i < len(real_voices):
            real_voice = real_voices[i]

        persona = {
            'id': i + 1,
            'type': persona_type['type'],
            'type_label': persona_type['label'],
            'type_description': persona_type['description'],
            'name': name,
            'age': age,
            'gender': gender,
            'occupation': occupation,
            'family': family,
            'symptom': symptom,
            'daily_pattern': daily,
            'tried_solution': tried_solution,
            'inner_voice': voice,
            'real_voice': real_voice,
            'desire': desire,
            'pain_level': min(5, max(3, 5 - i)),  # 1番目が最も深い
        }

        personas.append(persona)

    return personas
