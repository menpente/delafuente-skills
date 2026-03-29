---
name: linear-programming
description: >
  Formulates and solves linear programming (LP) problems from plain-language
  problem statements. Handles LP, Integer Programming (IP), Mixed-Integer
  Programming (MIP), and multi-objective problems. Extracts decision variables,
  objective function, and constraints from prose; solves using PuLP or SciPy;
  and delivers a full solution with sensitivity analysis and plain-language
  interpretation. Trigger when the user mentions "linear programming", "LP",
  "optimize", "maximize", "minimize", "subject to constraints", "resource
  allocation", "scheduling problem", "blending problem", "transportation
  problem", "assignment problem", or describes a problem with limited
  resources and a goal to optimize.
language: python
libraries: [pulp, scipy, pandas, numpy]
---

# Linear Programming Skill

## Overview

Linear programming finds the best outcome (maximum profit, minimum cost,
optimal allocation) given a set of linear constraints. This skill:

1. Extracts the mathematical model from a plain-language problem
2. Formulates it correctly (LP, IP, or MIP)
3. Solves it with PuLP (primary) or SciPy (fallback)
4. Delivers the solution, sensitivity analysis, and interpretation

---

## Step 1 — Extract the Mathematical Model

Parse the problem statement into four components:

### 1. Decision variables
What quantities are we choosing? Name them clearly.
- "How many units of product A and B to produce?" → x_A, x_B ≥ 0
- "Which workers to assign to which shifts?" → x_ij ∈ {0, 1}

### 2. Objective function
What are we optimizing, and in which direction?
- Maximizing: profit, revenue, throughput, utilization
- Minimizing: cost, waste, time, distance

Write as: `maximize/minimize c₁x₁ + c₂x₂ + ... + cₙxₙ`

