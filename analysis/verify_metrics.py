#!/usr/bin/env python3
"""模拟数据 / 独立项目：标准库核验 + SQLite 分析，原始数据只读。"""
import argparse
import csv
import hashlib
import json
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = '模拟数据 / 独立项目'
FIELDS = ['user_id', 'event_date', 'event_type', 'user_type']
EVENTS = {'register', 'start_learning', 'open_app', 'complete_task', 'churn_flag', 'reactivate'}
LEARNING = {'start_learning', 'complete_task'}
ACTIVE = LEARNING | {'open_app'}


def inspect_source(source):
    with source.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != FIELDS:
            raise ValueError(f'CSV 字段不符：{reader.fieldnames}')
        rows = list(reader)
    if not rows:
        raise ValueError('CSV 为空')
    issues = defaultdict(list)
    users = defaultdict(list)
    seen = set()
    for line, row in enumerate(rows, 2):
        if set(row) != set(FIELDS) or any(not row[k] or not row[k].strip() for k in FIELDS):
            raise ValueError(f'第 {line} 行缺失字段或列数异常')
        parsed = date.fromisoformat(row['event_date'])
        if parsed.isoformat() != row['event_date']:
            raise ValueError(f'第 {line} 行日期不是 YYYY-MM-DD')
        if row['event_type'] not in EVENTS:
            raise ValueError(f'第 {line} 行未知事件：{row["event_type"]}')
        key = tuple(row[k] for k in FIELDS)
        if key in seen:
            issues['duplicate_rows'].append(line)
        seen.add(key)
        users[row['user_id']].append(row)
    end_date = max(date.fromisoformat(r['event_date']) for r in rows)
    records = []
    diagnostics = {
        'd7_without_d1': [], 'd1_without_activation': [],
        'complete_without_same_day_start': [], 'post_d0_learning_without_same_day_open': [],
        'reactivate_without_prior_churn': [], 'activity_after_churn_without_reactivate': [],
        'activity_between_churn_and_reactivate': [], 'insufficient_d7_window': [],
    }
    for uid, events in sorted(users.items()):
        registrations = [e for e in events if e['event_type'] == 'register']
        if len(registrations) != 1:
            raise ValueError(f'{uid} 注册记录数为 {len(registrations)}，需人工确定注册口径')
        if len({e['user_type'] for e in events}) != 1:
            raise ValueError(f'{uid} 用户类型不一致')
        reg = date.fromisoformat(registrations[0]['event_date'])
        days = defaultdict(set)
        for e in events:
            day_no = (date.fromisoformat(e['event_date']) - reg).days
            if day_no < 0:
                raise ValueError(f'{uid} 存在注册前事件')
            days[day_no].add(e['event_type'])
        churn_days = sorted(d for d, es in days.items() if 'churn_flag' in es)
        react_days = sorted(d for d, es in days.items() if 'reactivate' in es)
        d1, d7 = int('open_app' in days[1]), int('open_app' in days[7])
        activated = int('start_learning' in days[0])
        observable = int(reg + timedelta(days=7) <= end_date)
        checks = {
            'd7_without_d1': d7 and not d1,
            'd1_without_activation': d1 and not activated,
            'complete_without_same_day_start': any('complete_task' in es and 'start_learning' not in es for es in days.values()),
            'post_d0_learning_without_same_day_open': any(d > 0 and es & LEARNING and 'open_app' not in es for d, es in days.items()),
            'reactivate_without_prior_churn': bool(react_days) and (not churn_days or react_days[0] <= churn_days[0]),
            'activity_after_churn_without_reactivate': bool(churn_days) and not react_days and any(d > churn_days[0] and es & ACTIVE for d, es in days.items()),
            'activity_between_churn_and_reactivate': bool(churn_days and react_days) and any(churn_days[0] < d < react_days[0] and es & ACTIVE for d, es in days.items()),
            'insufficient_d7_window': not observable,
        }
        for key, found in checks.items():
            if found:
                diagnostics[key].append(uid)
        records.append({
            'user_id': uid, 'user_type': events[0]['user_type'], 'reg_date': reg.isoformat(),
            'activated': activated, 'd1': d1, 'd7': d7,
            'day0_complete': int('complete_task' in days[0]),
            'learning_days_d0_d6': sum(bool(days[d] & LEARNING) for d in range(7)),
            'churn': int(bool(churn_days)), 'reactivated': int(bool(react_days)),
            'first_churn_date': (reg + timedelta(days=churn_days[0])).isoformat() if churn_days else None,
            'first_reactivate_date': (reg + timedelta(days=react_days[0])).isoformat() if react_days else None,
            'd7_observable': observable,
        })
    audit = {
        'data_status': STATUS, 'source_file': source.name,
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'event_rows': len(rows), 'users': len(users),
        'date_min': min(r['event_date'] for r in rows), 'date_max': end_date.isoformat(),
        'registration_date_min': min(r['reg_date'] for r in records),
        'registration_date_max': max(r['reg_date'] for r in records),
        'missing_fields': 0, 'invalid_dates': 0, 'unknown_events': 0,
        'duplicate_row_count': len(issues['duplicate_rows']), 'duplicate_csv_lines': issues['duplicate_rows'],
        'event_distribution': dict(sorted(Counter(r['event_type'] for r in rows).items())),
        'diagnostics': {k: {'user_count': len(v), 'user_ids': v} for k, v in diagnostics.items()},
    }
    user_days = defaultdict(set)
    for row in rows:
        user_days[(row['user_id'], row['event_date'])].add(row['event_type'])
    audit['complete_without_same_day_start_user_days'] = sum(
        'complete_task' in es and 'start_learning' not in es for es in user_days.values())
    audit['post_d0_learning_without_same_day_open_user_days'] = sum(
        bool(es & LEARNING) and 'open_app' not in es and 'register' not in es for es in user_days.values())
    audit['learning_without_open_on_reactivation_user_days'] = sum(
        bool(es & LEARNING) and 'open_app' not in es and 'reactivate' in es for es in user_days.values())
    # 当前分析不静默清洗，也不以未成熟队列作全体留存分母。
    if audit['duplicate_row_count'] or diagnostics['insufficient_d7_window']:
        raise ValueError('发现重复行或 D7 观察窗不足，请先明确处理口径；未生成新报告')
    return rows, records, audit


