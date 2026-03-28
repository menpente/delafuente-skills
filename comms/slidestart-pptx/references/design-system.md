# Design System Reference

Consulting-grade design rules for professional presentations. These rules are derived from analyzing thousands of real slides from McKinsey, BCG, Bain, Goldman Sachs, Google, and other top organizations, as curated by SlideStart and Analyst Academy.

---

## Color Palettes

Choose a palette that matches the topic and audience. **Do not default to generic blue.** Each palette below includes a primary (dominant, 60%), secondary (supporting, 30%), and accent (highlight, 10%).

### Professional / Corporate

| Name | Primary | Secondary | Accent | Best For |
|------|---------|-----------|--------|----------|
| **McKinsey Navy** | `003B5C` (deep navy) | `F5F5F5` (off-white) | `0077B6` (bright blue) | Strategy, executive reports |
| **BCG Green** | `006845` (forest green) | `FFFFFF` (white) | `8DC63F` (lime) | Market analysis, growth |
| **Bain Red** | `CC0000` (Bain red) | `F7F7F7` (light gray) | `333333` (charcoal) | Recommendations, bold claims |
| **Goldman Slate** | `2C3E50` (dark slate) | `ECF0F1` (cloud) | `E67E22` (amber) | Financial analysis |
| **Midnight Executive** | `1E2761` (midnight) | `CADCFC` (ice blue) | `FFFFFF` (white) | Board presentations |

### Modern / Tech

| Name | Primary | Secondary | Accent | Best For |
|------|---------|-----------|--------|----------|
| **Teal Trust** | `028090` (teal) | `00A896` (seafoam) | `F0F3BD` (lemon) | Tech strategy, SaaS |
| **Charcoal Minimal** | `36454F` (charcoal) | `F2F2F2` (off-white) | `FF6B6B` (coral) | Product presentations |
| **Indigo Data** | `3D5A80` (indigo) | `98C1D9` (sky) | `EE6C4D` (salmon) | Data/analytics decks |
| **Dark Mode** | `1A1A2E` (near-black) | `16213E` (dark blue) | `0F3460` (navy) + `E94560` (hot pink) | Innovation, AI/ML |

### Warm / Creative

| Name | Primary | Secondary | Accent | Best For |
|------|---------|-----------|--------|----------|
| **Warm Terracotta** | `B85042` (terracotta) | `E7E8D1` (sand) | `A7BEAE` (sage) | Culture, HR, brand |
| **Berry & Cream** | `6D2E46` (berry) | `A26769` (dusty rose) | `ECE2D0` (cream) | Marketing, customer |
| **Sage Calm** | `84B59F` (sage) | `69A297` (eucalyptus) | `50808E` (slate) | Sustainability, ESG |
| **Coral Energy** | `F96167` (coral) | `F9E795` (gold) | `2F3C7E` (navy) | Pitch decks, startups |

### How to Apply

- **Slide backgrounds**: Alternate between white/off-white (content slides) and dark primary (title, divider, closing)
- **Title text on dark bg**: White or light secondary
- **Title text on light bg**: Primary or charcoal
- **Body text**: Always dark (`333333` or `2C3E50`) on light backgrounds
- **Accent color**: Used for key numbers, highlighted data, action items, icons, chart emphasis
- **Charts**: Primary color for main series, secondary for comparison, accent for highlight

---

## Typography

### Font Pairings

Pick one pairing and use it consistently throughout the entire deck.

| Pair | Header Font | Body Font | Personality |
|------|-------------|-----------|-------------|
| **Classic Consulting** | Georgia | Calibri | Traditional, authoritative |
| **Clean Modern** | Calibri | Calibri Light | Clean, approachable |
| **Bold Impact** | Arial Black | Arial | Strong, direct |
| **Editorial** | Cambria | Calibri | Thoughtful, structured |
| **Tech Forward** | Trebuchet MS | Calibri | Modern, digital-first |
| **Elegant** | Palatino | Garamond | Refined, premium |
| **Code-Aware** | Consolas | Calibri | Technical, data-heavy |

### Size Hierarchy

Maintain strict size hierarchy — the difference between levels should be unmistakable.

| Element | Size | Style | Notes |
|---------|------|-------|-------|
| Slide action title | 20-24pt | Bold, primary or dark color | Full sentence — the slide's main point |
| Section subtitle | 16-18pt | Bold, primary color | Below the title, introduces content zones |
| Body text | 12-14pt | Regular, dark gray | Left-aligned. Never center body text. |
| Bullet lead words | 12-14pt | Bold | First 2-4 words of each bullet bolded |
| Callout / big number | 48-72pt | Bold, accent color | Hero metrics that need to pop |
| Caption / source | 8-10pt | Regular, muted gray (`999999`) | Bottom of slide — sources, footnotes |
| Card header | 14-16pt | Bold, white on accent bg | Inside content cards/boxes |
| Card body | 11-13pt | Regular | Inside content cards/boxes |

