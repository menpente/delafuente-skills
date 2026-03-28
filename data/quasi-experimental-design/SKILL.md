---
name: quasi-experimental-design
description: >
  Selects and implements the right quasi-experimental method when randomized
  controlled trials are not possible. Covers Difference-in-Differences (DiD),
  Regression Discontinuity Design (RDD), Instrumental Variables (IV),
  Synthetic Control, and Interrupted Time Series (ITS). Trigger when user
  asks about causal inference, "did this intervention work", "impact of a
  policy", "natural experiment", "we can't randomize", DiD, RDD, synthetic
  control, or counterfactual analysis.
language: python
libraries: [pandas, numpy, statsmodels, linearmodels, scipy]
---

# Quasi-Experimental Design Skill

## Overview

Use this skill when the user wants to estimate a **causal effect** but
randomization was not possible. The goal is to find a credible counterfactual:
what would have happened to the treated group had they not been treated?

---

## Step 1 — Gather Context

| # | Question | Why it matters |
|---|----------|----------------|
| 1 | What is the **treatment/intervention**? | Defines what we're estimating |
| 2 | What is the **outcome variable**? | Defines what we're measuring |
| 3 | Was assignment to treatment **arbitrary** in some way? | Determines method eligibility |
| 4 | Is there a **cutoff or threshold** that determined treatment? | → RDD |
| 5 | Is there **pre-treatment data** for treated and control groups? | → DiD |
| 6 | Is there an **external variable** that affects treatment but not outcome? | → IV |
| 7 | Is there a **clear date** when treatment started, with a time series? | → ITS |
| 8 | Are there **donor units** (untreated similar entities)? | → Synthetic Control |

---

## Step 2 — Method Selection

```
Can you randomize?
└── NO → Is there a sharp cutoff that determined treatment?
    ├── YES → Regression Discontinuity Design (RDD)
    └── NO → Do you have treated AND control groups with pre-treatment data?
        ├── YES → Difference-in-Differences (DiD)
        │   └── No control group, just time series? → Interrupted Time Series (ITS)
        └── NO → Is there an instrument (variable affecting treatment but not outcome)?
            ├── YES → Instrumental Variables (IV)
            └── NO (aggregate data, few treated units) → Synthetic Control
```

---

## Method 1: Difference-in-Differences (DiD)

**When to use:** You have panel or repeated cross-sectional data, a treatment group, a control group, and pre/post periods.

**Core assumption:** Parallel trends — in the absence of treatment, treated and control groups would have followed the same trend.

**How to check parallel trends:**
- Plot pre-treatment trends for both groups visually
- Run a placebo test using only pre-treatment periods
- Test for divergence in pre-period using leads (should be non-significant)

```python
import pandas as pd
import statsmodels.formula.api as smf

# df must have: outcome, treated (0/1), post (0/1), unit_id, time
# DiD coefficient is the interaction term: treated * post

model = smf.ols(
    'outcome ~ treated + post + treated:post + C(unit_id)',
    data=df
).fit(cov_type='cluster', cov_kwds={'groups': df['unit_id']})

print(model.summary())
did_estimate = model.params['treated:post']
print(f"\nDiD estimate (ATT): {did_estimate:.4f}")
print(f"p-value: {model.pvalues['treated:post']:.4f}")

# Parallel trends check: plot mean outcome by group over time
import matplotlib.pyplot as plt
df.groupby(['time', 'treated'])['outcome'].mean().unstack().plot()
plt.axvline(x=treatment_period, linestyle='--', color='red', label='Treatment')
plt.legend(); plt.title('Parallel Trends Check'); plt.show()
```

**Robustness checks:**
- Add unit fixed effects (`C(unit_id)`) and time fixed effects (`C(time)`)
- Use clustered standard errors at the unit level
- Run placebo tests with fake treatment dates
- Check for anticipation effects (leads)

---

## Method 2: Regression Discontinuity Design (RDD)

**When to use:** Treatment was assigned based on whether a continuous "running variable" (score, age, income) crossed a known cutoff.

**Core assumption:** Units just below and just above the cutoff are similar in all ways except treatment assignment.

**Sharp RDD** (all units above cutoff are treated):

```python
import numpy as np
import statsmodels.formula.api as smf

# Center running variable at cutoff
df['running_c'] = df['running_var'] - cutoff
df['treated'] = (df['running_var'] >= cutoff).astype(int)

# Bandwidth selection: use ~1 SD of running variable or IK optimal bandwidth
bandwidth = df['running_c'].std()
df_bw = df[df['running_c'].abs() <= bandwidth].copy()

# Local linear regression on each side of cutoff
model = smf.ols(
    'outcome ~ running_c + treated + running_c:treated',
    data=df_bw
).fit()

rdd_estimate = model.params['treated']
print(f"RDD estimate (LATE at cutoff): {rdd_estimate:.4f}")
print(f"p-value: {model.pvalues['treated']:.4f}")

# Density test (McCrary test) — check for manipulation at cutoff
# Treated and control density should be continuous at cutoff
```

