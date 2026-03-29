---
name: input-output-metrics
description: >
  Classifies metrics as input (leading, controllable) or output (lagging,
  outcome) and builds a metric tree showing how inputs influence outputs.
  Surfaces missing input metrics when only outputs are provided. Designed for
  analytics and data teams building metric frameworks, dashboards, or OKR
  measurement systems. Trigger when the user mentions "input metrics", "output
  metrics", "leading vs lagging indicators", "metric framework", "metric tree",
  "influence diagram", "what metrics should I track", "what drives this KPI",
  "I only have outcome metrics", "north star metric", or asks how to measure
  a business goal or product area.
---

# Input vs Output Metrics Skill

## Overview

**Output metrics** (lagging) measure what happened — the result.
**Input metrics** (leading) measure the actions and conditions that cause the result.

The key insight for analytics teams: output metrics tell you *if* something
is working. Input metrics tell you *why* and *what to do about it*.

A well-designed metric framework always has both, with an explicit causal
chain connecting inputs to outputs.

---

## The Taxonomy

### Output metrics
- Measure outcomes, not activity
- Lag behind the actions that caused them (days, weeks, months)
- Hard to move directly — you can only influence them through inputs
- Examples: revenue, churn rate, NPS, DAU, profit margin, conversion rate

### Input metrics
- Measure controllable actions or conditions that *cause* outputs
- Lead the outcome — change first, output changes later
- Directly actionable by a team or individual
- Examples: response time, feature adoption rate, onboarding completion,
  number of experiments shipped, call connect rate, content published

### The critical test
> "Can a team directly change this metric by deciding to act differently today?"

