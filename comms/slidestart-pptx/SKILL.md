---
name: slidestart-pptx
description: "Create professional consulting-grade PowerPoint presentations inspired by top-tier firms (McKinsey, BCG, Bain). Use this skill whenever the user wants to create a business presentation, pitch deck, strategy deck, consulting deliverable, executive report, or any professional slide deck. Trigger when the user mentions 'consulting slides', 'McKinsey style', 'BCG style', 'professional presentation', 'executive deck', 'strategy presentation', 'pitch deck', 'business deck', 'slidestart', or wants slides that look like they came from a top consulting firm. Also trigger when the user asks for presentations with frameworks (SWOT, Porter's Five Forces, etc.), data-heavy slides, or structured business content. This skill produces significantly better presentations than the default pptx skill for business/consulting contexts."
---

# SlideStart-Style Consulting Presentations

Create professional presentations that follow the design principles of top consulting firms (McKinsey, BCG, Bain) and the slide patterns curated by SlideStart / Analyst Academy.

## Before You Start

1. **Read the base pptx skill first**: Run `view /mnt/skills/public/pptx/SKILL.md` — this skill extends it.
2. **Read the pptxgenjs reference**: Run `view /mnt/skills/public/pptx/pptxgenjs.md` — you'll need it for code.
3. **Read the slide types reference**: Run `view` on this skill's `references/slide-types.md` for layout blueprints.
4. **Read the design system reference**: Run `view` on this skill's `references/design-system.md` for color, typography and consulting design rules.

## Core Philosophy: The Pyramid Principle

Every slide must follow the Pyramid Principle — the communication framework used by McKinsey, BCG, and Bain:

1. **Title = Main Point** — The slide title is an *action title* (a complete sentence stating the insight or conclusion, NOT a topic label). Bad: "Revenue Overview". Good: "Revenue grew 23% YoY driven by expansion into APAC markets".
2. **Subtitles = Key Arguments** — 2-3 supporting arguments that directly back the title claim.
3. **Body = Evidence** — Charts, data, callouts, and text that prove each argument.

The audience should be able to read just the slide titles in sequence and understand the full story of the presentation (the "title test").

## Presentation Architecture: SCQA Framework

Structure the overall deck using the SCQA storytelling framework:

1. **Title Slide** — Clean, bold, minimal.
2. **Situation** — "Here is the current state" (1-2 slides).
3. **Complication** — "Here is the problem / change" (1-2 slides).
4. **Question** — Implicit or explicit: "What should we do?" (often a divider slide).
5. **Answer** — The bulk of the deck: recommendations, analysis, frameworks, data (5-15+ slides).
6. **Next Steps / Appendix** — Action items, timeline, additional data.

If the user provides a simpler brief (e.g., "make me a deck about X"), still apply this structure to organize their content logically.

## Slide Type Selection

For each slide in the deck, choose the most appropriate slide type from the consulting slide taxonomy. **Read `references/slide-types.md`** for full layout blueprints. The available types are:

| Type | When to Use |
|------|-------------|
| **Title** | Opening/closing slides, section dividers |
| **Agenda** | Table of contents, meeting structure |
| **Header Horizontal** | Key message + supporting visual side-by-side |
| **Header Vertical** | Title banner + content below (most common layout) |
| **Pillar** | 2-4 parallel categories or strategic pillars |
| **Boxed** | Grid of content blocks with equal emphasis |
| **Framework** | 2x2 matrices, SWOT, Porter's, etc. |
| **Linear Flow** | Processes, timelines, step sequences |
| **Vertical Flow** | Top-down hierarchies, waterfall logic |
| **Single Chart** | One chart + insight callout |
| **Multiple Chart** | 2-3 charts showing related metrics |
| **Mixed Chart** | Chart + text analysis side-by-side |
| **Table** | Comparison data, scorecards, feature matrices |
| **Diagram** | Org charts, system architectures, relationships |
| **Image** | Full or half-bleed photo with overlay text |
| **Text Only** | Executive summary, key quotes (use sparingly) |
| **Divider** | Section separators within the deck |

**Critical rule: Never repeat the same layout for consecutive slides.** Vary your slide types to keep the audience engaged.

## Workflow

1. **Understand the brief** — Ask for topic, audience, desired length, and key messages if not provided.
2. **Storyboard** — Plan the deck structure using SCQA. List each slide with: number, type, action title, key content.
3. **Select design system** — Pick a color palette and typography from `references/design-system.md` that matches the topic and audience.
4. **Build slides** — Follow the pptxgenjs reference for code. For each slide, consult the layout blueprint in `references/slide-types.md`.
5. **QA** — Follow the QA process from the base pptx skill. This is mandatory.

## Key Design Rules (Quick Reference)

- **Action titles always**: Complete sentence stating the insight, not a topic label
- **One message per slide**: If you have two messages, make two slides
- **Every slide needs a visual element**: Chart, icon, shape, or image — text-only is last resort
- **Bold the important parts**: Key numbers, conclusions, and terms should be bold
- **Source everything**: Add a small source line at the bottom of data slides
- **Consistent formatting**: Same margins, fonts, colors, spacing across ALL slides
- **White space is good**: Don't fill every inch — breathing room improves clarity
- **Left-align body text**: Only center titles. Never center paragraphs or bullets.
- **NEVER use accent lines under titles**: This is a hallmark of AI-generated slides

## Output

Always output a `.pptx` file to `/mnt/user-data/outputs/` and present it to the user.
