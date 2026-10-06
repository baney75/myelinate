---
name: flashcards
description: Write high-quality spaced-repetition flashcards and export them for Quizlet, Anki, Obsidian, or in-chat drills. Use when someone asks for flashcards, a deck, cards, or review sets, or at the end of a lesson.
---

# Flashcards

Cards exist for **durable recall of what the learner already understands** — fast, reliable access to facts, terms, relationships and steps so working memory is free for reasoning. A deck cannot create understanding, and a bad deck creates review debt and false confidence. Few, sharp cards beat many vague ones.

Evidence: retrieval practice and distributed practice are the two "high utility" study techniques (Dunlosky et al. 2013); repeated retrieval beats restudy at a week (Roediger & Karpicke 2006); successive relearning — reach 3 correct recalls per item in the first session, then relearn to 1 correct recall in each of 3+ spaced sessions — raises college exam scores (Rawson & Dunlosky 2011; Rawson, Dunlosky & Sciartelli 2013). Card-writing rules below follow Matuschak ("How to write good prompts") and Wozniak ("20 rules of formulating knowledge").

## 0. Rules that override everything else

1. **Understand first, then card.** If the learner can't explain it, teach it (`tutor`) before carding it.
2. **One retrieval per card.** Atomic: one fact, one link, one step.
3. **Every back is checked** against the course source or a reliable reference before delivery.
4. **Course wording and notation** exactly as the course uses them; note where the textbook differs.
5. **Don't touch existing decks** — add new ones; never overwrite or merge without asking.

## 1. What makes a good prompt

- **Focused** — one detail. "Describe glycolysis" is twenty cards.
- **Precise** — one acceptable answer. Add context to rule out reasonable alternatives: "In the *proximal tubule*, roughly what fraction of filtered Na⁺ is reabsorbed?" → about two-thirds (~65%).
- **Consistent** — produces the same answer every review.
- **Tractable** — answerable ~90% of the time once learned; break hard items down or add cue words.
- **Effortful** — real retrieval. No yes/no. No front that gives the back away by pattern.
- **Short** — back ideally one line. A paragraph back is several cards.
- **No orphans** — each card serves an objective. Skip completionism.

## 2. Card types — mix them per concept

A concept deserves several angles; this is what turns cards into understanding scaffolds rather than trivia.

| Type | Front → Back example |
| --- | --- |
| Fact | Rate-limiting enzyme of glycolysis? → PFK-1 |
| Mechanism / why | Why does high ATP inhibit PFK-1? → ATP binds an allosteric site, lowering affinity for F6P (signals high energy charge) |
| Cause → effect | ↓pH: which way does the O₂–Hb curve shift? → right |
| Cause → effect | Right-shifted O₂–Hb curve: tissue O₂ unloading increases or decreases? → increases |
| Contrast | Competitive vs noncompetitive inhibitor: effect on Vmax? → unchanged vs decreased |
| Application | ↑PaCO₂, ↓pH, normal HCO₃⁻ at first: primary disorder? → acute respiratory acidosis |
| Procedure step | After writing the ICE table for a weak acid, next step? → write Ka in terms of x |
| Cloze (closed list/sequence) | Cranial nerve order: olfactory, optic, {{c1::oculomotor}}, trochlear… |
| Image occlusion | Masked structure on a diagram → its name (one mask per card) |
| Definition ↔ term | Reverse only when both directions are tested (vocab, drug ↔ class) |
| Hook-assisted | Target fact on the front/back; the mnemonic (`memory-hooks`) as an optional hint line on the back — never the answer itself |

**Interference control:** confusable pairs (SIADH/DI, SN1/SN2, mitosis/meiosis) get an explicit contrast card instead of two near-identical prompts.

**Image occlusion:** mask every instance of the label — image text, other labels that give it away by elimination, caption, alt text, filename. Use licensed or course-supplied images only (`find-media`).

## 3. How many and which

- Per lesson: typically 6–15 cards. Per exam: weight cards by the study guide, not by what's easy to card.
- Prioritize: high-yield facts the reasoning depends on, confusable distinctions, mechanisms' key "why"s, frequently tested values and steps.
- Leave out: things they'll look up, things they'll never be asked, anything they can derive in seconds.

## 4. Export formats

Ask which tool they use if unknown. Default: Quizlet-ready block + readable table. Sets over ~20 cards: also deliver a file (`.txt`/`.tsv`/`.md`) and state the count.

**Quizlet** (Import → "Between term and definition: Tab", "Between cards: New line"):
```
Rate-limiting enzyme of glycolysis	PFK-1
Effect of ↓pH on O₂–Hb curve	Shifts right; more O₂ unloaded to tissue
```
No tabs or line breaks inside a card. If a back needs a line break, use a custom card separator (e.g., `;;`) and say so.

**Anki** (File → Import; a plain-text file):
```
#separator:tab
#html:false
#tags column:3
Rate-limiting enzyme of glycolysis	PFK-1	BIOL126::Exam2::Metabolism
```
Cloze cards go in a separate file with `#notetype:Cloze` and text like `Hemoglobin's Hill coefficient is about {{c1::2.7}}`. Hierarchical tags `Course::Exam::Topic`.

**Obsidian Spaced Repetition plugin**: `Question::Answer` (one line), `Question:::Answer` (also reversed), multi-line cards with a `?` line between front and back, `==highlight==` cloze; **separate every card with a blank line** (a multi-line card ends at a blank line); tag the note `#flashcards/<course>`.

**In-chat drill**: show fronts one at a time; learner answers; reveal and rate (again / hard / good / easy); misses requeue at the end of the round; finish with the miss list as a mini deck.

**Inside a lab** (`lab`): built-in review with a stored schedule (e.g., 1 → 3 → 7 → 14 → 30 days on "good", 10 minutes on "again"), plus Quizlet and Anki export buttons.

## 5. Scheduling and use

- Encourage an SRS (Anki/FSRS, Quizlet's spaced mode, Obsidian SR) over massed review.
- First session: 3 correct recalls per card. Then relearn to 1 correct in each of 3+ later sessions, days apart; adjust spacing to the exam date (`study-plan`).
- Say aloud or write the answer before flipping — no "I knew that" self-grading.
- Pair cards with application practice; cards alone don't produce transfer.
- Retire or rewrite cards that fail repeatedly (usually too big, ambiguous, or not understood) — a leech is a teaching problem, not a discipline problem.

## 6. Quality check before delivering

- [ ] Every back verified against source; numbers and units correct
- [ ] Each card has exactly one answer; no yes/no; no giveaway fronts
- [ ] Mix includes why/contrast/application, not only facts
- [ ] No duplicates or near-duplicates; confusable pairs have contrast cards
- [ ] Format imports cleanly (one tab per line for Quizlet; headers for Anki)
- [ ] Count stated; tags/course labels applied

## Anti-patterns

Paragraph backs · yes/no cards · cards before understanding · copying slide bullets verbatim as cards · 300-card decks for a 4-chapter exam · mnemonic as the answer · ambiguous prompts that accept several answers · reverse cards by default · overwriting the learner's existing decks.
