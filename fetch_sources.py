#!/usr/bin/env python3
"""
fetch_sources.py — Skill Navigator source updater
==================================================
Fetches live metadata for all third-party skill sources and writes
sources-live.json. Designed to run as a scheduled GitHub Actions job.

What gets auto-updated:
  - GitHub repos: stars, forks, last push date, open issues, SKILL.md count
  - All sources: HTTP reachability check + last verified timestamp
  - Skill counts derived from GitHub tree (count of SKILL.md files)

What stays manual (in MANUAL_OVERRIDES):
  - Trust scores and trust notes (judgment calls)
  - Security notes (require expert review)
  - Vetting status (not inferable from repo stats)
  - Non-GitHub sources (SkillsMP, agentskills.io) — scraping would be fragile

Usage:
    python fetch_sources.py                        # uses anonymous GitHub API (60 req/hr)
    GITHUB_TOKEN=ghp_xxx python fetch_sources.py   # authenticated (5000 req/hr)
    python fetch_sources.py --dry-run              # print without writing
    python fetch_sources.py --out ./docs/sources-live.json

Output: sources-live.json  (loaded by skill-navigator.html at runtime)
"""

import json
import os
import sys
import time
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ── GITHUB SOURCES (auto-fetchable) ───────────────────────────────────────────
# Format: id → GitHub owner/repo  (or None for non-GitHub)

GITHUB_REPOS = {
    "anthropics-skills":    "anthropics/skills",
    "voltagent-awesome":    "VoltAgent/awesome-agent-skills",
    "k-dense-scientific":   "K-Dense-AI/claude-scientific-skills",
    "alirezarezvani":       "alirezarezvani/claude-skills",
    "orchestra-research":   "Orchestra-Research/AI-Research-SKILLs",
    "travisvn-awesome":     "travisvn/awesome-claude-skills",
    "composio-awesome":     "ComposioHQ/awesome-claude-skills",
    "skillmatic-awesome":   "skillmatic-ai/awesome-agent-skills",
    "behisecc-awesome":     "BehiSecc/awesome-claude-skills",
    "glebis-skills":        "glebis/claude-skills",
    # mcollina — no dedicated skills repo, skip GitHub fetch
    # duckdb / vercel — listed via VoltAgent, no standalone repo
}

# Non-GitHub sources — just check URL reachability
URL_ONLY_SOURCES = {
    "agentskills-io":   "https://agentskills.io",
    "skillsmp":         "https://skillsmp.com",
    "lobehub":          "https://lobehub.com/skills",
    "agentskill-sh":    "https://agentskill.sh",
    "skills-sh":        "https://skills.sh",
    "superpowers":      "https://blog.fsck.com/2025/10/09/superpowers/",
    "mcollina-skills":  "https://github.com/mcollina",
    "duckdb-skills":    "https://github.com/duckdb",
    "vercel-skills":    "https://github.com/vercel-labs/agent-skills",
}

# ── MANUAL OVERRIDES ───────────────────────────────────────────────────────────
# These fields are NOT auto-fetched — edit them here when your assessment changes.
# Everything else (stars, skillCount, lastPush, reachable) comes from the API.

