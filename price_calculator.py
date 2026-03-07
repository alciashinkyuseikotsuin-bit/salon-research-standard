"""
目標金額→価格逆算モジュール

Obsidian知識ベース:
- 売上 = 新規数 x 客単価 x リピート回数
- 2万円の商品を20万円にするだけで集客数が10分の1になる
- 月商目標 → 必要な客数・単価を逆算
- 稼働日数・予約枠数から現実的な計算

入力:
- 月の目標売上
- 理想の稼働日数（月）
- 1日の予約枠数
- 竹コースの価格（月額換算 or 一括）
- 竹コースの期間（月数）

出力:
- 必要な新規顧客数/月
- 必要なリピート率
- 現実的な達成シナリオ
"""

from typing import Dict
import math


def calculate_pricing(
    monthly_target: int,
    working_days: int = 22,
    slots_per_day: int = 6,
    bamboo_price: int = 180000,
    bamboo_months: int = 3,
    plum_price: int = 27000,
    plum_to_bamboo_rate: float = 0.5,
) -> Dict:
    """
    目標売上から逆算して必要な数値を計算する

    Args:
        monthly_target: 月の目標売上（円）
        working_days: 月の稼働日数
        slots_per_day: 1日の予約枠数
        bamboo_price: 竹コースの価格（一括）
        bamboo_months: 竹コースの期間（月数）
        plum_price: 梅コースの価格
        plum_to_bamboo_rate: 梅→竹への成約率

    Returns:
        価格計算結果
    """
    # === 基本計算 ===
    total_monthly_slots = working_days * slots_per_day  # 月の総予約枠
    bamboo_monthly = bamboo_price / bamboo_months  # 竹の月額換算

    # === シナリオ1: 竹コースのみで達成 ===
    new_bamboo_per_month = math.ceil(monthly_target / bamboo_monthly)
    # ただし竹は一括なので、初月に必要な新規数
    new_bamboo_needed = math.ceil(monthly_target / bamboo_price)

    # === シナリオ2: 梅→竹の導線で達成 ===
    # 梅を入口にして、竹への成約を狙う
    plum_needed_for_one_bamboo = math.ceil(1 / plum_to_bamboo_rate)
    total_plum_needed = new_bamboo_needed * plum_needed_for_one_bamboo
    plum_revenue = total_plum_needed * plum_price
    bamboo_revenue_from_plum = math.floor(total_plum_needed * plum_to_bamboo_rate) * bamboo_price
    scenario2_revenue = plum_revenue + bamboo_revenue_from_plum

    # === シナリオ3: 現実的なミックス ===
    # 既存の竹コース継続者 + 新規梅 + 新規竹
    # 3ヶ月目以降は既存の竹継続者がいる前提
    existing_bamboo_slots_per_day = 0  # 初月は0
    available_for_new = total_monthly_slots

    # 1日あたり何人の新規が必要か
    daily_new_needed = math.ceil(new_bamboo_needed / working_days * bamboo_months)

    # === 稼働率計算 ===
    # 竹コースは月4回来院
    bamboo_visits_per_month = 4
    # 竹コース1人あたりの月の枠消費
    slots_used_per_bamboo = bamboo_visits_per_month

    # 竹コースで埋められる最大人数
    max_bamboo_clients = total_monthly_slots // slots_used_per_bamboo

    # === 日割り計算 ===
    bamboo_per_session = bamboo_price // (bamboo_months * bamboo_visits_per_month)
    bamboo_per_day = bamboo_price // (bamboo_months * 30)

    # === 年間予測 ===
    annual_target = monthly_target * 12
    # 安定期（4ヶ月目以降）: 既存リピーター + 新規
    stable_month_new_needed = math.ceil(monthly_target * 0.4 / bamboo_price)  # 40%を新規で

    # === 結果をまとめる ===
    result = {
        'input': {
            'monthly_target': monthly_target,
            'monthly_target_display': f'{monthly_target:,}円',
            'working_days': working_days,
            'slots_per_day': slots_per_day,
            'bamboo_price': bamboo_price,
            'bamboo_price_display': f'{bamboo_price:,}円',
            'bamboo_months': bamboo_months,
            'plum_price': plum_price,
            'plum_price_display': f'{plum_price:,}円',
        },

        'basic': {
            'total_monthly_slots': total_monthly_slots,
            'bamboo_monthly_equivalent': int(bamboo_monthly),
            'bamboo_monthly_display': f'{int(bamboo_monthly):,}円/月',
            'bamboo_per_session': bamboo_per_session,
            'bamboo_per_session_display': f'{bamboo_per_session:,}円/回',
            'bamboo_per_day': bamboo_per_day,
            'bamboo_per_day_display': f'{bamboo_per_day:,}円/日',
            'max_bamboo_clients': max_bamboo_clients,
        },

        'scenario_bamboo_only': {
            'title': '竹コースのみで達成する場合',
            'new_clients_needed': new_bamboo_needed,
            'description': f'月に{new_bamboo_needed}人の新規が竹コース({bamboo_price:,}円)を申し込めば達成',
            'difficulty': '高' if new_bamboo_needed > 5 else '中' if new_bamboo_needed > 2 else '低',
            'revenue': new_bamboo_needed * bamboo_price,
        },

        'scenario_with_plum': {
            'title': '梅→竹の導線で達成する場合',
            'plum_clients_needed': total_plum_needed,
            'bamboo_conversions': math.floor(total_plum_needed * plum_to_bamboo_rate),
            'conversion_rate': f'{plum_to_bamboo_rate * 100:.0f}%',
            'plum_revenue': plum_revenue,
            'bamboo_revenue': bamboo_revenue_from_plum,
            'total_revenue': scenario2_revenue,
            'description': f'梅{total_plum_needed}人 → 竹に{math.floor(total_plum_needed * plum_to_bamboo_rate)}人成約で{scenario2_revenue:,}円',
        },

        'stable_phase': {
            'title': '安定期（4ヶ月目以降）の目安',
            'monthly_new_needed': stable_month_new_needed,
            'description': f'リピーターが定着すれば、月{stable_month_new_needed}人の新規で目標達成可能',
            'annual_target': annual_target,
            'annual_target_display': f'{annual_target:,}円/年',
        },

        'action_items': [
            f'1日あたり{slots_per_day}枠のうち、新規は{min(2, slots_per_day)}枠を確保',
            f'梅コース({plum_price:,}円)で毎月{total_plum_needed}人を集客',
            f'梅→竹の成約率{plum_to_bamboo_rate * 100:.0f}%を目指す',
            f'竹コースのリピーター{max_bamboo_clients}人が上限。それ以上は値上げで対応',
        ],

        'pricing_tips': {
            'daily_cost_framing': f'竹コースは1日あたりたった{bamboo_per_day:,}円の投資',
            'session_cost_framing': f'1回あたり{bamboo_per_session:,}円で{bamboo_months}ヶ月の悩みが解決',
            'comparison': f'コンビニコーヒー1杯分({bamboo_per_day:,}円)で人生が変わるとしたら？',
            'roi_message': f'{bamboo_price:,}円の投資で、何年も続いた悩みから解放されます',
        },
    }

    return result
