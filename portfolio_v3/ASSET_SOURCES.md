# V3 视觉素材与技术参考

## 实际使用的视觉素材

- `assets/cover-final.png`：项目根目录 `cover-final.png` 的原图副本。首页直接显示这张最终设计稿；六章页头的小卡片从同一张图的现有章节卡片区域读取，不重画人物、字形、图标或封面布局。
- `assets/STAY_English_PRD.docx`：项目现有 PRD 的副本，供 `VIEW PRD` 下载。
- 网站没有引入第三方插画、字体、图标包或远程 CDN。正文的线条、纸张边框、色块和交互采用本项目原生 HTML/CSS/JS。

## 检索到的开源参考

这些链接用于评估实现方式和未来可选素材；当前版本没有复制或打包其中的代码、图形或字体。

1. [Rough.js](https://github.com/rough-stuff/rough) — MIT；可用 SVG/Canvas 生成手绘线条。当前页面只需少量静态笔触，因此未增加运行时依赖。
2. [Iconoodle](https://github.com/NK2552003/Iconoodle) — MIT；可导出独立 SVG doodle。已确定的封面优先于外部图标，当前版本未导入这些素材。
3. [Signature Studio](https://github.com/Technical-1/Signature-Studio) — SVG 笔画逐段呈现的技术思路。当前首页保留此前基于原图遮罩的蜡笔标题 reveal，不重新绘制标题。

## 视觉依据与事实边界

视觉第一优先级是用户提供的 `cover-final.png`；`doodle_reference_color.png`、`doodle_reference_mono.png` 和 `references/` 中的两张图用于判断手绘线条、配色与纸张质感，没有直接放进网页。内容以 `STAY_English_PORTFOLIO_V2_MASTER_PLAN.md` 为主，PRD V1.0 提供运营规则与实验细节。所有访谈、用户、事件和分析结果均为个人独立模拟项目材料。
