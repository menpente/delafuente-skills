---
name: 6-12-chart
description: >
  Creates a 6-12 chart (also called a month-over-month rolling comparison
  chart or YTD vs prior year chart). Shows the last 12 months of a metric
  alongside the previous 12 months on the same axis, making seasonality and
  year-over-year trends immediately visible. Trigger when user asks for a
  "6-12 chart", "year-over-year comparison", "YoY trend chart", "current year
  vs last year", "rolling 12 month comparison", "same period last year",
  "monthly trend with prior year overlay", or wants to visualize seasonal
  performance. Output: Python chart + summary table.
language: python
libraries: [pandas, numpy, matplotlib]
---

# 6-12 Chart Skill

## Overview

A 6-12 chart plots **two consecutive 12-month windows** on the same time
axis so you can see:
- How current performance compares to the same period last year
- Whether a trend is a genuine shift or just seasonality repeating
- Month-over-month changes within each year

The name "6-12" comes from the layout: 6 months back + current month +
6 months forward, but the standard implementation covers the full 12 vs 12
comparison.

---

## Step 1 — Gather Context

| # | Question | Why it matters |
|---|----------|----------------|
| 1 | What is the metric? (revenue, signups, churn rate...) | Labels and formatting |
| 2 | What is the granularity? (daily, weekly, monthly) | Aggregation logic |
| 3 | How many periods of history are available? | Need ≥ 24 months for full 12v12 |
| 4 | Should the chart show absolute values or % change? | Display choice |
| 5 | Is there a target or budget line to overlay? | Optional reference line |
| 6 | Should the chart highlight the YoY delta? | Optional delta bar/annotation |

---

## Step 2 — Prepare Data

```python
import pandas as pd
import numpy as np

def prepare_6_12_data(df, date_col, value_col, freq='MS'):
    """
    Prepare data for a 6-12 chart.
    
    Parameters
    ----------
    df : DataFrame with date and value columns
    date_col : str — name of the date column
    value_col : str — name of the metric column
    freq : str — 'MS' (month start), 'W' (weekly), 'D' (daily)
    
    Returns
    -------
    DataFrame with columns: period, current_year, prior_year, yoy_change, yoy_pct
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col).resample(freq)[value_col].sum().reset_index()
    df = df.sort_values(date_col).reset_index(drop=True)
    
    # Get last 24 periods
    df = df.tail(24).reset_index(drop=True)
    
    if len(df) < 24:
        raise ValueError(f"Need at least 24 periods. Got {len(df)}.")
    
    prior_year  = df.iloc[:12].reset_index(drop=True)
    current_year = df.iloc[12:].reset_index(drop=True)
    
    result = pd.DataFrame({
        'period':       current_year[date_col].dt.strftime('%b'),
        'period_date':  current_year[date_col],
        'current_year': current_year[value_col].values,
        'prior_year':   prior_year[value_col].values,
    })
    result['yoy_change'] = result['current_year'] - result['prior_year']
    result['yoy_pct'] = (result['yoy_change'] / result['prior_year'] * 100).round(1)
    
    return result
```

---

