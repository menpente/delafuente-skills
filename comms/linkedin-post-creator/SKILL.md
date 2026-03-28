---
name: linkedin-post-creator
description: Create high-engagement LinkedIn posts about AI/ML topics with companion infographic visuals. Use this skill whenever the user asks to write a LinkedIn post, draft social media content for LinkedIn, create thought leadership content, wants to share an AI/ML insight on LinkedIn, or mentions "LinkedIn", "post", "thought leadership", "social content", "hard-earned lesson", "positioning post", "contrarian take", or "practical breakdown". Also trigger when the user shares a technical idea or article and wants to turn it into a LinkedIn-friendly format.
---

# LinkedIn Post Creator

Create short, punchy, high-visibility LinkedIn posts on AI/ML topics. Every post comes with a companion infographic delivered as a downloadable PNG file (plus a React preview artifact and an AI image generation prompt).

## Core Philosophy

LinkedIn posts that convert into opportunities share these traits:
- They sound like a smart friend explaining something at lunch — not a professor giving a lecture
- They lead with tension or a strong opinion, not information
- They are scannable in 3 seconds
- Their companion image is so valuable people save it

The goal is not impressions. The goal is: **curiosity → conversations → opportunities**.

## Writing the Post

### Step 1: Choose a Post Type

If the user specifies a type, use it. If not, pick the most appropriate for their topic.

---

**Type 1: Hard-earned lesson** *(best for engagement + authority — use most often)*

Formula:
1. Open with the pain, mistake, or wasted effort
2. Deliver the counterintuitive insight
3. Close with a clear, practical takeaway

Example:
> I wasted €3k trying to run AI locally before realizing this:
>
> More compute ≠ better results.
>
> The real bottleneck was bad model choice, poor batching, zero observability.
>
> Hardware matters less than people think.
>
> If you're starting: don't overinvest in GPUs too early.
>
> What setup are you actually running right now?

---

**Type 2: Practical breakdown** *(structured value — use regularly)*

Formula:
1. Strong, opinionated hook (not neutral)
2. Structured list with clear tradeoffs — not just options
3. End with a rule or recommendation, not a summary

Key: More opinion, less neutral tone. Take a side.

Example:
> Most people choose the wrong hardware for local AI.
>
> Not because of budget — because they never defined the use case.
>
> 🍎 Mac Mini → learning / light inference
> 💻 RTX laptop → flexibility
> 🖥️ GPU desktop → serious workloads
> 🖧 Server → teams (and headaches)
>
> Rule: optimize for constraints, not power.
>
> What are you running?

---

**Type 3: Contrarian insight** *(best for reach — use sparingly, 1× per week)*

Formula:
1. Challenge a widely held belief directly
2. Reframe it in one or two lines
3. Keep it short and punchy — shorter than other types

Example:
> Hot take: running AI locally is overrated.
>
> For 80% of teams:
> → APIs are cheaper
> → faster to iterate
> → easier to maintain
>
> Local only wins when latency matters, privacy is critical, or you really know what you're doing.
>
> Most people just want to feel in control.
>
> Agree or disagree?

---

**Type 4: Positioning post** *(converts to consulting / recruiting — use once per week)*

Formula:
1. Name what you do in plain, concrete terms
2. List 2-3 recent, specific things you've worked on
3. Open the door without asking directly

Example:
> I help teams move from "AI experiments" → "AI in production".
>
> Recently I've been working on:
> — LLM evaluation pipelines
> — local vs cloud tradeoffs
> — reducing hallucination in production workflows
>
> If you're dealing with any of this, happy to exchange notes.

---

### Step 2: Apply the Non-Negotiable Rules

**1. First line = everything**

The first line decides if the post lives or dies. Test it: would someone stop mid-scroll for this?

❌ Weak: "You want to run AI locally…"
✅ Strong: "Most people waste money on AI hardware."

**2. Always add tension**

No tension = no engagement. Use words like:
- wrong, mistake, trap, wasted, failed, overrated, misunderstood

**3. One idea only**

If the post tries to cover two things, cut one. Save it for the next post.
Simpler = more engagement. Always.

**4. Specific CTA — never generic**

❌ "What do you think?"
✅ "What GPU are you actually using right now?"
✅ "What's the biggest bottleneck in your pipeline right now?"

The question must have an easy, concrete answer. Make it feel natural to reply.

**5. Opinion over neutrality**

