# delafuente-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-11-blue)](#skills)
[![Built with Claude](https://img.shields.io/badge/built%20with-Claude-blueviolet)](https://claude.ai)
[![delafuente.ai](https://img.shields.io/badge/web-delafuente.ai-lightgrey)](https://delafuente.ai)

Claude skill library for data science, DevOps, and communications work.
Built and maintained by [Ruben de la Fuente](https://delafuente.ai).

## What is a skill?

A skill is a `SKILL.md` file that gives Claude structured instructions for a specific task — decision trees, output formats, code templates, and quality checks. Claude reads the skill before responding, producing consistently better output than a generic prompt.

Skills live in `/mnt/skills/user/` in the Claude environment and are triggered automatically based on the user's request.

---

## Structure

```
delafuente-skills/
├── data/                        # Statistical analysis and data visualization
│   ├── statistical-test-selector/
│   ├── quasi-experimental-design/
│   ├── xmr-chart/
│   ├── 6-12-chart/
│   ├── input-output-metrics/
│   ├── linear-programming/
│   └── next-best-action/
├── comms/                       # Content creation and presentation
│   ├── linkedin-post-creator/
│   └── slidestart-pptx/
└── strategy/                    # Business strategy and planning
    ├── csf-identifier/
    └── jobs-to-be-done/
```

---

## Skills

### 📊 Data

#### `statistical-test-selector`
Selects the right statistical test based on data type, research question, and sample size. Runs programmatic assumption checks (Shapiro-Wilk, Levene's, IQR), outputs the recommended test with justification, a ready-to-run Python code block with effect sizes, and a checklist of assumptions verified vs pending.

**Triggers:** "which statistical test", "is there a significant difference", "how do I compare groups", "is there a correlation"

---

#### `quasi-experimental-design`
Selects and implements the right causal inference method when randomization isn't possible. Covers DiD, RDD, IV, Synthetic Control, and ITS — each with Python code, assumption checks, and robustness tests.

**Triggers:** "did this intervention work", "causal inference", "natural experiment", "we can't randomize", DiD, RDD, synthetic control

---

#### `xmr-chart`
Builds XmR (Process Behavior) charts to distinguish signal from noise in time series data. Computes natural process limits, detects signals using all four standard rules, and generates a two-panel chart (X chart + mR chart) with plain-language interpretation.

**Triggers:** "XmR", "control chart", "process behavior chart", "is this variation normal", "SPC", "signal or noise"

---

#### `6-12-chart`
Creates year-over-year comparison charts plotting the current 12-month window against the prior 12 months. Includes a delta bar chart, summary table with YoY % by month, and totals row.

**Triggers:** "6-12 chart", "year-over-year", "YoY comparison", "current year vs last year", "same period last year"

---

#### `input-output-metrics`
Classifies metrics as input (leading, controllable) or output (lagging, outcome) and builds a metric tree showing how inputs influence outputs. Surfaces missing input metrics when only outputs are provided. Includes guard rail recommendations to prevent gaming.

**Triggers:** "input metrics", "output metrics", "leading vs lagging", "metric framework", "metric tree", "what drives this KPI", "I only have outcome metrics", "north star metric"

---

#### `linear-programming`
Formulates and solves LP, Integer, Mixed-Integer, and Binary programming problems from plain-language descriptions. Extracts decision variables, objective function, and constraints from prose; solves with PuLP (CBC) or SciPy; delivers mathematical formulation, full Python code, solution table, sensitivity analysis, and plain-language interpretation.

**Triggers:** "linear programming", "LP", "optimize", "maximize", "minimize", "subject to constraints", "resource allocation", "scheduling problem", "blending problem", "transportation problem", "assignment problem"

---

#### `next-best-action`
Designs and implements Next Best Action (NBA) frameworks for customer-facing decisions. Covers rule-based, propensity scoring, and multi-armed bandit (Thompson Sampling) approaches. Outputs a ranked action recommendation with business rules, Python implementation, and expected value table.

**Triggers:** "next best action", "NBA", "what should we show this customer", "customer decisioning", "which offer to send", "propensity model", "retention action", "upsell trigger"

---

### 📣 Comms

#### `linkedin-post-creator`
Writes high-engagement LinkedIn posts with a companion whiteboard-style infographic (PNG + React preview). Uses a 4-type post system (hard-earned lesson, practical breakdown, contrarian insight, positioning post) with enforced tension, specific CTAs, and a 7-point self-check before delivery.

**Triggers:** "LinkedIn post", "thought leadership", "hard-earned lesson", "positioning post", "contrarian take", "practical breakdown"

---

#### `slidestart-pptx`
Produces consulting-grade PowerPoint decks inspired by McKinsey/BCG style. Applies Pyramid Principle / SCQA structure, proper data visualization choices, and a consistent design system. Outputs a `.pptx` file.

**Triggers:** "slide deck", "presentation", "consulting slides", "pitch deck", "McKinsey style"

---

### 🎯 Strategy

#### `csf-identifier`
Identifies Critical Success Factors (CSFs) for a business, strategy, or project. Follows a 6-step process: clarify strategic goals, analyze industry context, define key result areas, apply the critical test, and link each CSF to KPIs/OKRs with an owner. Outputs a summary table, a narrative per CSF, and a prioritization note.

**Triggers:** "critical success factors", "CSF", "what must go right", "make-or-break factors", "strategic priorities", project kickoffs, strategy reviews, OKR planning sessions

---

#### `jobs-to-be-done`
Applies the Jobs To Be Done (JTBD) framework to understand why customers buy, switch, or churn. Extracts functional, emotional, and social jobs from interviews or reviews. Produces job statements, Ulwick opportunity scores, Four Forces switch analysis, and strategic implications for product, messaging, pricing, and sales.

**Triggers:** "jobs to be done", "JTBD", "why do customers buy", "customer motivation", "switching triggers", "hire a product", "what job is this product doing", "product-market fit", "voice of customer"

---

## Usage

1. Copy the desired skill folder into `/mnt/skills/user/` in your Claude environment
2. Claude will automatically detect and use the skill based on your request
3. You can also explicitly ask: *"Use the xmr-chart skill to..."*

---

## Roadmap

- `strategy/okr-planner` — OKR design and alignment from strategy to team level
- `strategy/swot-to-strategy` — structured SWOT → strategic options → priorities
- `devops/dora-metrics` — DORA metrics interpreter with LLM analysis
- `devops/incident-postmortem` — structured incident report generator
- `data/wbr-report` — Weekly Business Review from CSV
- `comms/roobs-video-producer` — YouTube production package (EN/ES)

---

## License

MIT — use freely, attribution appreciated.

Built with [Claude](https://claude.ai) · [delafuente.ai](https://delafuente.ai)
