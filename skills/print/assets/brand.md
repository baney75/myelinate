# Myelinate brand guide

Myelinate should look like a well-kept lab notebook from a good university press: cream paper, dark ink, one rust accent. It should feel calm, exact and warm, never like a glossy app.

## The mark

The mark is a nerve fiber (axon) with myelin segments. Two rust arcs hop from node to node, like a signal jumping between gaps, and together they spell a lowercase **m**.

| File | Use |
| --- | --- |
| `logo-mark.svg` | Mark on light backgrounds (ink + rust) |
| `logo-mark-dark.svg` | Mark on dark backgrounds (cream + light rust) |
| `logo.svg` / `logo-dark.svg` | Horizontal lockup: mark + outlined Newsreader wordmark |
| `favicon.svg` | Browser tab icon. It switches colors with `prefers-color-scheme`. |
| `favicon-32.png`, `apple-touch-icon.png` | Raster icons on a paper tile |
| `hero.svg` | README banner, 1280×480 |
| `social-preview.png` | GitHub social card, 1280×640 |

- Leave clear space around the mark equal to one myelin segment's height (about 20% of the mark).
- Keep the mark at 16px or larger. It is drawn to read at 16px, with heavier strokes in `favicon.svg`.
- Do not rotate it, outline it, put it in a gradient, add a glow, or recolor the arcs anything but the accent.
- The rust period in "Myelinate**.**" belongs to the wordmark. Keep it.

## Palette

| Token | Light | Dark | Role |
| --- | --- | --- | --- |
| `--paper` | `#f7f3e9` | `#0f1e24` | Page background |
| `--paper-raised` | `#fffcf5` | `#15282f` | Cards |
| `--paper-sunken` | `#efe8d8` | `#0b171c` | Wells, inline code |
| `--ink` | `#16313b` | `#ece6d8` | Text, mark body |
| `--muted` | `#4c6269` | `#a3b3b2` | Secondary text (AA on paper and cards) |
| `--rule` | `#e3dccb` | `#23383f` | Hairlines |
| `--rule-strong` | `#c9c1ad` | `#34505a` | Card borders |
| `--accent` | `#a54320` | `#e8835a` | Rust: arcs, the period, primary buttons, numerals |
| `--teal` | `#165d78` | `#7cc0d6` | Focus rings, "hinted" states |
| `--code-bg` | `#16313b` | `#0a1519` | Code blocks |
| Margin line | `#d6a78f` | rust at 28% | The notebook's red margin |

Use one accent per view. Rust marks what matters; it is not decoration. Body text is always `--ink` or `--muted`. Every text pair above meets WCAG AA (≥ 4.5:1).

## Type

| Role | Web (Google Fonts) | SVG / fallback stack |
| --- | --- | --- |
| Display & headings | **Newsreader** 400–600, optical size 6–72 | `Newsreader, Georgia, 'Times New Roman', serif` |
| Interface & body | **Inter** 400–700 | `Inter, 'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif` |
| Code & prompts | **JetBrains Mono** 400–500 | `'JetBrains Mono', ui-monospace, Menlo, Consolas, monospace` |

- Headlines use Newsreader at weight 500 with slightly tight tracking (−0.01 to −0.025em). Italics are for quotations and asides.
- Small labels are uppercase Inter 700 with wide tracking (0.12–0.16em).
- SVG text must stay real `<text>` and fit with the widest common fallback (DejaVu Serif/Sans). `logo.svg` is the exception: its wordmark is outlined, so it renders the same everywhere.

## Motifs

- **Notebook paper**: faint horizontal rules every 40px and a rust margin line. Use it in heroes and banners only.
- **The axon**: a line of myelin segments with rust hop arcs. Use it for routes, sequences and dividers.
- No grain, noise, gradients, glassmorphism, or animations that loop or play on their own. One gentle entrance is fine when `prefers-reduced-motion` allows it.

## Voice

Direct, warm, adult. Write like a good tutor talks to a capable student.

| Do | Don't |
| --- | --- |
| "Make a prediction first." | "Unlock your brain's full potential!" |
| "Its own effect on learning has not been established." | "Scientifically proven to boost grades." |
| "Asks how you learn: pace, chunk size, what's hard." | Name, guess at or label a learner's condition (one they choose to share is used, never labeled). |
| Cite the study, name its limits. | Turn one study into a universal law. |
| "Myelinate is a name, not a mechanism." | Claim the skill changes myelin or forces permanent memory. |
| "Not yet. Step 2 drops the coefficient. Check it again." | "Great job!" for a wrong answer, or giving in when the learner pushes back on a correct correction. |
| Short sentences, concrete verbs, plain numbers. | Hype, exclamation marks, emoji, "revolutionary", "supercharge". |
