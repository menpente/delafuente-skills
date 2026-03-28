---
name: statistical-test-selector
description: >
  Selects the right statistical test based on dataset characteristics and
  research goal. Accepts flexible input (text description, CSV sample, or
  Python DataFrame), runs programmatic assumption checks, and outputs:
  (1) recommended test with justification, (2) ready-to-run Python code
  with effect sizes, (3) assumption checklist (verified and pending).
  Trigger when user asks "which statistical test", "how do I compare groups",
  "is there a significant difference", "is there a correlation", or uploads
  data and asks about significance, relationships, or predictions.
language: python
libraries: [scipy, statsmodels, pandas, numpy, pingouin]
---

# Statistical Test Selector Skill

## Overview

When a user asks which statistical test to use — or describes their data and
goal — follow this skill to select the right test, validate assumptions
programmatically, and deliver working Python code.

---

## Step 1 — Gather Context

Extract from the conversation or dataset. Ask only for what is missing.

| # | Question | Why it matters |
|---|----------|----------------|
| 1 | What is the **research question**? (compare groups / find relationship / predict) | Determines test family |
| 2 | What is the **dependent variable** and its measurement level? (nominal / ordinal / continuous) | Determines parametric eligibility |
| 3 | What are the **independent variables** (if any) and their levels? | Determines test type |
| 4 | Are observations **independent** or **paired/repeated**? | Paired vs. unpaired tests |
| 5 | How many **groups or categories**? | t-test vs. ANOVA vs. chi-square |
| 6 | Approximate **sample size** per group? | Exact tests for n < 20 |
| 7 | Is a **dataset or DataFrame available**? | Enables automated assumption checks |

If the user provides data, infer as many answers as possible before asking.

---

## Step 2 — Decision Tree

### A. Comparing groups (is there a difference?)

```
Dependent variable continuous?
├── YES → Are observations paired?
│   ├── PAIRED → normality of differences?
│   │   ├── Normal → Paired t-test
│   │   └── Non-normal → Wilcoxon signed-rank
│   └── INDEPENDENT → How many groups?
│       ├── 2 groups → Use Welch's t-test by default (works regardless of equal/unequal variance)
│       │   └── Non-normal or n < 20 → Mann-Whitney U
│       └── 3+ groups → One-way ANOVA
│           ├── Non-normal → Kruskal-Wallis
│           └── Post-hoc: Tukey HSD (equal n), Games-Howell (unequal variance)
└── NO (categorical) → Chi-square test of independence
    ├── Expected cell counts < 5 AND 2×2 table → Fisher's exact
    ├── Expected cell counts < 5 AND larger table → Chi-square + Monte Carlo simulation
    └── Note: scipy.stats.fisher_exact only works on 2×2 tables
```

### B. Finding relationships (is there an association?)

```
Both variables continuous?
├── YES → Pearson correlation (if linear + normal)
│   └── Non-linear or non-normal → Spearman correlation
└── NO → One continuous + one categorical → Point-biserial correlation
    └── Both ordinal → Spearman or Kendall's tau
```

### C. Predicting (what drives the outcome?)

```
Continuous outcome → Linear regression (OLS)
├── Multiple predictors → Multiple linear regression
└── Binary outcome → Logistic regression
    └── Ordinal outcome → Ordinal logistic regression
```

### D. Special cases

- **Multiple testing** (many comparisons): Apply Bonferroni correction or use FDR (Benjamini-Hochberg)
- **Repeated measures + multiple groups**: Mixed ANOVA or LME (statsmodels)
- **Time series data**: Don't use standard tests — use autocorrelation-aware methods
- **Very small n (< 10 per group)**: Prefer exact tests, report with caution

---

## Step 3 — Programmatic Assumption Checks

Always run these checks in code before recommending the final test:

