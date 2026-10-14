---
name: study-plan
description: "Use when the user has an exam or assignment deadline and asks what to study or when, wants a study schedule or cram triage, or asks for study reminders."
---

# Study Plan

A plan is only as good as the hours it fits into. Compute real time, rank by what the exam rewards and what the learner can't yet do, schedule retrieval (not rereading), space it, and protect sleep. Then say plainly what won't fit.

Paths like `references/…`, `skills/…` and `templates/…` are relative to the Myelinate root (two folders up in the repository or plugin; this skill's own folder in a standalone install). If a file is missing, fetch it from `https://raw.githubusercontent.com/baney75/myelinate/main/`.

**Stand down when it isn't wanted.** If memory or the person says not to use Myelinate for this subject or kind of request, skip this skill's method and answer plainly; a slash command brings it back.

## 1. Inputs

- **Scope**: study guide / objectives (confirmed) or inferred list (label it). From `tutor`'s course map, or `teach`'s curriculum for self-directed learners.
- **Exam**: date and time, format, weight in the course, allowed materials.
- **Real hours**: hours they can actually study per day until the exam — ask, don't assume. Subtract classes, work, sleep (7–9 h), commute, other exams.
- **Current state per target**: from a quick check (5–15 mixed items) or tracked states — Not checked / Needs support / Independent this session / Retrieved after delay / Transferred. Self-ratings are a weak signal; prefer a quick check.

## 2. Rank

Priority ≈ **exam weight × gap × prerequisite leverage**.
1. Needs support on heavily tested targets
2. Not checked on heavily tested targets (check fast)
3. Prerequisites that unlock several targets
4. Needs support on light targets
5. Independent-this-session items due for delayed retrieval
Drop or skim: lightly tested, already retrieved-after-delay, or costly-to-learn-for-one-question items. Say what you dropped and why.

## 3. Schedule rules (evidence)

- **Retrieval over rereading.** Practice testing and distributed practice are "high utility"; rereading and highlighting "low" (Dunlosky et al. 2013).
- **Successive relearning**: reach 3 correct recalls per item in session 1, then relearn to 1 correct recall in each of 3+ later sessions spaced ≥ a day apart (Rawson & Dunlosky 2011).
- **Spacing scales with the horizon**: the optimal gap was about 20–40% of a 1-week test delay and about 5–10% of a 1-year delay (Cepeda et al. 2008). For an exam in 7 days, review at about days 1, 3, 6; in 30 days, about 1, 4, 10, 20, 28; with no deadline, the default ladder ~1 → 3 → 7 → 14 → 30 days. These are starting heuristics; adjust to errors.
- **Interleave** confusable types once basics are in place (Brunmair & Richter 2019).
- **Pretest** each new block — even wrong guesses help later learning.
- **Match the exam format** in the final days (timed MCQ sets, drawings, practical stations, essay outlines).
- **Sleep**: sleep before learning supports encoding and after learning supports consolidation; don't trade sleep for a final cram. No all-nighters in the plan.
- **Blocks**: 25–50 min focused blocks, one active task per block, short breaks. A clear "next block" beats a perfect week grid.

## 4. Output

Use `templates/study-plan.md`:
- Exam clock: "Exam Fri 10:00 — 3 days, ~11 study hours available."
- Ranked target list with state
- Day-by-day blocks: target → activity (tutor drill / lab section / problem set / flashcard review / mixed practice test) → check
- **Next block** (start now)
- **If time runs out, drop**: …
- **Won't be covered**: …
- Sleep and exam-morning plan (brief warm-up retrieval, no new material)

Calendar entries and reminders: see §4a. A suggested review date is not a reminder. Save the plan and topic states to memory (or the learner profile) so the next session picks up where this left off.

## 4a. Calendar and reminders (opt-in, no setup required)

Reminders turn a plan into something that happens. They're optional: offer once when a plan has dates, and only use a calendar the learner has connected (Google Calendar, Outlook or the device calendar through the assistant's connectors) or a scheduling tool the platform actually has.

- **What to add, with their OK:** exam dates and assignment due dates from the syllabus (for a class) or from a Claude-run course; spaced review sessions; study blocks they agreed to. Show the list first, then create, then read each event back to confirm it exists.
- **Add, never rearrange.** Create new events on a calendar they choose; never edit or delete existing events unless asked.
- **Earlier personal deadlines, by agreement.** If they've told you, or the record shows, that work tends to land at the last minute, offer a personal deadline a few days before the real one ("Draft due to yourself Tuesday; real deadline Friday"), labeled clearly as personal so it's never confused with the course's date. Say it plainly and kindly; it's a planning tool, not a judgment. Keep it only if it helps: ask after a couple of deadlines whether it did.
- **Keep the record honest.** If a reminder couldn't be created, say so. If dates came from a syllabus you inferred rather than read, mark them "check against your syllabus."
- Save the deadlines and the early-deadline preference to memory (with their OK the first time) so later plans use them.

## 5. Re-plan

After each session, update states from actual unassisted results and re-rank. If they fall behind, cut scope, not sleep. Final 24 h: mixed retrieval on high-weight items and confident-wrong areas; no new topics unless heavily tested and quick.

## Anti-patterns

Calendar hours instead of real hours · plans that are all reading · equal time per chapter · no "drop" list · all-nighters · planning more than doing (keep planning under ~10% of time) · promising a grade.
