---
name: xmr-chart
description: >
  Creates XmR charts (Individual and Moving Range charts), also known as
  Process Behavior Charts. The XmR chart is the right tool for detecting
  whether variation in a metric is routine (noise) or exceptional (signal).
  Trigger when user mentions "XmR", "process behavior chart", "control chart",
  "is this variation normal", "natural process limits", "statistical process
  control", "SPC", "is this a signal or noise", or wants to know if a change
  in a time series metric is meaningful. Output: limits table + Python chart.
language: python
libraries: [pandas, numpy, matplotlib]
---

# XmR Chart Skill (Process Behavior Chart)

## Overview

An XmR chart answers one question: **is this variation signal or noise?**

It consists of two charts:
- **X chart** (Individuals): plots each data point with a center line (mean) and upper/lower natural process limits (UNPL/LNPL)
- **mR chart** (Moving Range): plots the point-to-point variation with an upper range limit (URL)

Use it for any time-ordered sequence of individual measurements: weekly revenue, monthly churn, daily error rate, NPS scores, deployment frequency, etc.

---

## Step 1 — Gather Context

| # | Question | Why it matters |
|---|----------|----------------|
| 1 | What is the metric? | Labels and context |
| 2 | What is the time period / frequency? | X axis |
| 3 | Is there a known process change or intervention to annotate? | Baseline recalculation |
| 4 | How many data points? | Need ≥ 10; recommend 20-30 for stable limits |
| 5 | Should limits be calculated on a baseline period? | Useful when a known shift occurred |

---

## Step 2 — Calculate Limits

XmR limits are derived from the **average moving range** (mR̄), not from standard deviation. This makes them robust to outliers.

```python
import numpy as np
import pandas as pd

def calculate_xmr_limits(values, baseline_end=None):
    """
    Calculate XmR chart limits.
    
    Parameters
    ----------
    values : array-like — time-ordered measurements
    baseline_end : int or None — if set, calculate limits using only
                   values[:baseline_end] and project forward
    
    Returns
    -------
    dict with: X_bar, UNPL, LNPL, mR_bar, URL
    """
    values = np.array(values, dtype=float)
    
    # Use baseline period if specified
    baseline = values[:baseline_end] if baseline_end else values
    
    # Moving ranges (absolute successive differences)
    mR = np.abs(np.diff(baseline))
    mR_bar = np.mean(mR)     # Average moving range
    X_bar  = np.mean(baseline)  # Process average
    
    # Scaling constant d2 = 1.128 for n=2 (successive pairs)
    d2 = 1.128
    sigma_hat = mR_bar / d2  # Estimated process sigma
    
    # Natural Process Limits (±3 sigma)
    UNPL = X_bar + 3 * sigma_hat
    LNPL = X_bar - 3 * sigma_hat
    
    # Upper Range Limit (D4 * mR_bar, D4=3.267 for n=2)
    D4 = 3.267
    URL = D4 * mR_bar
    
    return {
        "X_bar": X_bar,
        "UNPL": UNPL,
        "LNPL": LNPL,
        "mR_bar": mR_bar,
        "URL": URL,
        "sigma_hat": sigma_hat,
    }
```

---

## Step 3 — Detect Signals

Four standard signal rules (use all four every time):

```python
def detect_signals(values, limits):
    """
    Detect signals using the four standard XmR rules.
    Returns a boolean array: True = signal at that index.
    """
    values = np.array(values, dtype=float)
    X_bar = limits["X_bar"]
    UNPL  = limits["UNPL"]
    LNPL  = limits["LNPL"]
    sigma = limits["sigma_hat"]
    n = len(values)
    signals = np.zeros(n, dtype=bool)

    # Rule 1: Any point outside the natural process limits
    signals |= (values > UNPL) | (values < LNPL)

    # Rule 2: 8 consecutive points on the same side of the center line
    for i in range(7, n):
        run = values[i-7:i+1]
        if np.all(run > X_bar) or np.all(run < X_bar):
            signals[i-7:i+1] = True

    # Rule 3: 3 out of 3 consecutive points in the outer third (beyond ±2σ)
    outer_upper = X_bar + 2 * sigma
    outer_lower = X_bar - 2 * sigma
    for i in range(2, n):
        window = values[i-2:i+1]
        if (np.sum(window > outer_upper) >= 3 or
                np.sum(window < outer_lower) >= 3):
            signals[i-2:i+1] = True

    # Rule 4: 6 consecutive points trending up or down
    for i in range(5, n):
        window = values[i-5:i+1]
        diffs = np.diff(window)
        if np.all(diffs > 0) or np.all(diffs < 0):
            signals[i-5:i+1] = True

    return signals
```

---

