---
name: next-best-action
description: >
  Designs and implements Next Best Action (NBA) frameworks for customer-facing
  decisions. Covers rule-based, propensity model, and multi-armed bandit
  approaches. Given a customer context, outputs the ranked action
  recommendation with rationale, business rules, and Python implementation.
  Trigger when the user mentions "next best action", "NBA", "what should we
  show this customer", "customer decisioning", "personalization logic",
  "which offer to send", "propensity model", "retention action", "upsell
  trigger", or needs to decide what to do next with a customer based on
  their behavior or attributes.
language: python
libraries: [pandas, numpy, scikit-learn, scipy]
---

# Next Best Action Skill

## Overview

Next Best Action answers: **given everything we know about this customer
right now, what is the single most valuable action we can take?**

NBA balances four forces:
- **Customer value**: what does the customer need or want right now?
- **Business value**: what action drives revenue, retention, or engagement?
- **Feasibility**: what channels and actions are available?
- **Timing**: is now the right moment?

---

## Step 1 — Gather Context

| # | Question | Why it matters |
|---|----------|----------------|
| 1 | What **customer data** is available? (behavior, attributes, history) | Determines signal richness |
| 2 | What is the **action space**? (offers, messages, interventions) | Defines what NBA can recommend |
| 3 | What is the **primary business objective**? (retention, upsell, activation) | Sets the optimization target |
| 4 | What **channels** are available? (email, in-app, push, SMS, call) | Constrains delivery |
| 5 | Are there **hard business rules**? (eligibility, compliance, frequency caps) | Must be enforced before scoring |
| 6 | What is the **decision frequency**? (real-time, daily batch, event-triggered) | Determines architecture |
| 7 | Is there **historical outcome data** for past actions? | Determines if propensity models are feasible |

---

## Step 2 — Choose the NBA Approach

### Approach 1: Rule-based decisioning
**When to use:** Limited data, fast to deploy, highly regulated environment,
or when interpretability is required.

```python
def rule_based_nba(customer: dict) -> str:
    """Simple priority-ordered rule engine."""
    # Hard eligibility gates first
    if customer.get('opted_out'):
        return 'no_action'

    # Highest priority: at-risk customers
    if (customer['days_since_last_login'] > 14 and
            customer['lifetime_value'] > 200):
        return 'winback_offer'

    # Onboarding incomplete
    if (not customer['onboarding_complete'] and
            customer['days_since_signup'] <= 7):
        return 'onboarding_nudge'

    # Upsell: engaged free users
    if (customer['plan'] == 'free' and
            customer['sessions_last_30d'] >= 10):
        return 'upgrade_prompt'

    # Cross-sell: loyal customers
    if (customer['nps_score'] >= 9 and
            customer['tenure_months'] >= 6):
        return 'referral_ask'

    return 'no_action'
```

**Pros:** Transparent, auditable, fast to deploy
**Cons:** Doesn't scale, misses nuance, requires manual maintenance

---

### Approach 2: Propensity scoring + priority ranking
**When to use:** Historical outcome data exists, multiple competing actions,
need to rank by expected value.

```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# ── Train one propensity model per action ────────────────────────────────

def train_propensity_models(df: pd.DataFrame,
                             actions: list,
                             features: list) -> dict:
    """
    Train a binary classifier per action.
    df must have columns: features + one binary column per action
    (1 = customer responded positively to this action when shown).
    """
    models = {}
    for action in actions:
        X = df[features]
        y = df[action]  # 1 = positive response, 0 = no response
        model = Pipeline([
            ('scaler', StandardScaler()),
            ('clf', LogisticRegression(max_iter=500, class_weight='balanced'))
        ])
        model.fit(X, y)
        models[action] = model
    return models


# ── Score a customer against all actions ─────────────────────────────────

def score_customer(customer_features: pd.DataFrame,
                   models: dict,
                   business_value: dict,
                   eligibility_mask: dict = None) -> pd.DataFrame:
    """
    Score one customer against all actions.

    Parameters
    ----------
    customer_features : single-row DataFrame with model features
    models : {action_name: trained_model}
    business_value : {action_name: expected_value_if_accepted} (€ or score)
    eligibility_mask : {action_name: bool} — hard rules applied first

    Returns
    -------
    DataFrame ranked by expected value descending
    """
    results = []
    for action, model in models.items():
        # Hard eligibility check
        if eligibility_mask and not eligibility_mask.get(action, True):
            continue

        propensity = model.predict_proba(customer_features)[0][1]
        ev = propensity * business_value.get(action, 1.0)

        results.append({
            'action': action,
            'propensity': round(propensity, 4),
            'business_value': business_value.get(action, 1.0),
            'expected_value': round(ev, 4),
        })

    return (pd.DataFrame(results)
              .sort_values('expected_value', ascending=False)
              .reset_index(drop=True))


# ── Usage ─────────────────────────────────────────────────────────────────
# actions = ['winback_offer', 'upgrade_prompt', 'referral_ask', 'onboarding_nudge']
# business_value = {'winback_offer': 50, 'upgrade_prompt': 30,
#                   'referral_ask': 20, 'onboarding_nudge': 10}
# models = train_propensity_models(historical_df, actions, features)
# ranking = score_customer(customer_df, models, business_value, eligibility)
# nba = ranking.iloc[0]['action']
```

