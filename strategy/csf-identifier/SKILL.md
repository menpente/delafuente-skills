---
name: csf-identifier
description: >
  Identifies Critical Success Factors (CSFs) for a business, strategy, or
  project. Follows a structured 6-step process: clarify strategic goals,
  analyze industry context, define key result areas, consolidate with the
  "critical test", and link each CSF to KPIs/OKRs with an owner.
  Trigger when the user mentions "critical success factors", "CSF", "CSFs",
  "what must go right", "make-or-break factors", "strategic priorities",
  "what does our strategy depend on", or asks what a business needs to
  succeed. Also trigger for project kickoffs, strategy reviews, business
  plans, and OKR planning sessions where the user needs to surface the
  non-negotiables.
---

# CSF Identifier Skill

## Overview

A Critical Success Factor is something that **must go right** for a strategic
goal to be achievable. Not nice-to-haves. Not KPIs. The handful of conditions
whose failure makes success impossible.

The output of this skill is always:
1. A short list of 3–7 validated CSFs, each as a clear statement
2. The "critical test" applied to each (why it's non-negotiable)
3. Each CSF linked to 1–3 KPIs or OKRs and an owner

---

## Step 1 — Gather Context

Before identifying CSFs, extract the following. Ask for what's missing.

| # | Question | Why it matters |
|---|----------|----------------|
| 1 | What is the **type of business or project**? (SaaS, retail, consulting, internal initiative, etc.) | Determines industry-specific CSFs |
| 2 | What is the **main strategic goal** for the next 1–3 years? | CSFs must serve a specific goal — not goals in general |
| 3 | What **stage** is the business in? (pre-revenue, growth, scaling, mature) | Early-stage CSFs differ from mature-company CSFs |
| 4 | Who are the **key stakeholders** and what do they care about most? | Surfaces competing priorities |
| 5 | What are the **top 3 threats** to the strategy right now? | Threats often point directly to CSFs |
| 6 | Is there a **SWOT, OKR set, or strategy doc** available? | Accelerates synthesis |

If the user provides minimal context, infer reasonable assumptions from the
business type and ask for confirmation before proceeding.

---

## Step 2 — Analyze Industry and Competitive Context

Before generating CSFs, consider the industry's structural requirements.
Common CSF patterns by sector:

| Sector | Typical CSFs |
|--------|-------------|
| **SaaS / Tech** | Product-market fit, low churn, fast iteration cycle, developer/sales talent |
| **Retail / E-commerce** | Supply chain reliability, customer acquisition cost, repeat purchase rate |
| **Consulting / Services** | Client relationships, talent retention, reputation/differentiation, utilization rate |
| **Healthcare** | Regulatory compliance, patient outcomes, trust, operational efficiency |
| **Manufacturing** | Quality control, cost efficiency, supplier relationships, delivery reliability |
| **Marketplace** | Liquidity (supply and demand balance), trust/safety, network effects |
| **Internal initiative / transformation** | Executive sponsorship, change management, clear ownership, quick wins |

Use these as a calibration check — not as a template to copy. The user's
specific goals and threats should override generic patterns.

---

## Step 3 — Define Key Result Areas (KRAs)

Group the business into functional areas and ask: *what conditions must be
true in each area for the strategy to succeed?*

Standard KRAs to consider:

- **Customer**: acquisition, retention, satisfaction, loyalty
- **Operations**: efficiency, quality, reliability, speed
- **Financial**: unit economics, cash flow, profitability, funding
- **Talent / Culture**: hiring, retention, capability, alignment
- **Product / Innovation**: development speed, differentiation, roadmap
- **Market / Competitive**: positioning, brand, partnerships, distribution
- **Compliance / Risk**: regulatory, legal, reputational, security

For each relevant KRA, surface 1–2 candidate CSFs using this question:

> "What would have to be true in [KRA] for our main goal to be achievable?"

---

## Step 4 — Consolidate and Apply the Critical Test

Take all candidate CSFs and apply a two-part filter:

### The Critical Test
For each candidate, ask:
1. **"If we fail at this, is our main strategic goal impossible?"**
   → If YES: it's a CSF. Keep it.
   → If NO: it's a nice-to-have or a KPI. Remove it from the CSF list.

2. **"Is this within our control or influence?"**
   → If NO: it's a constraint or a risk, not a CSF. Document it separately.

### Consolidation rules
- Combine CSFs that are variations of the same underlying condition
- Write each CSF as a short, active statement (not a KPI, not a project task):
  - ❌ "Increase NPS to 60 by Q4" — this is a KPI
  - ❌ "Launch mobile app" — this is a task
  - ✅ "Deliver a consistently excellent customer experience across all touchpoints"
  - ✅ "Maintain a development cycle that can ship and iterate faster than competitors"
- Aim for **3–7 CSFs**. More than 7 means the critical test wasn't strict enough.

---

## Step 5 — Link CSFs to KPIs/OKRs and Owners

For each validated CSF, define:

| Field | Description |
|-------|-------------|
| **CSF statement** | Short, clear description of the success condition |
| **Why it's critical** | One sentence: what fails if this CSF is missed |
| **Owner** | The role or team accountable for this CSF |
| **KPIs (1–3)** | Measurable indicators that signal the CSF is being achieved |
| **OKR (optional)** | Time-bound objective + key results for the next cycle |
| **Review cadence** | How often to revisit (quarterly recommended) |

---

## Output Format

Always deliver the results as:

### 1. CSF Summary Table

| # | CSF | Why Critical | Owner | KPIs | OKR |
|---|-----|-------------|-------|------|-----|
| 1 | [statement] | [one sentence] | [role] | [1-3 metrics] | [optional] |
| … | | | | | |

### 2. Narrative for each CSF

For each CSF, write a short paragraph (3–5 sentences) that explains:
- What the CSF means in practice
- What "success" looks like concretely
- The most likely failure mode to watch for
- The leading indicator to track before the KPI lags

### 3. Prioritization note

If the list exceeds 5 CSFs, recommend which 2–3 to focus on first, with a
brief rationale based on stage, risk, or strategic leverage.

---

## Example

**Input:** "We're a B2B SaaS startup, 12 months post-launch, €300k ARR,
trying to reach €1M ARR in the next 12 months. Our main risk is churn — we
lose about 8% of customers per month."

**Output (abbreviated):**

| # | CSF | Why Critical | Owner | KPIs |
|---|-----|-------------|-------|------|
| 1 | Deliver enough value in the first 30 days that customers don't cancel | 8% monthly churn makes €1M ARR mathematically unreachable | Head of Customer Success | Day-30 activation rate, 90-day retention, time-to-first-value |
| 2 | Build a repeatable, efficient sales motion for the ICP | Without predictable new ARR, churn losses can't be outrun | Head of Sales | CAC, sales cycle length, win rate by segment |
| 3 | Identify and double down on the customer segment with lowest churn | Current churn may be segment-specific — solving for the wrong customer is burning the runway | CEO / Product | Churn by segment, NRR by cohort |

---

## Key Principles

- **CSFs are not KPIs.** KPIs measure; CSFs define what must be true.
- **CSFs are not tasks.** A CSF is a condition, not an action.
- **3–7 is the right number.** More than 7 means you haven't applied the critical test rigorously.
- **CSFs change.** What's critical at seed stage is not critical at Series B. Revisit annually or after major strategic shifts.
- **Conflict is a signal.** If two stakeholders disagree about CSFs, that disagreement is itself strategically important — surface it explicitly.