def run_sql(rows, python_records):
    sql_path = ROOT / 'sql/funnel_analysis.sql'
    parts = re.split(r'^-- report: ([a-z0-9_]+)\s*$', sql_path.read_text(encoding='utf-8'), flags=re.M)
    with sqlite3.connect(':memory:') as db:
        db.row_factory = sqlite3.Row
        db.execute('CREATE TABLE user_events (user_id TEXT, event_date TEXT, event_type TEXT, user_type TEXT)')
        db.executemany('INSERT INTO user_events VALUES (?, ?, ?, ?)', [tuple(r[k] for k in FIELDS) for r in rows])
        db.executescript(parts[0])
        sql_records = [dict(r) for r in db.execute('SELECT * FROM portfolio_user_metrics ORDER BY user_id')]
        if sql_records != python_records:
            raise AssertionError('Python 与 SQLite 逐用户计算结果不一致')
        reports = {parts[i]: [dict(r) for r in db.execute(parts[i + 1])] for i in range(1, len(parts), 2)}
    n = len(python_records)
    if sum(r['registered_users'] for r in reports['segment_metrics']) != n:
        raise AssertionError('分群人数不等于注册人数')
    for name in ['learning_activity', 'churn_reactivation']:
        if sum(r['users'] for r in reports[name]) != n:
            raise AssertionError(f'{name} 人数不守恒')
    return reports, hashlib.sha256(sql_path.read_bytes()).hexdigest()


def table(rows):
    if not rows:
        return '无记录。'
    keys = [k for k in rows[0] if k != 'data_status']
    return '\n'.join([
        '| ' + ' | '.join(keys) + ' |',
        '| ' + ' | '.join(['---'] * len(keys)) + ' |',
        *['| ' + ' | '.join(str(row[k]) for k in keys) + ' |' for row in rows],
    ])