MANUAL_OVERRIDES = {
    "anthropics-skills": {
        "trustScore": 5,
        "trustNotes": "Source of truth. Production-grade, maintained by Anthropic engineers. Document skills battle-tested in production.",
        "vettingStatus": "verified",
        "securityNotes": "Safest available. Document skills are proprietary/source-available. No arbitrary code execution in example skills.",
        "installCmd": "/plugin marketplace add anthropics/skills",
        "crossPlatform": True,
    },
    "agentskills-io": {
        "trustScore": 5,
        "trustNotes": "Canonical spec. Use it to validate your own SKILL.md files and understand what any third-party skill can/cannot do.",
        "vettingStatus": "verified",
        "securityNotes": "Governance site, not a skill repo. No security risk.",
        "installCmd": None,
        "crossPlatform": True,
    },
    "voltagent-awesome": {
        "trustScore": 4,
        "trustNotes": "High signal. 'Official dev team' badge means the skill is maintained by the library's own team — meaningful accountability. Best starting point for engineering skills.",
        "vettingStatus": "curated-enterprise",
        "securityNotes": "Official team skills have higher accountability but still review scripts. Community-contributed skills have a lower bar.",
        "installCmd": None,
        "crossPlatform": True,
    },
    "k-dense-scientific": {
        "trustScore": 4,
        "trustNotes": "Best-in-class security posture for a community repo. Cisco scanner on every contribution. Clear distinction between K-Dense-authored vs community skills.",
        "vettingStatus": "security-scanned",
        "securityNotes": "Community contributions less thoroughly reviewed. Run scanner locally: `skill-scanner scan /path/to/skill`. Skills make external DB API calls.",
        "installCmd": "See README — uses uv package manager",
        "crossPlatform": True,
    },
    "skillsmp": {
        "trustScore": 2,
        "trustNotes": "Aggregator, not curator. Almost no individual vetting. Use only as discovery layer — always review the source repo before installing.",
        "vettingStatus": "minimal",
        "securityNotes": "⚠ High risk. Aggregates everything with ≥2 stars. Malicious skills can execute arbitrary code. Always review SKILL.md and scripts.",
        "installCmd": None,
        "crossPlatform": True,
    },
    "lobehub": {
        "trustScore": 3,
        "trustNotes": "Better curation than SkillsMP. LobeHub has a track record in OSS AI tooling. Still community-sourced — verify before production.",
        "vettingStatus": "community-curated",
        "securityNotes": "Provides a skill-vetter skill. Remote skill.md loading is mild supply-chain risk — pin to a commit hash.",
        "installCmd": "Read https://lobehub.com/skills/skill.md",
        "crossPlatform": True,
    },
    "agentskill-sh": {
        "trustScore": 3,
        "trustNotes": "Two-layer scanning adds value over pure aggregators. Still large volume — catches obvious issues but not sophisticated attacks.",
        "vettingStatus": "security-scanned",
        "securityNotes": "Two-layer scan (static + LLM review). Better than nothing. Don't treat a passing scan as a green light.",
        "installCmd": None,
        "crossPlatform": True,
    },
    "skills-sh": {
        "trustScore": 2,
        "trustNotes": "Popularity ≠ safety. Use as discovery only.",
        "vettingStatus": "minimal",
        "securityNotes": "No explicit security scanning mentioned. Treat like SkillsMP.",
        "installCmd": None,
        "crossPlatform": True,
    },
    "alirezarezvani": {
        "trustScore": 3,
        "trustNotes": "High stars = community validation, not security audit. Stdlib-only Python is a meaningful plus — no pip supply chain risk. Broad scope means quality varies.",
        "vettingStatus": "community-popular",
        "securityNotes": "Stdlib-only Python tools are safer. Still review SKILL.md before production. Compliance skills: validate against actual regulatory requirements.",
        "installCmd": "git clone https://github.com/alirezarezvani/claude-skills.git && ./scripts/install.sh",
        "crossPlatform": True,
    },
    "orchestra-research": {
        "trustScore": 3,
        "trustNotes": "Highly specialised. Quality high within ML research domain. Autoresearch skill makes autonomous network requests — review carefully.",
        "vettingStatus": "community-curated",
        "securityNotes": "Installs GPU-heavy ML packages. Autoresearch makes external web requests. Run in isolated environment first.",
        "installCmd": "npx @orchestra-research/ai-research-skills",
        "crossPlatform": True,
    },
    "travisvn-awesome": {
        "trustScore": 3,
        "trustNotes": "Good starting list for Claude-specific skills. Active maintenance. Honest risk disclosure.",
        "vettingStatus": "community-curated",
        "securityNotes": "Lists Superpowers experimental lab skills separately — good practice.",
        "installCmd": "/plugin marketplace add obra/superpowers-marketplace",
        "crossPlatform": False,
    },
    "composio-awesome": {
        "trustScore": 3,
        "trustNotes": "Composio has a legitimate product. Action skills introduce OAuth flows — additional trust surface.",
        "vettingStatus": "vendor-curated",
        "securityNotes": "Action skills send data to external APIs. Check Composio data retention policy.",
        "installCmd": None,
        "crossPlatform": True,
    },
    "skillmatic-awesome": {
        "trustScore": 3,
        "trustNotes": "Meta-list, not a skill collection. High value for orientation and ecosystem mapping.",
        "vettingStatus": "community-curated",
        "securityNotes": "Links to external resources — apply normal web hygiene.",
        "installCmd": None,
        "crossPlatform": True,
    },
    "behisecc-awesome": {
        "trustScore": 3,
        "trustNotes": "Security skills are high-stakes — VibeSec appears well-regarded. DNA/health skills touch sensitive data.",
        "vettingStatus": "community-curated",
        "securityNotes": "DNA/health skills process sensitive personal data. Review data handling carefully.",
        "installCmd": None,
        "crossPlatform": True,
    },
    "glebis-skills": {
        "trustScore": 3,
        "trustNotes": "Niche but high-quality within consulting/knowledge-management. Single author — maintenance depends on one person.",
        "vettingStatus": "personal-maintained",
        "securityNotes": "NotebookLM skill uses notebooklm-py — review API key handling. Obsidian integration reads local vault files.",
        "installCmd": "Manual — copy skill folders to ~/.claude/skills/",
        "crossPlatform": False,
    },
    "superpowers": {
        "trustScore": 3,
        "trustNotes": "Jesse Vincent is trusted in OSS. Lab skills explicitly warned as experimental. Community-editable = variability. Pin to specific commits.",
        "vettingStatus": "community-curated",
        "securityNotes": "Community-editable repo = supply chain risk. Lab skills may break. Not for production without pinning.",
        "installCmd": "/plugin marketplace add obra/superpowers-marketplace",
        "crossPlatform": False,
    },
    "mcollina-skills": {
        "trustScore": 4,
        "trustNotes": "Author has exceptional domain credibility — skills about tools he maintains. High signal for Node.js/Fastify ecosystem work.",
        "vettingStatus": "expert-authored",
        "securityNotes": "Low risk — instruction-only skills from a trusted OSS maintainer.",
        "installCmd": "Manual — see repo",
        "crossPlatform": True,
    },
    "duckdb-skills": {
        "trustScore": 5,
        "trustNotes": "Maintained by the DuckDB team — maximum domain authority.",
        "vettingStatus": "vendor-official",
        "securityNotes": "DuckDB can read arbitrary local files and remote storage. Standard DuckDB security considerations apply.",
        "installCmd": "See VoltAgent/awesome-agent-skills for install path",
        "crossPlatform": True,
    },
    "vercel-skills": {
        "trustScore": 5,
        "trustNotes": "Vercel Labs maintaining their own skills is a strong trust signal. Reflects Vercel's own best practices.",
        "vettingStatus": "vendor-official",
        "securityNotes": "Skills deploy to Vercel infrastructure — ensure secrets are not embedded in SKILL.md.",
        "installCmd": "npx skills add vercel-labs/agent-skills",
        "crossPlatform": True,
    },
}

