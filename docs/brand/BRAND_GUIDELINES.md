# Ai-Teech Brand Guidelines v1.0

## Brand foundation

- **Name:** Ai-Teech (UI wordmark: `ai-teech`)
- **Category:** AI-assisted learning and teacher intelligence
- **Positioning:** A playful, supportive learning companion that turns effort into evidence of understanding.
- **Audience:** Students (friendly/accessible) and teachers/schools (clear/trustworthy).
- **Tagline:** *Learn it. Prove it. Own it.*
- **Voice:** Curious, supportive, specific, unpretentious. Example: "Let's try the same idea in a new situation." Do not say "You're bad at this" or claim a model knows what a student thinks.

## Visual direction

Inspired by the two submitted Dribbble references: (1) soft cream dashboard with rounded functional cards, left rail, subtle highlight gradients and restrained charts; (2) expressive display serif with vivid playful accents. Adapted into a distinct Ai-Teech identity, not traced artwork.

| Token | Hex | Function |
|---|---|---|
| Ink | `#0C0C12` | Primary text, navigation, contrast |
| Paper | `#FFFDF5` | Main surface/background |
| Cloud | `#F6F4EE` | Secondary background |
| Learning Purple | `#BD47F2` | Brand accent, selected states |
| Spark Lime | `#91FE00` | Success highlights, learner progress (never sole signal) |
| Sunshine | `#FFE66D` | Friendly feature panels |
| Soft Iris | `#E8C8FF` | AI feedback surfaces |
| Warm Border | `#E6E2D7` | Cards and dividers |
| Error | `#BA3B4C` | Errors with text and icon |

Contrast rules: Ink on Paper for body. Never use Lime/Yellow as body text on light canvas. Check all critical pairings against WCAG AA; color alone must not convey correctness or mastery.

## Typography and spacing

- Display: `Source Serif 4`, fall back Georgia/serif. Use for large hero headings, brand communications, major empty states - not dense analytics.
- Product/UI: `Inter`, fall back system-ui. Math formulas use a compatible math renderer; Hindi localization uses `Noto Sans Devanagari`.
- Scale: 48/36/28/22/18/16/14px; body 16px with line-height 1.5. Minimum standard interactive target 44x44px.
- Radius: cards 20px, controls 12px, pills 999px. Spacing base 4px, common 8/12/16/24/32px.
- Motion: 120-220ms subtle feedback; honor reduced-motion setting. Avoid heavy animations in learning workflow.

## Logo creative brief

**Original symbol:** a stylized open book or library shelf arc embracing a simplified head-and-shoulders learner silhouette; one page edge forms a spark/idea. The symbol should read at 24px and work in one ink color. Rounded geometry is friendly but not childish.

Variants to draw: horizontal wordmark; icon-only app mark; monochrome; inverse; favicon. Clearspace >= height of the learner head; no distortion, gradients-only dependency, shadows or embedding a third-party logo/icon without license review.

Icon implementation can use a licensed icon library such as Lucide for *UI icons*, while the final logo must be a custom original vector mark. A generic person icon alone is not distinctive or advisable as a protected brand mark.

## Student UI vs teacher UI

- Student: motivating hero card, concept trail, one primary action, quiet explanations, warm illustrations, spaced-review badges.
- Teacher: dense but calm analytics, class filters, summary metrics, heatmap, misconceptions, intervention list and trend. Avoid decorative charts without actionable interpretation.
- Primary action label: "Practice this concept". Secondary: "Explain the idea". Feedback: "Your answer is correct; let's confirm it in a different case."

## Content and brand safety

- Avoid guaranteeing grades, diagnosing disability, or falsely calling uncertain mastery "verified".
- Label demo data and probabilistic AI inferences.
- Do not reuse the supplied Dribbble images in the public product, final logo or marketing without appropriate rights. Design is inspired by layout/palette, not copied assets.

## Design tokens starter

```css
:root {
  --ink: #0c0c12; --paper: #fffdf5; --cloud: #f6f4ee;
  --purple: #bd47f2; --lime: #91fe00; --sunshine: #ffe66d;
  --iris-soft: #e8c8ff; --border: #e6e2d7; --error: #ba3b4c;
  --radius-card: 20px; --radius-control: 12px;
  --font-ui: Inter, system-ui, sans-serif;
  --font-display: "Source Serif 4", Georgia, serif;
}
```