### 3. Constraints
What limits apply? Express each as a linear inequality or equality.
- Resource limits: `a₁x₁ + a₂x₂ ≤ b` (can't exceed available capacity)
- Demand requirements: `x₁ ≥ d` (must meet minimum demand)
- Balance equations: `x_in = x_out` (flow conservation)
- Logical constraints: `x_ij ∈ {0,1}` (binary decisions)

### 4. Variable bounds and integrality
- Non-negativity: all variables ≥ 0 (default)
- Upper bounds: `x ≤ max_capacity`
- Integer requirement: if variables must be whole numbers → IP/MIP
- Binary: if variables are yes/no decisions → x ∈ {0, 1}

### Problem type classification

| Type | When | Solver |
|------|------|--------|
| **LP** (Linear Program) | All variables continuous | PuLP / scipy.optimize.linprog |
| **IP** (Integer Program) | All variables integer | PuLP with CBC |
| **MIP** (Mixed-Integer) | Some integer, some continuous | PuLP with CBC |
| **Binary** | Yes/no decisions | PuLP with CBC, var cat='Binary' |
| **Multi-objective** | Two competing objectives | Weighted sum or ε-constraint |

---

## Step 2 — Formulate and Solve with PuLP

Always use PuLP as primary solver. Fall back to `scipy.optimize.linprog`
only for pure LP when PuLP is unavailable.

```python
import pulp
import pandas as pd

# ── 1. Define the problem ─────────────────────────────────────────────────
prob = pulp.LpProblem("problem_name", pulp.LpMaximize)  # or LpMinimize

# ── 2. Decision variables ─────────────────────────────────────────────────
# Continuous (LP)
x = pulp.LpVariable("x", lowBound=0)
y = pulp.LpVariable("y", lowBound=0)

# Integer (IP)
x_int = pulp.LpVariable("x_int", lowBound=0, cat='Integer')

# Binary (yes/no)
x_bin = pulp.LpVariable("x_bin", cat='Binary')

# Dict of variables (for indexed problems)
products = ['A', 'B', 'C']
units = pulp.LpVariable.dicts("units", products, lowBound=0)

# ── 3. Objective function ─────────────────────────────────────────────────
prob += 5 * x + 4 * y, "Objective"

# ── 4. Constraints ────────────────────────────────────────────────────────
prob += 6 * x + 4 * y <= 24, "Resource_1"
prob += x + 2 * y <= 6,      "Resource_2"

# ── 5. Solve ──────────────────────────────────────────────────────────────
status = prob.solve(pulp.PULP_CBC_CMD(msg=0))

print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Objective value: {pulp.value(prob.objective):.4f}")
for v in prob.variables():
    print(f"  {v.name} = {v.varValue:.4f}")
```

---

## Step 3 — Sensitivity Analysis

Always include sensitivity analysis for LP problems. It answers:
- **Shadow prices**: how much does the objective improve if we relax a
  constraint by 1 unit? (value of additional resources)
- **Reduced costs**: how much would the objective coefficient need to change
  before a non-basic variable enters the solution?
- **Ranging**: over what range can coefficients change without changing the
  optimal basis?

```python
# Shadow prices and slack after solving
print("\nSensitivity Analysis:")
print("-" * 50)
for name, constraint in prob.constraints.items():
    shadow_price = constraint.pi          # dual value / shadow price
    slack = constraint.slack              # unused capacity (0 = binding)
    status = "BINDING" if abs(slack) < 1e-6 else f"slack={slack:.3f}"
    print(f"  {name}: shadow price={shadow_price:.4f}, {status}")

# Reduced costs
print("\nReduced Costs:")
for v in prob.variables():
    print(f"  {v.name}: reduced cost = {v.dj:.4f}")
```

**Interpretation guide:**
- Shadow price = 0 → constraint is non-binding (has slack); relaxing it
  doesn't help
- Shadow price > 0 (maximization) → constraint is binding; worth relaxing
- Shadow price = X → adding 1 more unit of this resource improves
  objective by X
- Reduced cost = 0 → variable is in the optimal solution (basic)
- Reduced cost < 0 (maximization) → variable not in solution; profit
  coefficient would need to increase by |reduced cost| for it to enter

---

## Step 4 — SciPy Fallback (Pure LP only)

```python
from scipy.optimize import linprog
import numpy as np

# NOTE: scipy minimizes by default — negate coefficients to maximize
# min c·x  subject to  A_ub·x ≤ b_ub,  A_eq·x = b_eq,  bounds

c = [-5, -4]           # negate for maximization
A_ub = [[6, 4],
        [1, 2]]
b_ub = [24, 6]
bounds = [(0, None), (0, None)]

result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

print(f"Status: {result.message}")
print(f"Optimal value: {-result.fun:.4f}")   # negate back
print(f"Solution: x={result.x[0]:.4f}, y={result.x[1]:.4f}")
# Sensitivity via result.ineqlin.marginals (shadow prices)
print(f"Shadow prices: {result.ineqlin.marginals}")
```

---

## Step 5 — Common Problem Templates

### Production mix (maximize profit)
> "Produce products A and B. Each unit of A requires 2h labor and 1kg
> material; B requires 1h and 3kg. Available: 100h labor, 150kg material.
> Profit: €5/A, €4/B. How many of each to produce?"

```python
prob = pulp.LpProblem("production_mix", pulp.LpMaximize)
A = pulp.LpVariable("A", lowBound=0)
B = pulp.LpVariable("B", lowBound=0)
prob += 5*A + 4*B                     # maximize profit
prob += 2*A + 1*B <= 100              # labor constraint
prob += 1*A + 3*B <= 150              # material constraint
```

### Transportation (minimize cost)
> "Ship goods from 2 warehouses to 3 customers. Given supply, demand,
> and cost per unit shipped."

```python
prob = pulp.LpProblem("transportation", pulp.LpMinimize)
routes = [(i,j) for i in warehouses for j in customers]
x = pulp.LpVariable.dicts("ship", routes, lowBound=0)
prob += pulp.lpSum(cost[i][j] * x[(i,j)] for i,j in routes)
for i in warehouses:
    prob += pulp.lpSum(x[(i,j)] for j in customers) <= supply[i]
for j in customers:
    prob += pulp.lpSum(x[(i,j)] for i in warehouses) >= demand[j]
```

### Assignment (minimize cost, binary)
> "Assign n workers to n tasks, one-to-one, minimizing total cost."

```python
prob = pulp.LpProblem("assignment", pulp.LpMinimize)
x = pulp.LpVariable.dicts("assign", [(i,j) for i in workers
                           for j in tasks], cat='Binary')
prob += pulp.lpSum(cost[i][j] * x[(i,j)] for i in workers for j in tasks)
for i in workers:
    prob += pulp.lpSum(x[(i,j)] for j in tasks) == 1   # each worker assigned once
for j in tasks:
    prob += pulp.lpSum(x[(i,j)] for i in workers) == 1  # each task covered once
```

### Blending (minimize cost, meet specs)
> "Blend ingredients to meet minimum nutritional requirements at minimum cost."

```python
prob = pulp.LpProblem("blending", pulp.LpMinimize)
x = pulp.LpVariable.dicts("ingredient", ingredients, lowBound=0)
prob += pulp.lpSum(cost[i] * x[i] for i in ingredients)
for nutrient in nutrients:
    prob += pulp.lpSum(content[i][nutrient] * x[i]
                       for i in ingredients) >= requirement[nutrient]
prob += pulp.lpSum(x[i] for i in ingredients) == 1   # proportions sum to 1
```

---

## Output Format

Always deliver in this order:

### 1. Mathematical formulation (before code)
Write the model in clean mathematical notation:
```
Maximize:   5x₁ + 4x₂
Subject to: 6x₁ + 4x₂ ≤ 24
            x₁ + 2x₂ ≤ 6
            x₁, x₂ ≥ 0
```

### 2. Complete Python solution (ready to run)
Full self-contained script with data, model, solve, and print statements.
Include `pip install pulp` comment if PuLP is needed.

### 3. Solution table
| Variable | Value | Interpretation |
|----------|-------|----------------|
| x₁ | 3.0 | Produce 3 units of Product A |
| x₂ | 1.5 | Produce 1.5 units of Product B |
| **Objective** | **21.0** | **Maximum profit: €21** |

### 4. Sensitivity analysis table
| Constraint | Shadow Price | Slack | Status |
|-----------|-------------|-------|--------|
| Labor | 0.75 | 0 | Binding — worth relaxing |
| Material | 0 | 12 | Non-binding — not a bottleneck |

### 5. Plain-language interpretation
3–5 sentences explaining:
- What the optimal solution says in business terms
- Which constraints are bottlenecks (binding) and worth investing in
- What the shadow prices mean concretely ("one more hour of labor is worth €0.75")
- Any caveats (integrality gaps, model assumptions, sensitivity)

---

## Key Rules

- **Always write the mathematical formulation first** — it forces clarity
  and catches errors before coding
- **Label every constraint** — unnamed constraints make sensitivity analysis
  unreadable
- **Check feasibility first** — if `status != 'Optimal'`, report whether the
  problem is infeasible (contradictory constraints) or unbounded (missing
  upper bounds)
- **Integer problems have no shadow prices** — sensitivity analysis only
  applies to continuous LP relaxations
- **Validate with a manual check** — plug the solution back into each
  constraint and verify it satisfies them
- **Flag modeling assumptions** — linearity assumes constant returns to scale;
  flag if the real problem has nonlinear elements (volume discounts, setup
  costs) that LP can't capture directly
