# STAY English V3 网站交付说明

## 本轮完成

保留已确认的 `cover-final.png` 首页和透明交互层；在同一独立目录内完成六章：01 PROJECT BRIEF、02 USER RESEARCH、03 DATA & SQL、04 KEY FINDINGS、05 OPERATIONS PLAN、06 VALIDATION。章节顺序与叙事以 `STAY_English_PORTFOLIO_V2_MASTER_PLAN.md` 为主，运营规则和实验以现有 PRD V1.0 为准。

首页仍直接显示原图，标题使用现有遮罩入场动画。章节页使用原图中的六张章节卡片作为视觉连续性元素，配合米白纸面、钴蓝手写式编号、少量粉/黄/绿/紫笔触和不对称编辑排版。没有重绘或替换封面人物、标题、插画和按钮。

## 交互与文件

- `index.html`：六章内容、章节导航、可展开的 SQL/数据质量说明、PRD 入口。
- `styles.css`：六章统一视觉与桌面/手机断点；首页原图保持原比例。
- `app.js`：原有封面热点/入场动画，以及章节可见性、当前导航状态、PRD 八条运营规则预览。
- `previews/`：首页和六章的桌面/手机首屏截图，供审阅。
- `ASSET_SOURCES.md`：使用素材与 GitHub 检索结果。

网站没有新增框架或第三方运行时依赖。GitHub 技术参考见 `ASSET_SOURCES.md`。

## 内容边界

8 位访谈用户、40 条回答、1000 名用户、7306 条事件均为模拟。漏斗是注册队列观察点；23 位 D7 用户无 D1 记录，页面没有把 237/451 写成阶段转化。05 为 PRD 方案规则演示；06 的三组实验未真实上线，也没有真实提升结果。

## 基础检查

以本地 Chrome 测试了 1440px 桌面、390px 手机和 320px 小屏：六个章节锚点、规则切换、无横向溢出、无 JS 报错；`prefers-reduced-motion` 可关闭动效。正常动效模式下标题遮罩完成后移除，章节按视口轻量显示。`portfolio/` 与 `portfolio_v2/` 的文件哈希在本轮前后相同。