### Why Action Titles (Not Topic Titles)

Consulting firms write titles that are complete sentences stating the insight:

| Bad (Topic Title) | Good (Action Title) |
|--------------------|---------------------|
| Revenue Overview | Revenue grew 23% YoY, driven by APAC expansion |
| Customer Satisfaction | Customer NPS improved to 72, highest in 5 years |
| Market Size | The addressable market is projected to reach $4.2B by 2028 |
| Competitive Landscape | Company X leads with 35% market share but faces margin pressure |
| Recommendations | We recommend three priority investments totaling $12M |

**The title test**: Read all slide titles in sequence. If the story makes sense without seeing any body content, the titles are good.

---

## Spacing & Layout Rules

### Margins
- **Outer margin**: 0.5" from all slide edges — nothing should be closer
- **Title zone**: y: 0.3, height: ~0.6-0.8"
- **Content zone**: starts at y: 1.2-1.4
- **Source line**: y: 5.2-5.4 (near bottom)

### Gaps
- **Between content blocks**: 0.3" minimum
- **Between columns**: 0.3-0.5"
- **Between a title and content**: 0.3-0.5"
- **Between bullet items**: use `paraSpaceAfter: 6` (not `lineSpacing`)

### Alignment
- **Title**: left-aligned (x: 0.5) — consulting style is almost always left-aligned, not centered
- **Body text**: always left-aligned
- **Only center**: slide titles on Title/Divider slides, big callout numbers
- **Columns**: align tops of columns precisely

---

## Visual Elements

### Icons
- Use react-icons (Font Awesome, Material Design, Heroicons) rasterized to PNG via sharp
- Standard icon size: 0.4-0.5" on slide
- Place icons in colored circles (accent color bg, white icon) for consulting style
- Use consistently — if one bullet has an icon, all bullets need icons

### Cards / Boxes
- Use RECTANGLE shapes with subtle shadow for card-style layouts
- Card fill: white (`FFFFFF`)
- Shadow: `{ type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.10 }`
- Optional: accent-colored left border strip (0.08" wide rectangle)
- **NEVER use ROUNDED_RECTANGLE with accent borders** — corners won't align

### Charts
- **Always match the presentation palette** — use `chartColors` to override defaults
- **Remove chartjunk**: hide gridlines unless essential, use `style: "none"` on catGridLine
- **Data labels > legends**: put values on the bars/lines, remove legend if only one series
- **Muted axis labels**: use secondary/gray color, not black
- **Highlight the key data point** with the accent color

### Lines & Separators
- Title separator: thin horizontal line (0.5-1pt) in muted color, directly below title zone
- Column separator: thin vertical line between columns (optional, subtle)
- **NEVER place accent lines under titles** — this is a telltale sign of AI-generated slides

---

## Consulting-Specific Design Patterns

### Key Stat Callout
For emphasizing a single metric:
```
┌───────────────────┐
│   72%             │  ← 60-72pt, accent color, bold
│   Customer NPS    │  ← 14pt, muted
│   ▲ +12 pts YoY  │  ← 12pt, green if positive
└───────────────────┘
```

### Before / After Comparison
Two columns with contrasting headers:
- Left: "Current State" (muted bg)
- Right: "Target State" (accent bg)
- Matching bullet points on each side

### Harvey Ball Status Indicators
Use filled/empty circles to show completion status in tables:
- ● Full (filled circle) = Complete / Strong
- ◐ Half = In Progress / Moderate  
- ○ Empty = Not Started / Weak
Render these as text characters in table cells.

### RAG Status (Red/Amber/Green)
For project status slides:
- Red: `E74C3C`
- Amber: `F39C12`
- Green: `27AE60`
Small colored circles next to status items.

### Waterfall Chart
For showing how components add up to a total — very common in financial consulting slides. Use the BAR chart type with careful color coding for positive (green/blue) and negative (red) segments.

---

## Anti-Patterns (Never Do These)

1. **Topic titles** instead of action titles ("Revenue" instead of "Revenue grew 23%...")
2. **Centered body text** — always left-align
3. **Accent underlines on titles** — dead giveaway of AI slides
4. **Same layout repeated** — vary slide types across the deck
5. **Text-only slides with no visual structure** — add cards, numbers, icons
6. **Generic blue** — choose a palette that matches the topic
7. **Tiny text to fit more** — if it doesn't fit, split into two slides
8. **Decorative images** — every visual must support the message
9. **Missing sources** — always cite data origins
10. **Inconsistent formatting** — same fonts, colors, margins on every slide