# ── HTTP HELPERS ───────────────────────────────────────────────────────────────

def github_headers():
    token = os.environ.get("GITHUB_TOKEN")
    h = {"Accept": "application/vnd.github+json", "User-Agent": "delafuente-skill-navigator/1.0"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

def fetch_json(url, headers=None, timeout=10):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode()), r.status
    except urllib.error.HTTPError as e:
        return None, e.code
    except Exception:
        return None, 0

def check_reachable(url, timeout=8):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "delafuente-skill-navigator/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status < 400
    except Exception:
        return False

def count_skill_files(owner_repo, headers, delay=0.5):
    """Count SKILL.md files in a repo via the Git trees API."""
    url = f"https://api.github.com/repos/{owner_repo}/git/trees/HEAD?recursive=1"
    data, status = fetch_json(url, headers)
    if not data or status != 200:
        return None
    tree = data.get("tree", [])
    count = sum(1 for f in tree if f.get("path", "").endswith("SKILL.md"))
    time.sleep(delay)
    return count if count > 0 else None

# ── MAIN FETCH ─────────────────────────────────────────────────────────────────

def fetch_github_source(source_id, owner_repo, headers):
    print(f"  → GitHub: {owner_repo}", end=" ", flush=True)
    api_url = f"https://api.github.com/repos/{owner_repo}"
    data, status = fetch_json(api_url, headers)

    result = {"id": source_id, "fetchedAt": now_iso(), "reachable": True}

    if data and status == 200:
        result["stars"]     = data.get("stargazers_count")
        result["forks"]     = data.get("forks_count")
        result["openIssues"]= data.get("open_issues_count")
        result["lastPush"]  = data.get("pushed_at", "")[:10]   # YYYY-MM-DD
        result["archived"]  = data.get("archived", False)
        result["description"]= data.get("description", "")
        result["htmlUrl"]   = data.get("html_url", f"https://github.com/{owner_repo}")

        # Count actual SKILL.md files
        skill_count = count_skill_files(owner_repo, headers)
        if skill_count:
            result["skillCount"] = f"{skill_count}"
        print(f"★{result['stars']} | {result.get('skillCount','?')} skills | pushed {result['lastPush']}")
    else:
        result["reachable"] = (status not in (0, 404))
        print(f"HTTP {status}")

    return result

