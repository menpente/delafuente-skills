---
name: jobs-to-be-done
description: >
  Applies the Jobs To Be Done (JTBD) framework to understand why customers
  buy, switch, or churn. Extracts functional, emotional, and social jobs from
  interviews, reviews, or product descriptions. Produces job statements,
  opportunity scoring, and strategic implications for product, marketing, and
  positioning. Trigger when the user mentions "jobs to be done", "JTBD",
  "why do customers buy", "customer motivation", "switching triggers",
  "hire a product", "fire a product", "underlying need", "what job is this
  product doing", "customer insight", "product-market fit", "voice of
  customer", or wants to understand what customers are really trying to
  accomplish beyond surface-level feature requests.
---

# Jobs To Be Done Skill

## Overview

Jobs To Be Done reframes the question from *"what do customers want?"* to
*"what are customers trying to accomplish?"*

The core insight: customers don't buy products — they **hire** products to
do a job. When the job is done well, they keep the product. When it isn't,
they fire it and hire something else.

JTBD has three layers:
- **Functional job**: the practical task to be accomplished
- **Emotional job**: how the customer wants to feel (or avoid feeling)
- **Social job**: how the customer wants to be perceived by others

A complete JTBD analysis uncovers all three layers and connects them to
product, pricing, messaging, and positioning decisions.

---

## Step 1 — Gather Context

| # | Question | Why it matters |
|---|----------|----------------|
| 1 | What **product or feature** is being analyzed? | Anchors the job space |
| 2 | What **customer segment** is in focus? | Different segments have different jobs |
| 3 | What **inputs** are available? (interviews, reviews, surveys, support tickets) | Determines depth of analysis possible |
| 4 | Are we analyzing **acquisition** (why they hired), **retention** (why they stay), or **churn** (why they fired)? | Changes the job framing |
| 5 | What **competitors** or **alternatives** are customers switching from/to? | The "other hire" reveals the real job |

If raw customer language is provided (quotes, reviews, tickets), extract
jobs from that. Otherwise, generate hypotheses based on the product context.

---

## Step 2 — Extract Jobs from Customer Language

### The four JTBD signals to listen for

**1. Struggling moments** — when customers describe friction, workarounds,
or frustration. The job is what they're trying to accomplish despite the
struggle.
> *"I spend hours every Monday compiling reports from three different tools"*
> → Job: get a clear picture of last week's performance without manual effort

**2. Hire/fire language** — what triggered the switch to or from a product.
> *"We switched when our team grew past 10 people and spreadsheets stopped working"*
> → Job: coordinate work across a team without losing track of who owns what

**3. Progress language** — what "better" looks like to the customer.
> *"I just want to feel confident that nothing is falling through the cracks"*
> → Emotional job: peace of mind and sense of control

**4. Workaround language** — what customers do when the product doesn't
fully do the job.
> *"I export to Excel and build my own pivot tables"*
> → Unmet functional job: flexible data analysis without switching tools

### Job extraction template

For each customer quote or insight, extract:

```
Raw quote: "[customer's words]"

Functional job:   When [situation], I want to [action], so I can [outcome].
Emotional job:    When I do this, I want to feel [emotion] / avoid feeling [negative emotion].
Social job:       When others see me doing this, I want to be perceived as [identity].
Current hire:     [product/workaround currently used for this job]
Job quality:      How well is the current hire doing this job? (1–5)
Opportunity:      High / Medium / Low (importance × dissatisfaction)
```

---

## Step 3 — Write Job Statements

A well-formed job statement follows this structure:

> **When** [situation/trigger], **I want to** [motivation/action], **so I can** [desired outcome].

### Rules for good job statements
- **Situation-specific** — the "when" matters. The same person has different
  jobs in different contexts.
- **Solution-free** — never mention a product, feature, or technology in the
  job statement. The job exists independently of any solution.
- **Stable over time** — a good job statement would have been true 20 years
  ago and will be true 20 years from now. If it references an app or
  platform, it's too specific.
- **From the customer's perspective** — use first-person, customer language,
  not product or company language.

### Examples

| ❌ Weak (solution-dependent) | ✅ Strong (solution-free) |
|------------------------------|--------------------------|
| "Use our dashboard to track KPIs" | "When I present to leadership, I want to show progress clearly so I can build confidence in my team's work" |
| "Get Slack notifications for deadlines" | "When I'm deep in work, I want to know about urgent issues without constantly checking tools" |
| "Generate reports with one click" | "When my week ends, I want a clear summary of what happened so I can plan the next week confidently" |

---

## Step 4 — Opportunity Scoring

Opportunity score identifies which jobs are most worth solving. It uses
Tony Ulwick's formula:

```
Opportunity Score = Importance + max(Importance − Satisfaction, 0)
```

Where:
- **Importance**: how important is this job to the customer? (1–10)
- **Satisfaction**: how well are existing solutions doing this job? (1–10)

