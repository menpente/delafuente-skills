# Slide Types Reference

Detailed layout blueprints for each slide type in the consulting presentation taxonomy. These are inspired by real slides from McKinsey, BCG, Bain, Goldman Sachs, and other top firms as curated by SlideStart.

All coordinates assume `LAYOUT_16x9` (10" × 5.625").

---

## 1. Title Slide

The opening slide. Clean, confident, minimal. Sets the tone for the entire deck.

**Layout options:**

**A) Dark full-bleed** (most impactful)
- Background: dark color from palette (e.g., navy `1E2761`)
- Title: centered, 36-44pt, white, bold, positioned at y ~2.0
- Subtitle: centered, 16-18pt, light/muted color, y ~3.2
- Company/logo area: bottom-right or bottom-center, 10-12pt
- Optional: thin horizontal accent line (0.5pt) between title and subtitle

**B) Split layout**
- Left 60%: dark background with title text (white)
- Right 40%: accent color block or subtle geometric pattern
- Title left-aligned within the dark zone

**C) Minimal white**
- White background, title in primary dark color, centered
- Accent color shape (thin rectangle) at top or bottom edge
- Logo bottom-right

```
┌──────────────────────────────────┐
│            [dark bg]             │
│                                  │
│     PRESENTATION TITLE           │
│     Subtitle or tagline          │
│                                  │
│              Date | Author       │
└──────────────────────────────────┘
```

---

## 2. Agenda Slide

Lists the deck structure. Keeps the audience oriented.

**Layout:**
- Title at top: "Agenda" or "Contents" (24-28pt)
- Numbered items in a vertical list, left-aligned
- Active section highlighted with accent color or bold
- Each item: number (accent color, 20pt bold) + section name (16pt) + optional 1-line description (12pt, muted)
- Optional: right-side decorative shape or icon column

```
┌──────────────────────────────────┐
│ Agenda                           │
│──────────────────────────────────│
│ 01  Executive Summary            │
│ 02  Market Analysis         ◄──  │
│ 03  Strategic Options            │
│ 04  Financial Projections        │
│ 05  Recommendations              │
└──────────────────────────────────┘
```