Fence-sitting gets ignored. Take a side. A post that makes someone mildly disagree is better than one that makes everyone nod and scroll on.

**Language rules:**
- Write at a 3rd-to-5th grade reading level. If a 10-year-old wouldn't understand a sentence, rewrite it.
- Short sentences. Max 10-12 words per sentence. Many should be 5-7 words.
- One idea per sentence. One sentence per line.
- No jargon without a plain-English explanation right next to it.
- No filler words. Cut "just", "really", "very", "actually", "basically".
- Use "you" and "your" — talk TO the reader.

**Formatting rules:**
- Use blank lines between logical sections for scannability.
- No hashtags in the body. Add 3-5 hashtags as a separate block after the post.
- No emojis in the first line (they cheapen the hook). Max 2-3 emojis total, only if they add meaning.
- Bold or caps sparingly — only for one key phrase if needed.

### Step 3: Self-Check Before Delivering

Before showing the post, verify:
- [ ] Does the first line create immediate tension or curiosity?
- [ ] Does it contain at least one tension word (wrong / mistake / trap / wasted / overrated)?
- [ ] Is there one — and only one — idea in the post?
- [ ] Is the CTA specific enough that someone knows exactly what to answer?
- [ ] Does the post take a clear side, not sit on the fence?
- [ ] Would a 10-year-old understand every sentence?
- [ ] Is every sentence under 12 words?

If any check fails, rewrite before presenting.

## Creating the Infographic

Every post gets THREE image deliverables:

### Deliverable 1: Standalone HTML Infographic + React Preview

Create the infographic in TWO formats from the same design:

**A) Standalone HTML file** (`/home/claude/infographic.html`) — This is the source for PNG capture. It must be a complete, self-contained HTML document (DOCTYPE, html, head, body) with all styles inline. The `<body>` must have `width: 1080px; height: 1350px; overflow: hidden;`. Wrap the infographic content in a `<div id="root">` with the same dimensions. Do NOT use React, JSX, or any framework — pure HTML + inline CSS + inline SVG only.

**B) React artifact** (`.jsx` file in `/mnt/user-data/outputs/`) — The same visual design as the HTML, but as a React component for interactive preview in the chat UI. This is a nice-to-have preview; the PNG is the primary deliverable.

Both versions should render the same whiteboard-style, bold editorial infographic. The vibe is: someone sketched a brilliant explanation on a whiteboard, then a magazine designer made it gorgeous.