```python
import numpy as np
import pandas as pd
from scipy import stats

def check_normality(data, alpha=0.05):
    """Shapiro-Wilk for n<=50, D'Agostino-Pearson for n>50."""
    n = len(data)
    if n <= 50:
        stat, p = stats.shapiro(data)
        test_name = "Shapiro-Wilk"
    else:
        stat, p = stats.normaltest(data)
        test_name = "D'Agostino-Pearson"
    return {"test": test_name, "statistic": stat, "p_value": p,
            "normal": p > alpha, "n": n}

def check_equal_variance(*groups, alpha=0.05):
    """Levene's test for equal variances across groups."""
    stat, p = stats.levene(*groups)
    return {"test": "Levene", "statistic": stat, "p_value": p,
            "equal_variance": p > alpha}

def check_outliers_iqr(data, threshold=1.5):
    """Flag outliers using IQR method."""
    Q1, Q3 = np.percentile(data, [25, 75])
    IQR = Q3 - Q1
    lower, upper = Q1 - threshold * IQR, Q3 + threshold * IQR
    outliers = data[(data < lower) | (data > upper)]
    return {"n_outliers": len(outliers), "lower_bound": lower,
            "upper_bound": upper, "outlier_values": outliers.tolist()}

def expected_cell_counts(contingency_table):
    """Check minimum expected count for chi-square validity."""
    _, _, _, expected = stats.chi2_contingency(contingency_table)
    min_expected = expected.min()
    pct_below_5 = (expected < 5).mean() * 100
    return {"min_expected": min_expected, "pct_cells_below_5": pct_below_5,
            "chi2_valid": pct_below_5 < 20}
```

---

## Step 4 — Output Format

Always deliver three sections:

### 1. Recommended test + justification
State the test name, why it was selected, and which assumption checks passed/failed.

### 2. Assumption checklist table

| Assumption | Required for | Status | Notes |
|-----------|-------------|--------|-------|
| Normality | t-test, ANOVA | ✅ / ❌ / ⚠️ | p-value from Shapiro/D'Agostino |
| Equal variance | ANOVA, independent t | ✅ / ❌ | Levene's test result |
| Independence | All tests | ✅ / ❌ | Confirmed from design |
| Sample size | Fisher's exact | ✅ / ❌ | n per group |
| No severe outliers | Parametric tests | ✅ / ❌ | IQR check result |

### 3. Ready-to-run Python code

Include:
- The assumption checks
- The test itself
- Effect size (Cohen's d, eta², Cramér's V, r — depending on test)
- Interpretation of results in plain language

```python
# Example: Welch's t-test with effect size
from scipy import stats
import numpy as np

# Run assumption checks first
norm_a = check_normality(group_a)
norm_b = check_normality(group_b)
print(f"Normality group A: {'✅' if norm_a['normal'] else '❌'} (p={norm_a['p_value']:.3f})")
print(f"Normality group B: {'✅' if norm_b['normal'] else '❌'} (p={norm_b['p_value']:.3f})")

# Welch's t-test (equal_var=False is the safe default)
t_stat, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)

# Cohen's d effect size
pooled_std = np.sqrt((np.std(group_a)**2 + np.std(group_b)**2) / 2)
cohens_d = (np.mean(group_a) - np.mean(group_b)) / pooled_std

print(f"\nWelch's t-test: t={t_stat:.3f}, p={p_value:.4f}")
print(f"Cohen's d: {cohens_d:.3f}  ({'small' if abs(cohens_d)<0.5 else 'medium' if abs(cohens_d)<0.8 else 'large'} effect)")
print(f"Conclusion: {'Significant difference' if p_value < 0.05 else 'No significant difference'} at α=0.05")
```

---

## Key Rules

- **Welch's t-test is the default for 2-group comparisons** — it works whether variances are equal or not. Never use Student's t-test without first confirming equal variance.
- **Fisher's exact is 2×2 only** in scipy. For larger tables with low expected counts, use chi-square with Monte Carlo: `stats.chi2_contingency(table, lambda_="log-likelihood")` or `pingouin.chi2_independence`.
- **Always report effect size**, not just p-values. Statistical significance ≠ practical significance.
- **Check normality on differences** (not raw scores) for paired tests.
- **Suggest `pingouin`** for cleaner API when dealing with chi-square + small n, effect sizes, or repeated measures ANOVA.
