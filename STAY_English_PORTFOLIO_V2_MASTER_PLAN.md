# STAY English Portfolio V2 — Master Rebuild Plan

## 0. Purpose

This file is the source of truth for the portfolio V2 rebuild.

The existing website in `portfolio/` is the completed V1 case-study archive.  
**Do not modify, overwrite, rename, move, or delete `portfolio/`.**

The rebuild will create a new website in:

`portfolio_v2/`

The goal of V2 is not to show a long research report. It is to present a concise **language-learning user-operations plan** with research and SQL as evidence.

---

## 1. Project positioning

### Project name
**STAY English**

### Chinese title
**语言学习产品新用户激活与留存运营策划**

### Subtitle
**基于用户访谈、AI模拟行为数据与SQL分析的分层学习陪伴方案**

### Project nature
Personal independent simulated project / 个人独立模拟项目

### One-sentence definition
通过“用户研究 → 模拟数据 → SQL分析 → 运营规则 → PRD → A/B验证”，设计一套面向语言学习产品新用户的分层学习陪伴机制。

---

## 2. V2 narrative

The V2 main story must be:

1. Why this operations project exists
2. How users were researched
3. How simulated data and SQL were used
4. What the analysis found
5. What executable operations plan was designed
6. How the plan would be validated

The six main sections are fixed:

### 01 — PROJECT BRIEF
Why this project / background / problem / goal

### 02 — USER RESEARCH
8 original user types → interview/coding → 4 operational need segments

### 03 — DATA & SQL
AI-simulated behavior data + SQL analysis methodology + core code evidence

### 04 — KEY FINDINGS
Condensed findings from funnel, segmentation and early behavior analysis

### 05 — OPERATIONS PLAN
The core deliverable: STAY Engine / WHO × WHEN → WHAT / PRD-based executable operating rules and copy

### 06 — VALIDATION
A/B experiments + hypothesis testing

---

## 3. Important logic that must never be changed

### User research logic
The research starts with 8 original language-learning user types:

- 四六级冲刺型
- 考研长期型
- 雅思留学型
- 托福留学型
- 职业证书型
- 兴趣提升型
- 职场提升型
- 习惯打卡型

The four operational segments are **not** the starting point. They are derived after qualitative analysis:

- 目标驱动型
- 碎片学习型
- 兴趣成长型
- 习惯激励型

Correct chain:

`8类原始用户 → 模拟访谈/质性编码 → 4类运营需求分层 → 1000人模拟行为数据 → SQL分析 → 运营方案`

### Data boundary
- 8 interview users are simulated.
- 40 interview responses are simulated.
- 1000 behavior users are simulated.
- 7306 event logs are simulated.
- SQL findings are methodology demonstrations, not real business evidence.
- Do not claim real retention lift, real launch results, or causal effects.

---

## 4. Main-site vs detail content

V2 will be intentionally concise.

The six main pages should show only the information needed to understand the project.

Detailed evidence will later be opened through interaction, for example:

- `VIEW DETAILS`
- `VIEW SQL`
- `VIEW INTERVIEW EVIDENCE`
- `VIEW PRD`
- `VIEW DATA AUDIT`
- `VIEW EXPERIMENT DETAILS`

Possible interaction patterns:
- side drawer
- modal
- expandable detail panel
- dedicated detail route/page

Do not put all detail on the six main pages.

The existing V1 site remains a full research archive and can later serve as evidence/reference.

---

## 5. Round 1 scope — skeleton only

In Round 1, do **not** rebuild all content.

Create only:

### A. New V2 website
Create a new self-contained folder:

`portfolio_v2/`

Suggested minimum files:
- `portfolio_v2/index.html`
- `portfolio_v2/styles.css`
- `portfolio_v2/app.js`
- `portfolio_v2/assets/` only if needed

### B. New cover
The cover must immediately communicate that this is an operations plan.

Required cover text:

**STAY English**

**语言学习产品新用户激活与留存运营策划**