```python
import pandas as pd

def opportunity_score(importance: float, satisfaction: float) -> float:
    """
    Ulwick's opportunity algorithm.
    High importance + low satisfaction = high opportunity.
    Score > 10 = underserved market (prime opportunity).
    Score < 10 = overserved or adequately served.
    """
    return importance + max(importance - satisfaction, 0)

jobs_data = [
    {"job": "Get a clear weekly performance summary without manual work",
     "importance": 9, "satisfaction": 3},
    {"job": "Share results with non-technical stakeholders easily",
     "importance": 8, "satisfaction": 5},
    {"job": "Spot anomalies in metrics before they become problems",
     "importance": 9, "satisfaction": 2},
    {"job": "Onboard new team members to the data stack quickly",
     "importance": 6, "satisfaction": 6},
]

df = pd.DataFrame(jobs_data)
df['opportunity_score'] = df.apply(
    lambda r: opportunity_score(r['importance'], r['satisfaction']), axis=1
)
df = df.sort_values('opportunity_score', ascending=False)
df['priority'] = df['opportunity_score'].apply(
    lambda s: '🔴 Underserved' if s >= 12 else
              '🟡 Opportunity' if s >= 10 else
              '🟢 Adequately served'
)
print(df[['job', 'importance', 'satisfaction',
          'opportunity_score', 'priority']].to_string(index=False))
```

**Interpretation:**
- Score ≥ 12: **Underserved** — high importance, low satisfaction. Prime
  product opportunity.
- Score 10–12: **Opportunity** — worth addressing, but competitive pressure
  may exist.
- Score < 10: **Overserved or fine** — customers are satisfied; more
  investment here risks over-engineering.

---

## Step 5 — Forces of Progress (Switch Analysis)

When analyzing why customers switch (churn or acquisition), use the Four
Forces model:

```
PUSH (away from old)                PULL (toward new)
─────────────────────               ─────────────────────
Frustrations with current solution  Attraction of new solution
Anxiety about staying               Hope for progress

ANXIETY (about switching)           HABIT (inertia)
─────────────────────               ─────────────────────
Fear of learning curve              "This is how we've always done it"
Risk of disruption                  Switching costs (data, integrations)
Uncertainty about new solution      Team resistance to change
```

For a switch to happen, Push + Pull must overcome Anxiety + Habit.

```python
forces = {
    "push": [
        "Reporting takes 3+ hours every Monday",
        "Can't share live dashboards with clients",
        "No mobile access",
    ],
    "pull": [
        "Automated weekly digest sent to Slack",
        "Client-facing portal with branded reports",
        "Real-time mobile alerts",
    ],
    "anxiety": [
        "Migration of 2 years of historical data",
        "Team needs retraining",
        "Cost increase vs current tool",
    ],
    "habit": [
        "Current tool integrated with 6 other systems",
        "CEO is used to current report format",
        "IT procurement process takes 3 months",
    ],
}
# Use this to: identify what messaging must address (anxiety/habit),
# what product must deliver (pull), and what pain to surface in sales (push).
```

---

## Step 6 — Strategic Implications

After mapping jobs and opportunity scores, always translate findings into
decisions across four areas:

### Product
- Which underserved jobs should the roadmap prioritize?
- What features exist only to satisfy over-served jobs (candidates to cut)?
- What workarounds reveal unmet jobs worth productizing?

### Messaging / Marketing
- Job statements → headline copy. The job IS the value proposition.
- Emotional and social jobs → brand tone and aspiration.
- Switch triggers → ad targeting moments (search intent, competitor keywords).

### Pricing
- Customers pay based on job importance, not feature count.
- Underserved, high-importance jobs can support premium pricing.
- If customers are over-served, they may be paying for jobs they don't need
  — a packaging/tiering opportunity.

### Sales
- Push forces → discovery questions to surface pain.
- Anxiety forces → objection-handling scripts.
- Pull forces → demo narrative: show the job being done, not the features.

---

## Output Format

Always deliver:

### 1. Job map table
| Job statement | Type | Importance | Satisfaction | Opportunity score | Priority |
|--------------|------|-----------|-------------|-------------------|---------|

### 2. Full job statements (narrative)
For the top 3–5 jobs: functional + emotional + social layers, current hire,
and what a better solution would look like.

### 3. Forces of progress (if switch analysis requested)
Four-quadrant table: push / pull / anxiety / habit.

### 4. Strategic implications
One paragraph each on product, messaging, pricing, and sales implications.

### 5. Top 3 recommended actions
Concrete next steps ranked by opportunity score and feasibility.

---

## Key Principles

- **The job, not the customer** — segments are demographic; jobs are
  motivational. The same person has multiple jobs and hires different
  products for each.
- **The competition is anything that does the job** — a spreadsheet, a
  workaround, a person, or doing nothing are all competitors.
- **Features don't create loyalty — job completion does** — customers
  stay when the job gets done better and better over time.
- **Listen for struggle, not preferences** — customers can't tell you what
  they want, but they'll show you where they struggle. Follow the struggle.
- **A job statement that names a technology is not a job statement** — if
  it mentions your product or any specific tool, rewrite it.