- YES → input metric
- NO (it's the result of many factors over time) → output metric

### Guard rails and counter-metrics
A third category to always include: metrics that prevent gaming.
- If the input metric is "calls made per day" → guard rail is "call quality score"
- If the input metric is "features shipped" → guard rail is "bug rate / incident count"
- Always pair each input metric with at least one guard rail

---

## Step 1 — Gather Context

| # | Question | Why it matters |
|---|----------|----------------|
| 1 | What is the **north star or top-level output metric**? | Anchors the entire tree |
| 2 | What **team or function** owns this metric framework? | Determines relevant input levers |
| 3 | What **product or business area** is in scope? | Narrows the causal model |
| 4 | What metrics are **already being tracked**? | Avoids duplication, surfaces gaps |
| 5 | What is the **time horizon** for impact? | Separates true leading from lagging |
| 6 | Are there **known drivers** the team already believes in? | Starting hypothesis for the tree |

If the user provides a list of existing metrics without classification, proceed
directly to Step 3.

---

## Step 2 — Build the Metric Tree

A metric tree decomposes the top-level output into its causal drivers,
layer by layer, until you reach actionable input metrics.

### Structure
```
[North Star Output Metric]
├── [Sub-output 1]         ← still lagging, but more specific
│   ├── [Input A]          ← directly actionable
│   └── [Input B]
└── [Sub-output 2]
    ├── [Input C]
    ├── [Input D]
    └── [Guard rail for C/D]
```

### Decomposition rules
1. **Each level must be causally linked** — not just correlated. Ask "does
   changing this reliably move the level above?"
2. **Each branch must be exhaustive and mutually exclusive at its level**
   (MECE) — the sub-metrics should fully explain the parent metric
3. **Stop decomposing when you reach an actionable input** — a metric a
   team can change by deciding to act differently
4. **Maximum 3 levels deep** for clarity — deeper than that, split into
   sub-trees

### Common decomposition patterns

**Revenue tree:**
```
Revenue
├── New revenue
│   ├── Leads generated          [input]
│   ├── Lead-to-opportunity rate [input]
│   └── Win rate                 [input → guard rail: discount rate]
└── Retained revenue
    ├── Churn rate               [output]
    │   ├── Onboarding completion rate  [input]
    │   ├── Feature adoption (core)     [input]
    │   └── Support ticket resolution time [input]
    └── Expansion revenue
        ├── Upsell attempts      [input]
        └── NPS / CSAT           [leading output → input for expansion]
```

**Product engagement tree:**
```
DAU / WAU
├── Activation rate              [output]
│   ├── Time to first value      [input]
│   └── Onboarding step completion [input]
├── Retention (D7, D30)         [output]
│   ├── Core feature adoption    [input]
│   ├── Habit-forming actions/week [input]
│   └── Support deflection rate  [guard rail]
└── Resurrection rate            [output]
    └── Re-engagement campaign CTR [input]
```

---

## Step 3 — Classify Provided Metrics

If the user provides a metric list, classify each one using this framework:

### Classification algorithm

```
For each metric:
1. Apply the controllability test:
   "Can a team directly change this by deciding to act today?"
   → YES: input candidate
   → NO: output candidate

2. Apply the time-lag test:
   "Does this metric reflect past actions (days/weeks/months ago)?"
   → YES: output
   → NO (reflects current or near-real-time state): input candidate

3. Apply the causal direction test:
   "Does this metric CAUSE changes in other metrics, or is it CAUSED BY them?"
   → CAUSES others: input
   → CAUSED BY others: output
   → BOTH: intermediate metric (sub-output that is also an input to a higher level)

4. Flag guard rails:
   "Is this metric primarily here to prevent gaming or unintended consequences?"
   → YES: guard rail (label separately)
```

### Output table format

| Metric | Type | Causal direction | Time lag | Actionable by | Guard rail needed |
|--------|------|-----------------|----------|---------------|-------------------|
| [name] | Input / Output / Intermediate | → drives [X] / ← driven by [Y] | Days / Weeks / Months | [team/role] | [suggested guard rail or N/A] |

---

## Step 4 — Surface Missing Input Metrics

When only output metrics are provided (or the input layer is thin), generate
candidate input metrics using this diagnostic:

### For each output metric without sufficient inputs, ask:

1. **What human behaviors drive this metric?**
   (e.g., churn is driven by: product usage frequency, support experience,
   perceived value vs price, competitive alternatives)

2. **What process steps precede this outcome?**
   (e.g., conversion is preceded by: landing page visit → sign-up → activation
   → first purchase — instrument each step)

3. **What is the earliest leading signal of this outcome?**
   (e.g., for 30-day retention, the D3 login rate is often the earliest
   reliable predictor — find the earliest inflection point)

4. **What does the team actually control?**
   (e.g., if churn is the output, the team controls: onboarding flow,
   feature discoverability, support SLA, in-app nudges)

### Common missing input metrics by output

| Output | Often-missing inputs |
|--------|---------------------|
| Revenue / ARR | Lead quality score, sales cycle length by segment, demo-to-trial conversion |
| Churn | Onboarding completion rate, core feature adoption (week 1), health score |
| NPS / CSAT | First response time, resolution rate, effort score (CES) |
| DAU/WAU | Time-to-first-value, D1/D3 retention, habit-loop completion rate |
| Conversion rate | Funnel step drop-off rates, time-on-page, micro-conversion rates |
| Employee retention | Manager effectiveness score, internal mobility rate, recognition frequency |

---

## Step 5 — Render the Metric Tree (Text Diagram)

Always produce a text-based tree diagram for easy copy-paste into Notion,
Confluence, or a slide. Use this format:

```
[NORTH STAR: metric name]
│
├── [SUB-OUTPUT: metric name]          lag: X weeks
│   ├── [INPUT: metric name]           owner: Team A
│   │   └── ⚠ guard rail: [metric]
│   └── [INPUT: metric name]           owner: Team B
│
└── [SUB-OUTPUT: metric name]          lag: X weeks
    ├── [INPUT: metric name]           owner: Team C
    └── [INPUT: metric name]           owner: Team D
        └── ⚠ guard rail: [metric]

Legend:
  [OUTPUT]       — lagging, measures results
  [INPUT]        — leading, directly actionable
  ⚠ guard rail  — prevents gaming or unintended consequences
```

---

## Output Format

Always deliver in this order:

1. **Classification table** — every provided metric classified with type,
   causal direction, time lag, owner, and guard rail recommendation
2. **Missing inputs** — for each output without sufficient inputs, suggest
   2–3 candidate input metrics with rationale
3. **Metric tree** — text diagram showing the full causal structure from
   north star to actionable inputs
4. **Narrative** — 3–5 sentences interpreting the framework: where the
   causal chain is strong, where it's weak, and the one metric the team
   should add first if they're starting from scratch

---

## Key Principles

- **Output metrics are for accountability. Input metrics are for management.**
  Review outputs with leadership; manage day-to-day via inputs.
- **If your dashboard is all outputs, you're flying blind.** You'll know
  something went wrong weeks after it happened.
- **If your dashboard is all inputs, you're optimizing in the dark.** You
  need outputs to know if the inputs are actually working.
- **Correlation ≠ causation in a metric tree.** Every causal link should be
  backed by either an experiment, a mechanism, or strong domain logic.
- **The best input metric is the earliest reliable predictor of your
  most important output.** Finding it is worth running experiments.
- **Always add a guard rail.** Every input metric can be gamed. The guard
  rail is what keeps the incentive honest.
