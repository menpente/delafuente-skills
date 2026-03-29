# Repo Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make delafuente-skills look professional on GitHub for both Claude users and employers/clients via quick hygiene fixes.

**Architecture:** Three file changes — create `LICENSE`, rewrite `README.md`, delete `devops/`. No new skills, no CI, no tests. All changes committed individually.

**Tech Stack:** Markdown, MIT license text, git

---

## File Map

| Action | Path | What changes |
|--------|------|-------------|
| Create | `LICENSE` | MIT license text |
| Modify | `README.md` | Badges, remove language section, remove devops from tree, improve Usage |
| Delete | `devops/` | Empty folder removed from repo |

---

### Task 1: Add LICENSE file

**Files:**
- Create: `LICENSE`

- [ ] **Step 1: Create the LICENSE file**

Create `LICENSE` at the repo root with this exact content:

```
MIT License

Copyright (c) 2026 Ruben de la Fuente

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 2: Verify file exists**

Run: `ls -la LICENSE`
Expected: file listed at repo root

- [ ] **Step 3: Commit**

```bash
git add LICENSE
git commit -m "chore: add MIT LICENSE file"
```

---

### Task 2: Add badge row to README header

**Files:**
- Modify: `README.md` lines 1-4

- [ ] **Step 1: Replace the README header block**

Find this exact text in `README.md` (lines 1–4):

```markdown
# delafuente-skills

Claude skill library for data science, DevOps, and communications work.
Built and maintained by [Ruben de la Fuente](https://delafuente.ai).
```

Replace with:

```markdown
# delafuente-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-11-blue)](#skills)
[![Built with Claude](https://img.shields.io/badge/built%20with-Claude-blueviolet)](https://claude.ai)
[![delafuente.ai](https://img.shields.io/badge/web-delafuente.ai-lightgrey)](https://delafuente.ai)

Claude skill library for data science, DevOps, and communications work.
Built and maintained by [Ruben de la Fuente](https://delafuente.ai).
```

- [ ] **Step 2: Verify badges render correctly**

Run: `head -10 README.md`
Expected: heading, 4 badge lines, blank line, tagline

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add badge row to README header"
```

---

### Task 3: Remove language section and devops from README structure

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update the Structure folder tree**

Find this block in `README.md`:

```
delafuente-skills/
├── data/                        # Statistical analysis and data visualization
│   ├── statistical-test-selector/
│   ├── quasi-experimental-design/
│   ├── xmr-chart/
│   └── 6-12-chart/
├── comms/                       # Content creation and presentation
│   ├── linkedin-post-creator/
│   └── slidestart-pptx/
├── strategy/                    # Business strategy and planning
│   └── csf-identifier/
├── devops/                      # DevOps and MLOps (in progress)
└── language/                    # Linguistics and legal language tools
    └── constitucion-espanola-validador/
```

Replace with:

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

- [ ] **Step 2: Remove the Language skills section**

Find and delete this block (lines 104–111):

```markdown
### 🏛️ Language

#### `constitucion-espanola-validador`
Validates rewrites of the Spanish Constitution in plain language. Detects changes in fundamental rights, constitutional procedures, normative hierarchies, and competences. Generates side-by-side comparisons with issue classification (critical / moderate / minor).

**Triggers:** plain language rewrite of constitutional articles, legal language validation in Spanish

---
```

- [ ] **Step 3: Verify README no longer mentions language or constitucion**

Run: `grep -n "language\|constitucion\|devops" README.md`
Expected: no matches (or only in Roadmap section where devops skills are listed as upcoming)

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: remove language section and devops folder from README structure"
```

---

### Task 4: Improve Usage section

**Files:**
- Modify: `README.md` lines 129–133

- [ ] **Step 1: Replace the Usage section**

Find this block:

```markdown
## Usage

1. Copy the desired skill folder into `/mnt/skills/user/` in your Claude environment
2. Claude will automatically detect and use the skill based on your request
3. You can also explicitly ask: *"Use the xmr-chart skill to..."*
```

Replace with:

```markdown
## Usage

### Install a skill

```bash
git clone https://github.com/rubendelafuente/delafuente-skills.git
cp -r delafuente-skills/data/xmr-chart /mnt/skills/user/
```

Skills live in `/mnt/skills/user/` in the Claude environment. Once copied, Claude detects and applies them automatically based on your request.

### Invoke explicitly

> "Use the xmr-chart skill to plot this time series data."

You can always name a skill explicitly if Claude doesn't auto-trigger it.
```

- [ ] **Step 2: Verify section looks right**

Run: `grep -A 20 "^## Usage" README.md`
Expected: clone command, cp command, explanation paragraph, explicit invocation example

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: improve Usage section with quickstart and explicit invocation example"
```

---

### Task 5: Remove empty devops/ folder

**Files:**
- Delete: `devops/` directory

- [ ] **Step 1: Check what's in devops/**

Run: `find devops/ -type f`
Expected: no output (folder is empty or contains only a placeholder)

- [ ] **Step 2: Remove the folder from git tracking**

```bash
git rm -r devops/
```

Expected output: `rm 'devops/...'` or nothing if already untracked

- [ ] **Step 3: If devops/ only had untracked files, delete manually**

```bash
rm -rf devops/
```

- [ ] **Step 4: Verify devops/ is gone**

Run: `ls`
Expected: `comms  data  docs  language  README.md  LICENSE  strategy` — no `devops`

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "chore: remove empty devops/ folder"
```