**Code pattern:**
- Use a `for` loop to position items vertically with consistent spacing (~0.7" per item)
- Highlight current section with accent-colored rectangle behind the text or bold + accent color on the number

---

## 3. Header Horizontal (Two-Column)

The workhorse consulting slide. Action title at top, content split into two columns.

**Layout:**
- Action title: full width, top (y: 0.3, h: 0.7)
- Left column (x: 0.5, w: 4.2): text, bullets, or callout
- Right column (x: 5.3, w: 4.2): chart, image, or data visual
- Source line: bottom-left, 8-10pt, muted color

```
┌──────────────────────────────────┐
│ Action title (full sentence)     │
│──────────────────────────────────│
│ ┌─────────┐   ┌────────────┐    │
│ │  Text   │   │   Chart /  │    │
│ │  Bullets│   │   Visual   │    │
│ │  Detail │   │            │    │
│ └─────────┘   └────────────┘    │
│ Source: Company Report, 2024     │
└──────────────────────────────────┘
```

**Best practices:**
- Left column: 2-4 bullet points with bolded lead words
- Right column: chart, table, or key stat callout
- Keep columns visually balanced — neither side should be heavier than the other

---

## 4. Header Vertical

Title banner at top, content fills the lower 70-80%. The most flexible consulting layout.

**Layout:**
- Title zone: top 20% (colored background strip or bold title at top)
- Content zone: below, full width — can contain any combination of text, charts, tables
- Subtitle row: optional, 14-16pt, directly below title

```
┌──────────────────────────────────┐
│ ████ ACTION TITLE █████████████  │
│ Subtitle or key context line     │
│──────────────────────────────────│
│                                  │
│         [Content Area]           │
│    Charts / Tables / Text        │
│                                  │
│ Source: ...                       │
└──────────────────────────────────┘
```

---

## 5. Pillar Slide

Shows 2-4 parallel categories, strategic pillars, or options side by side.

**Layout:**
- Action title at top
- 2-4 equal-width columns below
- Each column: icon/number at top → bold header → description below
- Optional: colored rectangles or cards as background for each pillar
- Columns separated by vertical thin lines or whitespace

```
┌──────────────────────────────────┐
│ Action title                     │
│──────────────────────────────────│
│ ┌──────┐ ┌──────┐ ┌──────┐      │
│ │  01  │ │  02  │ │  03  │      │
│ │Pillar│ │Pillar│ │Pillar│      │
│ │ Name │ │ Name │ │ Name │      │
│ │ desc │ │ desc │ │ desc │      │
│ └──────┘ └──────┘ └──────┘      │
└──────────────────────────────────┘
```

**Code pattern:**
```javascript
const pillars = [...]; // array of { title, description, icon }
const colW = (9.0 - (pillars.length - 1) * 0.3) / pillars.length;
pillars.forEach((p, i) => {
  const x = 0.5 + i * (colW + 0.3);
  // Add card background, icon, title, description at calculated x
});
```

---

## 6. Boxed (Grid) Slide

2x2, 2x3, or 3x2 grid of content blocks with equal visual emphasis.

**Layout:**
- Action title at top
- Grid of rectangular cards below
- Each card: colored header strip or icon → title → 2-3 bullet points or a metric
- Consistent sizing — all cards must be identical dimensions

```
┌──────────────────────────────────┐
│ Action title                     │
│──────────────────────────────────│
│ ┌────────┐ ┌────────┐           │
│ │ Card 1 │ │ Card 2 │           │
│ │        │ │        │           │
│ ├────────┤ ├────────┤           │
│ │ Card 3 │ │ Card 4 │           │
│ │        │ │        │           │
│ └────────┘ └────────┘           │
└──────────────────────────────────┘
```

**Design rules:**
- Cards should have a subtle shadow or border to create visual separation
- Use the accent color for card headers or top-edge stripes
- Body text inside cards: 12-14pt
- Header text inside cards: 16-18pt bold

---

## 7. Framework Slide

2x2 matrix, SWOT analysis, Porter's Five Forces, or any strategic framework.

**Layout for 2x2 Matrix:**
- Action title at top
- Axes drawn with thin lines (1pt, muted color) — horizontal and vertical
- Axis labels at ends (12pt, muted)
- Quadrant labels: 14-16pt bold, positioned at center of each quadrant
- Content in each quadrant: bullets or data points (12pt)

```
┌──────────────────────────────────┐
│ Action title                     │
│──────────────────────────────────│
│           High ▲                 │
│    ┌────────┼────────┐           │
│    │  Q1    │  Q2    │           │
│ ───┼────────┼────────┼───►       │
│    │  Q3    │  Q4    │  High     │
│    └────────┼────────┘           │
│           Low                    │
└──────────────────────────────────┘
```

**Layout for SWOT:**
- 2x2 grid with colored backgrounds: green (Strengths), blue (Weaknesses), orange (Opportunities), red (Threats)
- Each quadrant: bold label + 3-5 bullets
- Quadrant colors at 85-90% transparency for readability

---

## 8. Linear Flow (Process / Timeline)

Horizontal process flow, timeline, or step sequence.

**Layout:**
- Action title at top
- 3-6 steps arranged horizontally
- Each step: numbered circle/shape → label → optional description below
- Arrows or connector lines between steps
- Active or highlighted step can use the accent color

```
┌──────────────────────────────────┐
│ Action title                     │
│──────────────────────────────────│
│                                  │
│  ①───→ ②───→ ③───→ ④───→ ⑤     │
│  Step  Step  Step  Step  Step    │
│  desc  desc  desc  desc  desc    │
│                                  │
└──────────────────────────────────┘
```

**Code pattern:**
- Calculate step positions: `x = startX + i * stepWidth`
- Use OVALs or ROUNDED_RECTANGLEs for step nodes
- Draw arrows with LINE shapes between nodes
- Add text below each node for descriptions

---

## 9. Vertical Flow

Top-down hierarchy, waterfall logic, or funnel.

**Layout:**
- Action title at top
- 3-5 items stacked vertically
- Each item: colored rectangle → text inside
- Arrows pointing downward between items
- Progressive narrowing for funnels

```
┌──────────────────────────────────┐
│ Action title                     │
│──────────────────────────────────│
│      ┌─────────────┐            │
│      │   Phase 1   │            │
│      └──────┬──────┘            │
│             ▼                    │
│      ┌─────────────┐            │
│      │   Phase 2   │            │
│      └──────┬──────┘            │
│             ▼                    │
│      ┌─────────────┐            │
│      │   Phase 3   │            │
│      └─────────────┘            │
└──────────────────────────────────┘
```

---

## 10. Single Chart Slide

One chart occupying most of the slide with an insight callout.

**Layout:**
- Action title at top (the insight the chart supports)
- Chart: occupies ~70% of slide area
- Insight callout: a small box (accent color border) with 1-2 sentences highlighting the key takeaway
- Source line: bottom

**Best practices:**
- Choose the right chart type: bar for comparison, line for trends, pie only for composition (max 5 slices), waterfall for deltas
- Remove chartjunk: no gridlines unless essential, no 3D effects, muted axis labels
- Use accent color to highlight the key data point

---

## 11. Multiple Chart Slide

2-3 small charts showing related metrics.

**Layout:**
- Action title at top
- 2-3 charts arranged horizontally (equal width)
- Each chart has its own small subtitle (14pt bold)
- Consistent axis scales across charts where possible

---

## 12. Mixed Chart Slide

Chart on one side, text analysis on the other. Very common in consulting.

**Layout:**
- Action title at top
- Left: chart (55% width)
- Right: text analysis with bolded key findings (45% width)
- OR: chart top, key insights box below

This is essentially a Header Horizontal where the right column is a chart.

---

## 13. Table Slide

Comparison data, scorecards, or feature matrices.

**Layout:**
- Action title at top
- Table centered, with ample margins
- Header row: dark background, white text, bold
- Alternating row shading for readability (very subtle: white / off-white)
- Key cells highlighted with accent color background or bold text

**Design rules:**
- Max 6-7 columns to avoid cramping
- Use icons (checkmarks, x marks) instead of text where possible
- Right-align numeric data, left-align text

---

## 14. Diagram Slide

Org charts, system architectures, Venn diagrams, relationship maps.

**Layout:**
- Action title at top
- Diagram centered in the content zone
- Use shapes (rectangles, ovals, arrows) to build the structure
- Keep it simple — max 8-10 nodes
- Use color to encode hierarchy levels or categories

---

## 15. Image Slide

Photography-driven slide for emotional impact.

**Layout options:**

**A) Full-bleed image** — image covers entire slide, text overlay in a semi-transparent box
**B) Half-bleed** — image covers left or right 50%, text on the other half
**C) Framed** — image in center with border/margin, text above or below

Use sparingly. Images should reinforce, not decorate.

---

## 16. Divider Slide

Section separator. Signals a topic change.

**Layout:**
- Dark or accent-colored background
- Section number: large (60-80pt), accent color or white
- Section title: 28-36pt, bold, white
- Optional: 1-line subtitle (16pt, muted)

```
┌──────────────────────────────────┐
│          [dark bg]               │
│                                  │
│            02                    │
│     MARKET ANALYSIS              │
│     Understanding the landscape  │
│                                  │
└──────────────────────────────────┘
```

---

## 17. Text Only Slide

Executive summary, key quotes, or purely textual insights. **Use sparingly.**

**Layout:**
- Action title at top
- 3-5 bullet points, each with a bolded lead sentence and 1-2 lines of detail
- Or: large quote (24pt, italic) with attribution
- Add visual interest: accent-colored left border on each bullet block, or numbered items

**Rule: Even text-only slides benefit from visual structure.** Use cards, colored sidebars, numbered circles, or indent levels to break up the wall of text.
