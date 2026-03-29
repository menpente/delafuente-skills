---
name: repo-polish
description: Quick-win polish pass to make delafuente-skills look professional on GitHub for both Claude users and employers/clients
type: project
---

# Repo Polish — Design Spec

**Date:** 2026-03-29
**Scope:** Quick wins (~30 min). No new skills, no CI, no tests.
**Audiences:** Claude users installing skills + employers/clients evaluating credibility.

---

## Goals

1. Fix broken references left by the removed `language/` skill
2. Add a proper `LICENSE` file so GitHub shows the license badge
3. Add a badge row to the README header for instant credibility signals
4. Improve the Usage/Quickstart section so visitors know how to actually use skills
5. Remove the empty `devops/` folder which signals abandoned intent

---

## Changes

### 1. `LICENSE` file

- Add `LICENSE` at repo root with standard MIT license text
- Author: Ruben de la Fuente, year 2026

### 2. README — Badge row

Insert immediately after the `# delafuente-skills` heading and tagline:

```
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-11-blue)](#skills)
[![Built with Claude](https://img.shields.io/badge/built%20with-Claude-blueviolet)](https://claude.ai)
[![delafuente.ai](https://img.shields.io/badge/web-delafuente.ai-lightgrey)](https://delafuente.ai)
```

### 3. README — Remove language section

- Remove `language/constitucion-espanola-validador` from the Structure diagram
- Remove `language/` row from the folder tree
- Remove the `### Language` section and its skill entry from the Skills list

### 4. README — Improve Usage section

Replace the current stub with:

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

### 5. Remove empty `devops/` folder

- Delete `devops/` from the repo (it contains no skills)
- Remove `devops/` from the Structure diagram and folder tree in the README
- Move `devops/dora-metrics` and `devops/incident-postmortem` roadmap items to a `## Roadmap` section that's clearly marked as upcoming

---

## Out of Scope

- CI/CD workflows
- CONTRIBUTING.md
- Example outputs or demo GIFs
- New skills