## Step 4 — Plot

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def plot_xmr(dates, values, metric_name="Metric", baseline_end=None,
             annotation=None):
    """
    Plot a full XmR chart (X chart + mR chart).
    
    Parameters
    ----------
    dates : array-like — x-axis labels (dates or period strings)
    values : array-like — measurements
    metric_name : str — label for the metric
    baseline_end : int — index to split baseline from projection
    annotation : dict — {"index": i, "label": "Event name"} for vertical line
    """
    values = np.array(values, dtype=float)
    mR_values = np.abs(np.diff(values))
    limits = calculate_xmr_limits(values, baseline_end)
    signals = detect_signals(values, limits)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    fig.suptitle(f"XmR Chart — {metric_name}", fontsize=14, fontweight='bold')

    # ── X chart ──────────────────────────────────────────────
    ax1.plot(dates, values, 'o-', color='#1d3557', linewidth=1.5,
             markersize=5, zorder=3, label=metric_name)
    ax1.axhline(limits["X_bar"], color='#457b9d', linewidth=1.5,
                linestyle='-', label=f"X̄ = {limits['X_bar']:.2f}")
    ax1.axhline(limits["UNPL"], color='#e63946', linewidth=1.5,
                linestyle='--', label=f"UNPL = {limits['UNPL']:.2f}")
    ax1.axhline(limits["LNPL"], color='#e63946', linewidth=1.5,
                linestyle='--', label=f"LNPL = {limits['LNPL']:.2f}")

    # Shade ±1σ and ±2σ zones
    s = limits["sigma_hat"]
    ax1.axhspan(limits["X_bar"] - s,  limits["X_bar"] + s,
                alpha=0.06, color='#2a9d8f')
    ax1.axhspan(limits["X_bar"] - 2*s, limits["X_bar"] + 2*s,
                alpha=0.04, color='#457b9d')

    # Highlight signals
    signal_dates = [dates[i] for i in range(len(values)) if signals[i]]
    signal_vals  = [values[i] for i in range(len(values)) if signals[i]]
    if signal_dates:
        ax1.scatter(signal_dates, signal_vals, color='#e63946',
                    s=80, zorder=5, label='Signal')

    # Annotation line
    if annotation:
        ax1.axvline(x=dates[annotation["index"]], color='#e63946',
                    linestyle=':', linewidth=1.5)
        ax1.text(dates[annotation["index"]], limits["UNPL"],
                 f'  {annotation["label"]}', fontsize=9, color='#e63946')

    ax1.set_ylabel(metric_name)
    ax1.legend(fontsize=8, loc='upper left')
    ax1.grid(axis='y', alpha=0.3)

    # ── mR chart ─────────────────────────────────────────────
    ax2.plot(dates[1:], mR_values, 'o-', color='#457b9d', linewidth=1.5,
             markersize=4)
    ax2.axhline(limits["mR_bar"], color='#457b9d', linewidth=1.5,
                linestyle='-', label=f"mR̄ = {limits['mR_bar']:.2f}")
    ax2.axhline(limits["URL"], color='#e63946', linewidth=1.5,
                linestyle='--', label=f"URL = {limits['URL']:.2f}")
    ax2.axhline(0, color='black', linewidth=0.5)

    # Flag mR points above URL
    mr_signals = mR_values > limits["URL"]
    if mr_signals.any():
        ax2.scatter(np.array(dates[1:])[mr_signals], mR_values[mr_signals],
                    color='#e63946', s=80, zorder=5)

    ax2.set_ylabel("Moving Range")
    ax2.legend(fontsize=8, loc='upper left')
    ax2.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

# ── Usage ────────────────────────────────────────────────────────────────────
# fig = plot_xmr(df['date'], df['metric'], metric_name='Weekly Revenue (€)')
# fig.savefig('xmr_chart.png', dpi=150, bbox_inches='tight')
# plt.show()
```

---

## Step 5 — Interpret and Report

Always deliver this summary after generating the chart:

```
Process Average (X̄):    [value]
Upper Natural Limit:     [UNPL]
Lower Natural Limit:     [LNPL]
Average Moving Range:    [mR̄]
Upper Range Limit:       [URL]
Estimated σ:             [sigma]

Signals detected:        [n signals, which rules triggered, which periods]
Interpretation:          [routine variation / exceptional variation detected]
Recommended action:      [investigate signal / continue monitoring / recalculate limits if process changed]
```

### Signal interpretation guide

| Finding | Meaning | Action |
|---------|---------|--------|
| No signals | Routine variation — process is stable | Monitor; don't react to individual points |
| Rule 1 (point outside limits) | Exceptional cause at that moment | Investigate that specific period |
| Rule 2 (8-point run) | Process has shifted to a new level | Recalculate limits from shift point |
| Rule 3 (3/3 in outer third) | Increasing instability | Look for assignable cause |
| Rule 4 (6-point trend) | Gradual drift in process | Investigate slow-moving cause |

---

## Key Principles

- **Never tamper with a stable process** — reacting to routine variation makes things worse
- **XmR limits ≠ specification limits** — they describe what the process does, not what you want it to do
- **Recalculate limits** after a confirmed process change (new baseline from the change point)
- **Need ≥ 10 points** for meaningful limits; 20-30 is better
- **XmR is robust** — it works for non-normal data because it uses mR̄, not σ directly