**Pros:** Data-driven, scales, accounts for customer heterogeneity
**Cons:** Requires labeled historical data, model drift risk

---

### Approach 3: Multi-armed bandit (exploration + exploitation)
**When to use:** No historical data, rapidly changing environment, or you
want to continuously learn the best action online.

```python
import numpy as np

class ThompsonSamplingNBA:
    """
    Thompson Sampling for NBA — balances exploring new actions
    with exploiting known good ones. Uses Beta distribution priors.
    """
    def __init__(self, actions: list):
        self.actions = actions
        # Beta(alpha, beta): alpha = successes + 1, beta = failures + 1
        self.alpha = {a: 1 for a in actions}   # prior: 1 success
        self.beta  = {a: 1 for a in actions}   # prior: 1 failure

    def recommend(self) -> str:
        """Sample from each action's Beta distribution, pick the highest."""
        samples = {
            a: np.random.beta(self.alpha[a], self.beta[a])
            for a in self.actions
        }
        return max(samples, key=samples.get)

    def update(self, action: str, reward: int):
        """Update posterior after observing outcome (1=success, 0=failure)."""
        if reward == 1:
            self.alpha[action] += 1
        else:
            self.beta[action] += 1

    def summary(self) -> pd.DataFrame:
        rows = []
        for a in self.actions:
            mean = self.alpha[a] / (self.alpha[a] + self.beta[a])
            rows.append({'action': a,
                         'estimated_success_rate': round(mean, 4),
                         'trials': self.alpha[a] + self.beta[a] - 2})
        return pd.DataFrame(rows).sort_values('estimated_success_rate',
                                              ascending=False)

# bandit = ThompsonSamplingNBA(['offer_A', 'offer_B', 'offer_C'])
# nba = bandit.recommend()
# ... show action to customer ...
# bandit.update(nba, reward=1)  # 1 if accepted, 0 if ignored
```

**Pros:** No historical data needed, self-improving, handles non-stationarity
**Cons:** Exploration cost, harder to explain to stakeholders

---

## Step 3 — Apply Business Rules (Always)

Business rules act as hard gates **before** any scoring. Always implement
these regardless of approach:

```python
def apply_eligibility_rules(customer: dict, actions: list) -> dict:
    """
    Returns a mask of eligible actions.
    All rules are checked before any scoring occurs.
    """
    mask = {a: True for a in actions}

    # Global exclusions
    if customer.get('opted_out') or customer.get('suppressed'):
        return {a: False for a in actions}

    # Frequency caps: don't contact more than once per 7 days
    if customer.get('days_since_last_contact', 99) < 7:
        mask = {a: False for a in actions}
        return mask

    # Action-specific eligibility
    if customer.get('plan') != 'free':
        mask['upgrade_prompt'] = False   # already paid

    if customer.get('tenure_months', 0) < 3:
        mask['referral_ask'] = False     # too new

    if customer.get('winback_sent_this_quarter'):
        mask['winback_offer'] = False    # already tried

    return mask
```

---

## Step 4 — Decision Approach Selection Guide

| Situation | Recommended approach |
|-----------|---------------------|
| No data, launch phase | Rule-based or Thompson Sampling bandit |
| <1000 historical outcomes per action | Rule-based with basic scoring |
| 1000+ outcomes per action, stable environment | Propensity scoring |
| Dynamic environment, content changes often | Multi-armed bandit |
| Regulated industry (finance, healthcare) | Rule-based (auditable) |
| Real-time decisioning (<100ms) | Pre-scored batch + rules |
| Daily batch decisioning | Propensity scoring pipeline |

---

## Output Format

Always deliver:

### 1. NBA framework diagram (text)
```
Customer Event / Trigger
        ↓
Eligibility Rules (hard gates)
        ↓
Scoring / Ranking (propensity × value)
        ↓
Channel Selection
        ↓
Action Delivered → Outcome Tracked → Model Updated
```

### 2. Action space table
| Action | Trigger condition | Channel | Business value | Eligibility rules |
|--------|------------------|---------|----------------|------------------|

### 3. Complete Python implementation
Tailored to the chosen approach, with customer feature assumptions stated.

### 4. Expected value ranking for a sample customer
| Rank | Action | Propensity | Business value | Expected value |
|------|--------|-----------|----------------|----------------|

### 5. Plain-language recommendation
Which approach to start with, what data to collect first, and what the
first experiment should be.

---

## Key Principles

- **Rules first, models second** — always apply hard business rules before
  any scoring. A model can never override an opt-out or a compliance gate.
- **Expected value = propensity × business value** — don't optimize for
  propensity alone (you'll send easy offers to customers who'd convert anyway).
- **No action is a valid action** — always include `no_action` in the action
  space. Contacting a customer at the wrong time destroys more value than
  waiting.
- **Track everything** — NBA without outcome tracking is a one-way door.
  Every action shown and its result must be logged to improve the system.
- **Start simple** — a well-tuned rule-based system often outperforms a
  poorly trained model. Build complexity only when data justifies it.