def write_reports(output, reports, records, audit):
    output.mkdir(parents=True, exist_ok=True)
    payload = {'data_status': STATUS, 'audit': audit, 'reports': reports}
    (output / 'metrics.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for name, rows in {**reports, 'user_metrics': [{'data_status': STATUS, **r} for r in records]}.items():
        with (output / f'{name}.csv').open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    headings = {'core_metrics': '核心指标', 'segment_metrics': '按用户类型分群', 'day0_completion': '首日任务完成与 D7', 'learning_activity': 'D0–D6 学习活跃天数与 D7', 'churn_reactivation': '流失标记与召回', 'registration_cohorts': '注册日期队列', 'event_distribution': '事件记录分布'}
    text = ['# 数据核验报告', '', f'**{STATUS}。全部结果仅用于方法演示，不代表真实平台表现。**', '',
            '本报告由 `analysis/verify_metrics.py` 自动生成。原始 CSV 只读；SQLite 使用内存数据库。', '',
            f'- 行为记录：{audit["event_rows"]}；用户：{audit["users"]}。',
            f'- 事件日期：{audit["date_min"]} 至 {audit["date_max"]}。',
            f'- 注册日期：{audit["registration_date_min"]} 至 {audit["registration_date_max"]}。',
            f'- 原始 CSV SHA-256：`{audit["source_sha256"]}`。',
            '- Python 与 SQL 的逐用户标记、活跃天数及日期已独立计算并完全一致。',
            '- 字段完整性、合法日期、事件枚举、单次注册、用户类型稳定性、注册前事件检查通过。',
            '- 未发现完全重复行；按文件截止日期，全部注册用户具备 D7 观察窗。', '',
            '## 口径与限制', '',
            '- 激活：注册当天发生 start_learning；不代表完成任务。',
            '- D1 / D7：注册后恰好第 1 / 7 个自然日发生 open_app；分母均为注册用户。',
            '- 严格漏斗末级：同时满足激活、D1、D7；不要将全体 D7 人数直接除以 D1 人数称作阶段转化。',
            '- 学习活跃度：D0–D6 发生 start_learning 或 complete_task 的不同日期数；不包含 D7。分组为 0、1–2、3–7 天。',
            '- day0_completion 同时列出全体注册用户和仅激活用户两种比较，未控制用户类型等混杂因素。',
            '- 召回率：有流失标记且之后出现 reactivate 的用户 / 有流失标记用户。不是运营干预的因果效果。',
            '- 同一天无时间戳，不能恢复事件先后；全局截止日期不能保证逐用户日志采集完整。',
            '- 研究资料的 5 类痛点与上下文 6 类痛点采用不同聚类粒度，原始文件不变。', '']
    for name, rows in reports.items():
        text += [f'## {headings[name]}（模拟数据）', '', table(rows), '']
    labels = {
        'd7_without_d1': 'D7 打开但 D1 未打开（留存集合不完全嵌套）',
        'd1_without_activation': 'D1 打开但注册日未开始学习',
        'complete_without_same_day_start': '至少一天有完成任务但无当天开始学习事件',
        'post_d0_learning_without_same_day_open': '注册后至少一天有学习事件但无当天打开事件',
        'reactivate_without_prior_churn': '召回前无更早日期的流失标记',
        'activity_after_churn_without_reactivate': '有流失标记无召回标记，但之后有活跃事件',
        'activity_between_churn_and_reactivate': '流失与召回日期之间出现活跃事件',
        'insufficient_d7_window': '按文件截止日判断 D7 观察窗不足',
    }
    text += ['## 数据诊断（模拟数据）', '', '| 检查 | 用户数 | 样例 ID（最多 5 个） |', '| --- | ---: | --- |']
    for key, value in audit['diagnostics'].items():
        text.append(f'| {labels[key]} | {value["user_count"]} | {", ".join(value["user_ids"][:5]) or "—"} |')
    text += ['', '诊断按用户去重；完整用户 ID 见 metrics.json。事件缺口为日志语义限制，未据此删除用户、补造事件或修改原始 CSV。', '']
    text += [f'完成任务但无当天开始学习：{audit["complete_without_same_day_start_user_days"]} 个用户日；注册后学习但无当天打开：{audit["post_d0_learning_without_same_day_open_user_days"]} 个用户日，其中 {audit["learning_without_open_on_reactivation_user_days"]} 个用户日同时有 reactivate。', '']
    (output / 'verification_report.md').write_text('\n'.join(text), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'english_app_user_events_1000.csv')
    parser.add_argument('--output', type=Path, default=ROOT / 'analysis/results')
    args = parser.parse_args()
    rows, records, audit = inspect_source(args.input)
    reports, sql_hash = run_sql(rows, records)
    audit['sql_sha256'] = sql_hash
    audit['python_sql_user_level_match'] = True
    write_reports(args.output, reports, records, audit)
    print(json.dumps({'data_status': STATUS, 'rows': len(rows), 'core_metrics': reports['core_metrics'][0], 'output': str(args.output.resolve())}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
