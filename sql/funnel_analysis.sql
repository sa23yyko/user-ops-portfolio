-- 模拟数据 / 独立项目。SQLite 语法，无需外部服务。
-- 输入表 user_events(user_id TEXT, event_date TEXT, event_type TEXT, user_type TEXT)。
-- 运行：python3 analysis/verify_metrics.py（自动导入原始 CSV 并执行本文件）。
-- 留存以注册日为 D0，分母为注册用户；open_app 为当前留存事件口径。
-- 观察窗可用性仅按文件最大日期判断，不代表已验证逐用户采集完整性。
CREATE TEMP VIEW portfolio_user_metrics AS
WITH registrations AS (
    SELECT user_id, MIN(event_date) AS reg_date, MIN(user_type) AS user_type
    FROM user_events WHERE event_type = 'register' GROUP BY user_id
), offsets AS (
    SELECT r.*, e.event_type, e.event_date,
           CAST(julianday(e.event_date) - julianday(r.reg_date) AS INTEGER) AS day_no
    FROM registrations r JOIN user_events e USING (user_id)
)
SELECT user_id, user_type, reg_date,
       MAX(CASE WHEN day_no = 0 AND event_type = 'start_learning' THEN 1 ELSE 0 END) AS activated,
       MAX(CASE WHEN day_no = 1 AND event_type = 'open_app' THEN 1 ELSE 0 END) AS d1,
       MAX(CASE WHEN day_no = 7 AND event_type = 'open_app' THEN 1 ELSE 0 END) AS d7,
       MAX(CASE WHEN day_no = 0 AND event_type = 'complete_task' THEN 1 ELSE 0 END) AS day0_complete,
       COUNT(DISTINCT CASE WHEN day_no BETWEEN 0 AND 6 AND event_type IN ('start_learning','complete_task') THEN event_date END) AS learning_days_d0_d6,
       MAX(CASE WHEN event_type = 'churn_flag' THEN 1 ELSE 0 END) AS churn,
       MAX(CASE WHEN event_type = 'reactivate' THEN 1 ELSE 0 END) AS reactivated,
       MIN(CASE WHEN event_type = 'churn_flag' THEN event_date END) AS first_churn_date,
       MIN(CASE WHEN event_type = 'reactivate' THEN event_date END) AS first_reactivate_date,
       CASE WHEN date(reg_date, '+7 day') <= (SELECT MAX(event_date) FROM user_events) THEN 1 ELSE 0 END AS d7_observable
FROM offsets GROUP BY user_id, user_type, reg_date;

-- report: core_metrics
SELECT '模拟数据 / 独立项目' AS data_status,
       COUNT(*) AS registered_users,
       SUM(activated) AS activated_users,
       ROUND(100.0 * SUM(activated) / COUNT(*), 2) AS activation_rate_pct,
       SUM(d1) AS d1_users, ROUND(100.0 * SUM(d1) / COUNT(*), 2) AS d1_rate_pct,
       SUM(d7) AS d7_users, ROUND(100.0 * SUM(d7) / COUNT(*), 2) AS d7_rate_pct,
       SUM(day0_complete) AS day0_complete_users,
       ROUND(100.0 * SUM(day0_complete) / COUNT(*), 2) AS day0_complete_rate_pct,
       SUM(churn) AS churn_flag_users, SUM(reactivated) AS reactivate_users,
       SUM(churn * reactivated) AS churn_and_reactivate_users,
       SUM(CASE WHEN first_reactivate_date > first_churn_date THEN 1 ELSE 0 END) AS ordered_reactivate_users,
       ROUND(100.0 * SUM(CASE WHEN first_reactivate_date > first_churn_date THEN 1 ELSE 0 END) / NULLIF(SUM(churn), 0), 2) AS flagged_reactivation_rate_pct,
       SUM(activated * d1 * d7) AS strict_funnel_d7_users,
       SUM(d1 * d7) AS d1_and_d7_users,
       ROUND(100.0 * SUM(d1 * d7) / NULLIF(SUM(d1), 0), 2) AS d7_among_d1_rate_pct,
       SUM(CASE WHEN d7 = 1 AND d1 = 0 THEN 1 ELSE 0 END) AS d7_without_d1_users,
       SUM(d7_observable) AS d7_observable_users
FROM portfolio_user_metrics;

-- report: segment_metrics
SELECT '模拟数据 / 独立项目' AS data_status, user_type, COUNT(*) AS registered_users,
       SUM(activated) AS activated_users, ROUND(100.0 * SUM(activated) / COUNT(*), 2) AS activation_rate_pct,
       SUM(d1) AS d1_users, ROUND(100.0 * SUM(d1) / COUNT(*), 2) AS d1_rate_pct,
       SUM(d7) AS d7_users, ROUND(100.0 * SUM(d7) / COUNT(*), 2) AS d7_rate_pct
FROM portfolio_user_metrics GROUP BY user_type ORDER BY d7_rate_pct DESC, user_type;

-- report: day0_completion
SELECT '模拟数据 / 独立项目' AS data_status, 'all_registered' AS population,
       day0_complete, COUNT(*) AS users, SUM(d7) AS d7_users,
       ROUND(100.0 * SUM(d7) / COUNT(*), 2) AS d7_rate_pct
FROM portfolio_user_metrics GROUP BY day0_complete
UNION ALL
SELECT '模拟数据 / 独立项目', 'activated_only', day0_complete, COUNT(*), SUM(d7),
       ROUND(100.0 * SUM(d7) / COUNT(*), 2)
FROM portfolio_user_metrics WHERE activated = 1 GROUP BY day0_complete;

-- report: learning_activity
SELECT '模拟数据 / 独立项目' AS data_status,
       CASE WHEN learning_days_d0_d6 = 0 THEN '0天'
            WHEN learning_days_d0_d6 <= 2 THEN '1–2天'
            ELSE '3–7天' END AS learning_days_group,
       COUNT(*) AS users, SUM(d7) AS d7_users,
       ROUND(100.0 * SUM(d7) / COUNT(*), 2) AS d7_rate_pct
FROM portfolio_user_metrics GROUP BY learning_days_group ORDER BY learning_days_group;

-- report: churn_reactivation
SELECT '模拟数据 / 独立项目' AS data_status, churn, reactivated, COUNT(*) AS users
FROM portfolio_user_metrics GROUP BY churn, reactivated ORDER BY churn, reactivated;

-- report: registration_cohorts
SELECT '模拟数据 / 独立项目' AS data_status, reg_date, COUNT(*) AS registered_users,
       SUM(d7_observable) AS d7_observable_users, SUM(d7) AS d7_users,
       ROUND(100.0 * SUM(d7) / COUNT(*), 2) AS d7_rate_pct
FROM portfolio_user_metrics GROUP BY reg_date ORDER BY reg_date;

-- report: event_distribution
SELECT '模拟数据 / 独立项目' AS data_status, event_type, COUNT(*) AS event_rows,
       COUNT(DISTINCT user_id) AS distinct_users
FROM user_events GROUP BY event_type ORDER BY event_type;
