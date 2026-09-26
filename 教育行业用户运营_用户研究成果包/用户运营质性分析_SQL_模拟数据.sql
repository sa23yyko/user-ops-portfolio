-- 教育行业用户运营：用户研究与质性编码
-- 数据口径：模拟独立项目数据，不代表真实用户调研或平台业务数据。
-- 语法以 SQLite 为主，字段类型可按 MySQL/PostgreSQL 调整。

DROP TABLE IF EXISTS user_interview_coding;
CREATE TABLE user_interview_coding (
    user_id TEXT,
    user_type TEXT,
    motivation_code TEXT,
    behavior_code TEXT,
    pain_point_code TEXT,
    trigger_code TEXT,
    stage TEXT
);

INSERT INTO user_interview_coding VALUES
('U01','四六级冲刺型','考试目标明确','启动成本高','任务不明确','低门槛任务','激活'),
('U02','考研长期型','长期备考','计划过载','任务负荷过重','动态计划','留存'),
('U03','雅思留学型','高目标/高投入','选择困难','内容过载','个性化推荐','激活/留存'),
('U04','托福留学型','效果导向','反馈不足','看不到进步','成长反馈','留存'),
('U05','职业证书型','碎片时间','时间不匹配','任务颗粒度过大','10分钟微任务','留存'),
('U06','兴趣提升型','弱目标','学习理由不足','缺乏紧迫性','兴趣内容/轻激励','激活/留存'),
('U07','职场提升型','工作场景驱动','优先级低','被工作打断','场景化内容','召回'),
('U08','习惯打卡型','习惯驱动','激励依赖','断签挫败','补签/温和激励','留存/召回');

-- 1. 统计不同痛点出现频次
SELECT pain_point_code,
       COUNT(*) AS user_count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM user_interview_coding), 1) AS user_share_pct
FROM user_interview_coding
GROUP BY pain_point_code
ORDER BY user_count DESC;

-- 2. 按用户类型查看痛点
SELECT user_type, pain_point_code, COUNT(*) AS user_count
FROM user_interview_coding
GROUP BY user_type, pain_point_code
ORDER BY user_type, user_count DESC;

-- 3. 看不同生命周期环节对应的运营触发
SELECT stage, trigger_code, COUNT(*) AS user_count
FROM user_interview_coding
GROUP BY stage, trigger_code
ORDER BY user_count DESC;

-- 4. 筛选对个性化/反馈较敏感的用户
SELECT user_id, user_type, pain_point_code, trigger_code
FROM user_interview_coding
WHERE pain_point_code IN ('内容过载','看不到进步')
   OR trigger_code IN ('个性化推荐','成长反馈');
