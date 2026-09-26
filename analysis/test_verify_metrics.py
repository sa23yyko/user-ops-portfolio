"""模拟数据 / 独立项目：核验关键指标口径和输入保护。"""
import csv
import tempfile
import unittest
from pathlib import Path

from verify_metrics import FIELDS, inspect_source, run_sql


class MetricContractTests(unittest.TestCase):
    def inspect(self, rows):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'synthetic_fixture.csv'
            with path.open('w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(FIELDS)
                writer.writerows(rows)
            return inspect_source(path)

    def fixture(self):
        # A 在 D7 回来但 D1 没回来，B 在 D1、D7 均回来。
        return [
            ('A', '2026-08-01', 'register', '测试组'),
            ('A', '2026-08-01', 'start_learning', '测试组'),
            ('A', '2026-08-01', 'complete_task', '测试组'),
            ('A', '2026-08-08', 'open_app', '测试组'),
            ('A', '2026-08-08', 'start_learning', '测试组'),
            ('B', '2026-08-01', 'register', '测试组'),
            ('B', '2026-08-01', 'start_learning', '测试组'),
            ('B', '2026-08-02', 'open_app', '测试组'),
            ('B', '2026-08-08', 'open_app', '测试组'),
        ]

    def test_non_nested_retention_and_no_d7_activity_leakage(self):
        rows, records, audit = self.inspect(self.fixture())
        reports, _ = run_sql(rows, records)
        core = reports['core_metrics'][0]
        self.assertEqual((core['d7_users'], core['strict_funnel_d7_users']), (2, 1))
        self.assertEqual(core['d7_among_d1_rate_pct'], 100.0)
        self.assertEqual(records[0]['learning_days_d0_d6'], 1)
        self.assertEqual(audit['diagnostics']['d7_without_d1']['user_ids'], ['A'])

    def test_duplicate_rows_are_rejected(self):
        rows = self.fixture()
        with self.assertRaisesRegex(ValueError, '重复行'):
            self.inspect(rows + [rows[3]])

    def test_immature_cohort_is_rejected(self):
        with self.assertRaisesRegex(ValueError, '观察窗不足'):
            self.inspect([('A', '2026-08-01', 'register', '测试组')])

    def test_missing_registration_is_rejected(self):
        with self.assertRaisesRegex(ValueError, '注册记录数'):
            self.inspect([('A', '2026-08-08', 'open_app', '测试组')])

    def test_reactivation_requires_prior_churn(self):
        rows, records, audit = self.inspect(self.fixture() + [
            ('A', '2026-08-09', 'reactivate', '测试组'),
            ('B', '2026-08-09', 'churn_flag', '测试组'),
            ('B', '2026-08-10', 'reactivate', '测试组'),
        ])
        reports, _ = run_sql(rows, records)
        core = reports['core_metrics'][0]
        self.assertEqual(core['reactivate_users'], 2)
        self.assertEqual(core['ordered_reactivate_users'], 1)
        self.assertEqual(core['flagged_reactivation_rate_pct'], 100.0)
        self.assertEqual(audit['diagnostics']['reactivate_without_prior_churn']['user_ids'], ['A'])


if __name__ == '__main__':
    unittest.main()