**基于用户访谈、AI模拟行为数据与SQL分析的分层学习陪伴方案**

Small labels may include:
`USER OPERATIONS / EDTECH / PERSONAL SIMULATED PROJECT / 2026`

The cover may reuse the established cobalt blue + warm cream + black visual system and hand-drawn editorial style from V1.

### C. Interactive six-section directory
Add an interactive directory/navigation with exactly six entries:

01 PROJECT BRIEF  
02 USER RESEARCH  
03 DATA & SQL  
04 KEY FINDINGS  
05 OPERATIONS PLAN  
06 VALIDATION

Each directory item must be clickable and jump/scroll to the matching section.

Desktop and mobile must both work.

### D. Six empty sections
Create the six sections, but **do not fill their body content yet**.

Each section should contain only:
- section number
- English section title
- optional Chinese title if needed for clarity

No research copy, charts, tables, SQL, cards, PRD content, or detailed placeholders in this round.

The goal is to approve:
- cover
- navigation
- overall rhythm
- six-page structure

before filling content.

---

## 6. Visual direction

Preserve the established visual identity from V1:

- Editorial Portfolio
- Playful Minimalism
- Hand-drawn doodle
- slightly retro printed-paper feeling
- cobalt blue + warm cream + black
- large numbers
- strong typography
- thin rules / L-lines
- asymmetrical editorial layout
- restrained motion

Avoid:
- SaaS dashboard look
- glassmorphism
- gradients
- neon/glow
- excessive rounded cards
- stock icon libraries
- heavy parallax

V2 should feel more concise and presentation-like than V1.

---

## 7. Interaction direction

For this round:
- directory click → smooth scroll / anchor
- hover/focus states
- current-section indicator if easy
- mobile navigation
- reduced-motion support

Do not build detail modals/drawers yet.
We will add them later when each page's content is finalized.

---

## 8. File organization target

Do not reorganize old files in Round 1. Avoid breaking existing paths.

Target project taxonomy for later cleanup:

```text
user-ops-portfolio/
├── portfolio/                  # V1 full website — frozen archive
├── portfolio_v2/               # new concise six-section website
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── assets/
├── docs/
│   ├── STAY_English_V1.0_PRD.docx
│   └── rebuild/
│       ├── STAY_English_PORTFOLIO_V2_MASTER_PLAN.md
│       └── CODEX_V2_ROUND1_PROMPT.txt
├── research/                   # interview/coding/source research files
├── data/
│   ├── raw/                    # original simulated datasets
│   └── derived/                # later calculated tables/exports
├── analysis/                   # analysis scripts/results
├── sql/                        # SQL queries
├── references/                 # visual references
└── archive/                    # obsolete handoff zips / superseded notes
```

Important:
- Do not move existing files now unless explicitly requested.
- First create V2 safely.
- Reorganize only after V2 runs correctly.

---

## 9. Source-of-truth priority

When rebuilding V2, use this priority:

1. `STAY_English_PORTFOLIO_V2_MASTER_PLAN.md`
2. `STAY_English_V1.0_PRD.docx`
3. approved simulated data / SQL outputs
4. existing `portfolio/` only as visual and evidence reference
5. older draft plans only when they do not conflict with the files above

---

## 10. Future rounds

After Round 1 is approved:

Round 2:
- Fill 01 PROJECT BRIEF
- Fill 02 USER RESEARCH

Round 3:
- Fill 03 DATA & SQL
- Fill 04 KEY FINDINGS

Round 4:
- Fill 05 OPERATIONS PLAN
- connect PRD and build expandable detail content

Round 5:
- Fill 06 VALIDATION
- build detail interactions

Round 6:
- Build the separate STAY English interactive demo
- link it from 05 OPERATIONS PLAN

Final:
- responsive QA
- visual consistency
- deployable website
- optional PDF export

---

## 11. Current principle

**Do not optimize the old V1 site. Do not delete it. Do not rebuild everything at once.**

Build V2 progressively, approve structure first, then fill content.