def fetch_url_source(source_id, url):
    print(f"  → URL check: {url}", end=" ", flush=True)
    reachable = check_reachable(url)
    print("✓" if reachable else "✗ UNREACHABLE")
    return {
        "id": source_id,
        "fetchedAt": now_iso(),
        "reachable": reachable,
        "htmlUrl": url,
    }

def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

# ── STALENESS DETECTION ────────────────────────────────────────────────────────

def staleness_flag(last_push_str):
    """Flag repos that haven't been pushed to in >6 months."""
    if not last_push_str:
        return None
    try:
        last = datetime.strptime(last_push_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        days = (datetime.now(timezone.utc) - last).days
        if days > 365: return "stale-1y"
        if days > 180: return "stale-6m"
        return None
    except Exception:
        return None

# ── ENTRY POINT ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fetch live skill source metadata")
    parser.add_argument("--out", default="sources-live.json", help="Output JSON path")
    parser.add_argument("--dry-run", action="store_true", help="Print without writing")
    parser.add_argument("--delay", type=float, default=0.8, help="Delay between GitHub API calls (seconds)")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    print(f"{'Authenticated' if token else 'Anonymous'} GitHub API ({5000 if token else 60} req/hr limit)")
    print(f"Fetching {len(GITHUB_REPOS)} GitHub repos + {len(URL_ONLY_SOURCES)} URL checks\n")

    headers = github_headers()
    live_data = {}

    # ── GitHub repos
    print("── GitHub Repos ──────────────────────────────────")
    for source_id, owner_repo in GITHUB_REPOS.items():
        result = fetch_github_source(source_id, owner_repo, headers)
        # Merge manual overrides
        result.update(MANUAL_OVERRIDES.get(source_id, {}))
        # Add staleness flag
        stale = staleness_flag(result.get("lastPush"))
        if stale:
            result["stalenessFlag"] = stale
            print(f"    ⚠ {stale}: last push {result['lastPush']}")
        live_data[source_id] = result
        time.sleep(args.delay)

    # ── URL-only sources
    print("\n── URL Checks ────────────────────────────────────")
    for source_id, url in URL_ONLY_SOURCES.items():
        result = fetch_url_source(source_id, url)
        result.update(MANUAL_OVERRIDES.get(source_id, {}))
        live_data[source_id] = result

    # ── Summary
    unreachable = [sid for sid, d in live_data.items() if not d.get("reachable", True)]
    stale_repos = [sid for sid, d in live_data.items() if d.get("stalenessFlag")]

    print(f"\n── Summary ───────────────────────────────────────")
    print(f"  Sources fetched:  {len(live_data)}")
    print(f"  Unreachable:      {len(unreachable)}{' → ' + ', '.join(unreachable) if unreachable else ''}")
    print(f"  Stale repos:      {len(stale_repos)}{' → ' + ', '.join(stale_repos) if stale_repos else ''}")
    print(f"  Generated at:     {now_iso()}")

    output = {
        "_meta": {
            "generatedAt": now_iso(),
            "sourceCount": len(live_data),
            "unreachable": unreachable,
            "staleRepos": stale_repos,
        },
        "sources": live_data,
    }

    if args.dry_run:
        print("\n── Output (dry run) ──────────────────────────────")
        print(json.dumps(output, indent=2))
    else:
        out_path = Path(args.out)
        out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
        print(f"\n  ✓ Written to {out_path.resolve()}")

if __name__ == "__main__":
    main()