**Key checks:**
- McCrary density test (no bunching at cutoff)
- Covariate smoothness at cutoff (pre-treatment covariates should not jump)
- Sensitivity to bandwidth choice

---

## Method 3: Instrumental Variables (IV)

**When to use:** Treatment is endogenous (correlated with unobserved confounders). You have a variable (instrument) that affects treatment but has no direct effect on outcome.

**Classic instruments:** lottery assignment, distance to facility, policy changes, natural disasters.

**Validity conditions:**
1. **Relevance**: instrument strongly correlated with treatment (F-statistic > 10)
2. **Exclusion restriction**: instrument affects outcome ONLY through treatment
3. **Independence**: instrument is as-good-as-randomly assigned

```python
from linearmodels.iv import IV2SLS

# formula: outcome ~ exog_vars + [endogenous ~ instruments]
model = IV2SLS.from_formula(
    'outcome ~ 1 + controls + [treatment ~ instrument]',
    data=df
).fit(cov_type='robust')

print(model.summary)
iv_estimate = model.params['treatment']

# First-stage F-statistic (must be > 10 for instrument relevance)
first_stage = IV2SLS.from_formula(
    'treatment ~ 1 + controls + instrument',
    data=df
).fit()
print(f"\nFirst-stage F-stat: {first_stage.first_stage.diagnostics}")
```

**Key checks:**
- First-stage F-statistic > 10 (weak instrument test)
- Overidentification test (Sargan-Hansen) if multiple instruments
- Plausibility of exclusion restriction (theoretical argument required)

---

## Method 4: Synthetic Control

**When to use:** One or few treated units (countries, regions, companies), many pre-treatment periods, several untreated "donor" units.

**Core idea:** Build a weighted combination of donor units that best matches the treated unit's pre-treatment trajectory. The counterfactual = what synthetic control does post-treatment.

```python
import numpy as np
from scipy.optimize import minimize

def synthetic_control(treated_pre, donors_pre):
    """Find weights for donor units that minimize pre-treatment RMSE."""
    n_donors = donors_pre.shape[1]
    
    def objective(w):
        synthetic = donors_pre @ w
        return np.sum((treated_pre - synthetic) ** 2)
    
    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = [(0, 1)] * n_donors
    w0 = np.ones(n_donors) / n_donors
    
    result = minimize(objective, w0, method='SLSQP',
                     bounds=bounds, constraints=constraints)
    return result.x

# weights = synthetic_control(treated_pre_series, donor_matrix_pre)
# synthetic_post = donor_matrix_post @ weights
# gap = treated_post - synthetic_post  (treatment effect over time)
```

**Key checks:**
- Pre-treatment fit quality (RMSPE should be low)
- Permutation inference: run placebo synth controls for all donor units
- If treated unit's post-treatment gap > donor gaps → significant effect

---

## Method 5: Interrupted Time Series (ITS)

**When to use:** Single group, clear intervention date, multiple time points before and after. No control group required.

**Core assumption:** Pre-treatment trend was stable and would have continued without intervention.

```python
import statsmodels.formula.api as smf
import pandas as pd

# df must have: outcome, time (integer), treated (0 before, 1 after), time_since_treatment
model = smf.ols(
    'outcome ~ time + treated + time_since_treatment',
    data=df
).fit()

print(model.summary())
level_change = model.params['treated']          # Immediate level shift
slope_change = model.params['time_since_treatment']  # Change in trend

print(f"\nImmediate level change: {level_change:.4f} (p={model.pvalues['treated']:.4f})")
print(f"Slope change: {slope_change:.4f} (p={model.pvalues['time_since_treatment']:.4f})")
```

**Key checks:**
- Autocorrelation in residuals (use Newey-West SEs or ARIMA errors)
- No other concurrent interventions
- Sufficient pre-period observations (≥ 12 recommended)

---

## Output Format

Always deliver:

1. **Method recommendation** — which method fits the design and why
2. **Assumptions checklist** — what holds, what needs to be argued or tested
3. **Ready-to-run Python code** with the chosen method
4. **Robustness checks** — what to run to stress-test the result
5. **Plain-language interpretation** — "The intervention increased X by Y units (95% CI: ...)"

## Common Mistakes to Flag

- Using DiD without checking parallel trends
- Using RDD with a bandwidth that's too wide (loses local validity)
- Weak instruments in IV (F < 10) — biased toward OLS
- ITS with too few pre-period observations
- Confusing correlation with causation when assumptions aren't met