**Whiteboard foundation:**
- Background: Off-white/cream (#faf8f4) with a subtle square notebook grid (use CSS `linear-gradient` for horizontal + vertical lines at ~32px spacing, opacity ~0.13).
- Hand-drawn circles: Use organic SVG `<path>` elements for circled numbers — each circle should be slightly different, not perfect ellipses. Example: `M6 26 C5 12, 16 4, 26 4 C36 4, 44 11, 44 22 C44 34, 35 44, 24 44 C14 44, 5 38, 6 26Z`
- Arrows and connectors: SVG hand-drawn arrows between steps (slightly curved paths with arrowheads). These are essential — they make it feel like someone just drew this on a whiteboard.
- Rough underlines: Use double-stroke SVG paths under the title — one thick primary stroke, one thinner stroke underneath at lower opacity. NOT clean CSS wavy text-decoration.
- Step box borders: Solid (not dashed), with slightly asymmetric border-radius (e.g., `3px 8px 4px 6px`). Each step box should have a different radius pattern.

**Typography (two fonts):**
- Import from Google Fonts: `Caveat` (handwriting) + `DM Sans` (clean body).
- Use Caveat for: subtitle, labels, hints, ghost prices, footer — anything that should feel hand-written.
- Use DM Sans for: title (52px, bold 900, rotated -1deg), step titles, descriptions, takeaway text.
- Marker colors: red (#e63946), blue (#457b9d), teal (#2a9d8f), charcoal (#1d3557). These should feel like whiteboard markers.
- One key stat dramatically oversized (80-88px) with a hand-drawn circle around it (SVG path with organic border-radius, ~0.3 opacity).

**Layout principles:**
- Dimensions: 1080×1350px (portrait, LinkedIn-optimized).
- Slight rotations on every element: title (-1deg), steps (-0.3deg, +0.25deg, -0.2deg), takeaway (+0.3deg). Nothing should be perfectly straight.
- Ghost prices: Large Caveat text (48px) at very low opacity (0.15) on the right side of each step.
- Hand-drawn arrows between steps (centered, ~36px tall SVG).
- Scattered scribble decorations: spirals, zigzags, dashed circles, stars — as absolutely positioned SVGs at ~0.1 opacity. 3-4 of these scattered around the edges.
- NO tape effects, no torn paper. Keep it authentically whiteboard-like.

**Content density:**
- Pack enough value that people save/screenshot it.
- 3-5 key points as visual blocks connected by hand-drawn arrows.
- Each step: circled number + title + hint (Caveat) + description + result with check/X icon.
- A bottom takeaway section with a solid border box (asymmetric border-radius) containing a lightbulb icon + bold insight.
- Self-contained: someone should understand it WITHOUT reading the post.

### Deliverable 2: PNG File (Primary Visual Output)

After creating the standalone HTML infographic, capture it as a high-resolution PNG using the bundled Puppeteer script:

```bash
node /path/to/skill/scripts/capture-infographic.js /home/claude/infographic.html /mnt/user-data/outputs/infographic.png
```

The script:
- Launches headless Chrome (from `~/.cache/puppeteer/chrome/`)
- Renders the HTML at 1080×1350 with 2× device pixel ratio (final image: 2160×2700)
- Waits for font loading and layout stabilization
- Screenshots the `#root` element to PNG

**Font fallback note:** Google Fonts (Caveat, DM Sans) may not load in sandboxed environments. The design should look good with system fallback fonts (sans-serif, cursive). The typography hierarchy and marker colors carry the whiteboard aesthetic even without custom fonts.

Present the PNG using `present_files` — this is the file the user will upload to LinkedIn.

### Deliverable 3: AI Image Generation Prompt

Write a detailed prompt optimized for ChatGPT (DALL-E) or Gemini image generation. Structure:

```
[INFOGRAPHIC PROMPT]
Create a whiteboard-style educational infographic with bold editorial design:
- Style: Hand-drawn whiteboard sketch on cream/off-white background, with bold magazine typography
- Dimensions: 1080x1350 (portrait, LinkedIn-optimized)
- Marker colors: Red-orange, blue, and dark charcoal — like real whiteboard markers
- Title: "[Main insight in 3-5 words]" — large, bold, slightly tilted
- Content: [List 3-5 key points with hand-drawn arrows, circles, and connectors between them]
- Include: Sketchy icons (lightbulbs, arrows, checkmarks), circled numbers, underlined key phrases
- Bottom section: [Bold takeaway, underlined or boxed]
- Feel: Like a brilliant professor's whiteboard after an amazing lecture, but designed by a magazine art director
- Important: All text must be legible. Organic layout, not rigid grid.
```

## Output Format

Always deliver in this order:

1. **The LinkedIn post** — ready to copy-paste
2. **Hashtags** — 3-5 relevant hashtags as a separate block
3. **PNG infographic file** — captured from standalone HTML, presented via `present_files` (this is what the user uploads to LinkedIn)
4. **React infographic preview** — as an artifact for inline preview in the chat
5. **AI image generation prompt** — clearly labeled, ready to paste into ChatGPT or Gemini as an alternative

### PNG Generation Workflow

The step-by-step process for generating the PNG:

1. Write the infographic as a standalone HTML file at `/home/claude/infographic.html`
2. (Optional) Also create the React `.jsx` version for inline preview
3. Run the capture script:
   ```bash
   node <skill-dir>/scripts/capture-infographic.js /home/claude/infographic.html /mnt/user-data/outputs/<topic>-infographic.png
   ```
4. Verify the PNG was created: `ls -lh /mnt/user-data/outputs/<topic>-infographic.png`
5. Present the PNG to the user with `present_files`

## Example

**User input:** "I want to post about how RAG systems often fail because people don't chunk their documents properly"

**Post type selected:** Type 1 — Hard-earned lesson

**Output:**

---

Your RAG app gives wrong answers.

You blame the model.
The model is fine.

The real mistake? How you split your documents.

Bad chunks = bad retrieval.
Bad retrieval = bad answers.

Fix your chunking strategy first.
Everything else gets easier.

What's the biggest bottleneck in your RAG pipeline right now?

#RAG #LLM #AI #MachineLearning #DataEngineering

---

(Then the PNG infographic file + React preview artifact + AI image prompt follow)
