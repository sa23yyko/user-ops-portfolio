# 第一次使用 Codex｜最简单的工作流

## 推荐方式：ChatGPT 桌面版里的 Codex

1. 在 Mac 上安装最新版 ChatGPT 桌面应用。
2. 使用自己的 ChatGPT 账号登录。
3. 左上角切换到 Codex。
4. 在桌面新建一个文件夹，例如：
   `~/Desktop/user-ops-portfolio`
5. 把 ChatGPT 生成并下载的项目资料全部放进这个文件夹。
6. 把下面两个文件也放进去：
   - `PROJECT_MASTER_CONTEXT.md`
   - `CODEX_EXECUTION_PROMPT.md`
7. 在 Codex 中选择/打开这个项目文件夹。
8. 把 `CODEX_EXECUTION_PROMPT.md` 的内容作为第一条任务发给 Codex。
9. 第一次让 Codex 先“读取、检查、规划”，然后再允许它创建/修改文件。
10. 每次阶段完成后，优先查看 git diff 或 Codex 的文件变更列表，不要盲目接受所有改动。

## 不需要安装什么？

完成这个“用户运营作品集网页 + 数据分析”项目：
- 不需要任何第三方插件
- 不需要 OpenAI API key
- 不需要部署数据库服务器
- 不需要安装 Figma/Axure
- 不需要购买外部服务

Codex 只要能访问项目本地文件，并能使用 Python/终端，就足够完成大部分工作。

## 可选方式：Codex CLI

如果希望在终端使用，可以安装 Codex CLI。

常见方式：
- npm：`npm install -g @openai/codex@latest`
- 或 Homebrew 安装/更新 Codex（按官方最新说明操作）

安装后：
- 在终端 `cd` 到项目文件夹
- 运行 `codex`
- 使用 ChatGPT 登录
- 粘贴 `CODEX_EXECUTION_PROMPT.md`

## 可选方式：VS Code

如果习惯 VS Code：
- 安装 OpenAI 官方 Codex IDE 扩展
- 打开项目文件夹
- 在 Codex 面板中发出任务

不要把 ChatGPT macOS 的“Work with Apps”扩展误认为必须的 Codex 扩展。那个扩展用于 ChatGPT 与 VS Code 等应用协作，不是完成本项目的前置条件。

## 插件建议

### 本项目不必安装
- OpenAI Developers plugin：主要用于构建/调试 OpenAI API 应用。这个用户运营作品集不需要调用 OpenAI API，因此不是必需。
- 第三方插件：不建议第一次使用时安装。先用纯 Codex + 本地文件把项目跑通。

### 以后可能有用
- 如果未来要开发 OpenAI API 应用，再安装 OpenAI Developers plugin。
- 如果未来要连接外部工具/服务，再根据明确需求安装插件。

## 最佳文件组织

建议项目根目录最终类似：

user-ops-portfolio/
├── PROJECT_MASTER_CONTEXT.md
├── CODEX_EXECUTION_PROMPT.md
├── README.md
├── data/
│   ├── english_app_user_events_1000.csv
│   ├── 用户样本库_模拟数据.csv
│   ├── 用户访谈质性编码_模拟数据.csv
│   └── 用户痛点汇总_模拟数据.csv
├── research/
│   ├── 用户访谈记录.docx
│   └── 用户研究成果包.xlsx
├── analysis/
│   └── verify_metrics.py
├── sql/
│   └── funnel_analysis.sql
├── portfolio/
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── docs/
    ├── PORTFOLIO_CASE_STUDY.md
    ├── resume_project_summary.md
    └── interview_story.md

## 第一次运行后应该检查的 5 件事

1. Codex 有没有把“模拟项目”误写成真实公司项目？
2. 漏斗数字有没有从 CSV 重新计算？
3. 网页是否能本地打开？
4. 图表是否明确标“模拟数据”？
5. 简历项目表述有没有夸大成真实业务成果？