## Step 3 — Plot

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def plot_6_12(data, metric_name="Metric", value_format=None,
              target=None, show_delta=True, current_label=None, prior_label=None):
    """
    Plot a 6-12 comparison chart.
    
    Parameters
    ----------
    data : DataFrame from prepare_6_12_data()
    metric_name : str — chart title label
    value_format : callable — e.g. lambda x: f'€{x/1e3:.0f}k' for formatting
    target : float — optional horizontal target/budget line
    show_delta : bool — show YoY delta bars below the main chart
    current_label : str — legend label for current period (default: current year)
    prior_label : str — legend label for prior period
    """
    current_year_label = current_label or str(data['period_date'].dt.year.iloc[-1])
    prior_year_label   = prior_label   or str(data['period_date'].dt.year.iloc[-1] - 1)
    
    if show_delta:
        fig, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(14, 9),
            gridspec_kw={'height_ratios': [3, 1]},
            sharex=True
        )
    else:
        fig, ax1 = plt.subplots(figsize=(14, 6))
        ax2 = None

    months = data['period']
    x = np.arange(len(months))
    width = 0.35

    # ── Main chart ────────────────────────────────────────────
    bars_current = ax1.bar(
        x + width/2, data['current_year'], width,
        label=current_year_label, color='#1d3557', alpha=0.85, zorder=3
    )
    bars_prior = ax1.bar(
        x - width/2, data['prior_year'], width,
        label=prior_year_label, color='#a8c8e8', alpha=0.75, zorder=3
    )
    
    # Line connecting current year bars for trend visibility
    ax1.plot(x + width/2, data['current_year'], 'o-',
             color='#e63946', linewidth=1.5, markersize=4, zorder=4)

    # Target line
    if target is not None:
        ax1.axhline(target, color='#2a9d8f', linewidth=1.5,
                    linestyle='--', label=f'Target: {target:,.0f}', zorder=5)

    # Value labels on current year bars
    if value_format:
        for bar in bars_current:
            h = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2, h * 1.01,
                     value_format(h), ha='center', va='bottom',
                     fontsize=8, color='#1d3557', fontweight='bold')

    ax1.set_title(f'{metric_name} — Year-over-Year Comparison',
                  fontsize=13, fontweight='bold', pad=12)
    ax1.set_ylabel(metric_name)
    ax1.legend(fontsize=9)
    ax1.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: value_format(x) if value_format else f'{x:,.0f}')
    )
    ax1.grid(axis='y', alpha=0.3, zorder=0)
    ax1.set_xticks(x)
    ax1.set_xticklabels(months)

    # ── Delta chart ───────────────────────────────────────────
    if show_delta and ax2 is not None:
        colors = ['#2a9d8f' if v >= 0 else '#e63946' for v in data['yoy_change']]
        ax2.bar(x, data['yoy_change'], color=colors, alpha=0.8, zorder=3)
        ax2.axhline(0, color='black', linewidth=0.8)

        for i, (val, pct) in enumerate(zip(data['yoy_change'], data['yoy_pct'])):
            label = f'{pct:+.1f}%'
            y_pos = val + (abs(val) * 0.05 * np.sign(val))
            ax2.text(i, y_pos, label, ha='center',
                     va='bottom' if val >= 0 else 'top',
                     fontsize=7.5, color='#333')

        ax2.set_ylabel('YoY Δ')
        ax2.grid(axis='y', alpha=0.3)

    plt.xticks(x, months, rotation=0)
    plt.tight_layout()
    return fig
```

---

## Step 4 — Summary Table

Always include a summary table with the chart:

```python
def summary_table(data, value_format=None):
    """Print a summary table for the 6-12 chart data."""
    fmt = value_format or (lambda x: f'{x:,.0f}')
    
    rows = []
    for _, row in data.iterrows():
        rows.append({
            'Month': row['period'],
            'Current': fmt(row['current_year']),
            'Prior':   fmt(row['prior_year']),
            'YoY Δ':   fmt(row['yoy_change']),
            'YoY %':   f"{row['yoy_pct']:+.1f}%",
        })
    
    summary_df = pd.DataFrame(rows)
    
    # Totals row
    totals = {
        'Month': 'TOTAL / AVG',
        'Current': fmt(data['current_year'].sum()),
        'Prior':   fmt(data['prior_year'].sum()),
        'YoY Δ':   fmt(data['yoy_change'].sum()),
        'YoY %':   f"{(data['yoy_change'].sum() / data['prior_year'].sum() * 100):+.1f}%",
    }
    summary_df = pd.concat([summary_df, pd.DataFrame([totals])], ignore_index=True)
    
    return summary_df
```

---

## Step 5 — Full Usage Example

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Example: generate 24 months of synthetic revenue data
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=24, freq='MS')
base = 100_000
seasonality = np.tile([0.8, 0.85, 1.0, 1.1, 1.15, 1.2,
                        1.3, 1.25, 1.1, 1.05, 0.95, 1.4], 2)
growth = np.linspace(1.0, 1.15, 24)  # 15% annual growth
values = base * seasonality * growth * (1 + np.random.normal(0, 0.04, 24))

df = pd.DataFrame({'date': dates, 'revenue': values})

# Prepare and plot
data = prepare_6_12_data(df, 'date', 'revenue')
fmt = lambda x: f'€{x/1e3:.0f}k'

fig = plot_6_12(
    data,
    metric_name='Monthly Revenue',
    value_format=fmt,
    target=120_000,
    show_delta=True,
    current_label='2025',
    prior_label='2024',
)
fig.savefig('6_12_chart.png', dpi=150, bbox_inches='tight')
plt.show()

# Summary table
print(summary_table(data, value_format=fmt).to_string(index=False))
```

---

## Key Interpretation Rules

| Pattern | Interpretation |
|---------|----------------|
| Both lines move together | Seasonality — check if growth trend is improving |
| Current year consistently above prior | Genuine YoY growth |
| Current year dips below prior in specific months | Investigate those months specifically |
| Delta bars all positive but shrinking | Growth is decelerating |
| Single month outlier in delta | One-off event — annotate and investigate |
| Current year flat, prior year rising | Regression to mean or structural decline |

---

## Variants

- **Rolling 12-month total overlay**: plot cumulative sum over time alongside prior year cumulative — useful for YTD tracking
- **Weekly 6-12**: same logic, 52-week windows instead of 12-month
- **Multi-metric**: small multiples of the same chart for different KPIs
- **% change only**: replace bar chart with a single line of YoY % change and a zero reference line
