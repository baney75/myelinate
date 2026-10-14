---
name: course-project
description: "Use when the user wants a full structured course, or a course run as a Claude Project, built to university standard with syllabus, lessons, assignments and tests."
---

# Course project

Some goals are a whole course, not a conversation: software engineering, organic chemistry, a language, statistics for research. For those, build the course properly and give it a home. A Claude Project gives it one: its own instructions (the teacher), its own files (syllabus, lesson plan, gradebook), its own chats, and its own memory. The result should feel like a strong accredited course, sequenced and assessed like one, and more personal than any lecture hall.

Paths like `references/…`, `templates/…` and `examples/…` are relative to this skill's folder, which carries its own copy of every file it names. Other Myelinate skills are siblings (`../tutor/SKILL.md`) and are installed as their own skills too. If a file is missing from your copy, fetch it from `https://raw.githubusercontent.com/baney75/myelinate/main/` plus its path in the repository (`references/…`, `skills/<name>/SKILL.md`); if you can't fetch, work from this file and the router's core rules.

## 0. When to offer it

- In `teach`, when the goal needs more than a few sessions or the learner asks for "a course."
- When the learner wants structure: a schedule, assignments, tests, grades.
- Offer it in one line; don't push. Some people prefer to keep learning in their usual chats, and `teach` works there too.

## 1. Learn the learner (briefly)

Use memory and `references/first-session.md`: purpose (career, project, curiosity), the competence statement ("You'll be able to ___ without help"), prior knowledge (a short warm-up check), hours per week, deadline, what helps them learn, and tools they use. Don't gate the build on every answer.

## 2. Research the course like a curriculum committee

1. **Accredited syllabi.** Find at least three syllabi or course pages for the matching course from different accredited universities (for example MIT OpenCourseWare and other published university course pages). Record institution, course number, term, and the topic sequence. Prefer recent terms; note the date you checked.
2. **Discipline standards,** where one exists. Examples: ACM/IEEE-CS/AAAI *Computer Science Curricula 2023* (computing); IEEE Computer Society *SWEBOK* (software engineering); American Chemical Society Committee on Professional Training guidelines (chemistry); *Vision and Change* (undergraduate biology); ABET criteria (engineering programs); ACTFL Proficiency Guidelines (languages); the AAMC content outline (MCAT). Verify the current version before citing.
3. **Synthesize.** Topics that every syllabus covers are the core; topics in some are electives; order prerequisites before what depends on them. Note where the learner's purpose changes emphasis (a backend engineer needs databases early; a pre-med needs reaction mechanisms before spectroscopy).
4. **Primary resources:** one main text (open texts such as OpenStax or LibreTexts when they fit; check licenses), primary sources where the field values them, and one to three verified videos per unit at most (`find-media`).
5. **Be honest about the benchmark.** Say which syllabi and standards you used. The course matches their bar; it doesn't grant credit.

If your platform can run research subagents, fan the syllabus search out and verify the results; otherwise search sequentially. Never invent a syllabus, course number or standard.

## 3. Write the course files

Produce four files the learner keeps (as files or documents they can download):

1. **Syllabus** (`course-syllabus.md`): title; who it's for; competence statement and course outcomes; benchmark sources with dates; units in order, each with objectives, readings, activities, assignment and assessment; schedule against their real hours; grading scale and weights; bonus policy (`assess` §5); the course's AI policy ("your teacher won't hand you answers to assigned work"; `assignment`).
2. **Lesson plan** (`lesson-plan.md`): for every unit, lesson by lesson: target, hook question, minimum teaching, the worked example, the visual to render (`references/visual-teaching.md`), practice items, the check, and the spaced review items from earlier units.
3. **Gradebook and progress** (`templates/gradebook.md`): starts empty except the plan.
4. **Project instructions** (`templates/course-project-prompt.md` filled in): the teacher.

Before delivering, check the files against each other: every syllabus objective appears in the lesson plan and is assessed at least once.

## 4. The project instructions

Fill in `templates/course-project-prompt.md`. It tells the project's Claude to:
- Be the teacher of this course, at a university standard, for this learner.
- Follow the lesson plan in order, one lesson per session unless the learner asks to move faster, and keep their place.
- Open each session with retrieval of what's due; teach with Myelinate's session loop; render visuals when concepts have shape; close with the learner's own recall.
- Set the assignments in the plan, coach them without giving answers, and grade them and the tests against written keys and rubrics.
- Keep the gradebook current: use project memory if it's on; otherwise end each session with an updated progress block for the learner to replace in the project's files.
- Load Myelinate if installed, or fetch it from its GitHub link.

Keep the instructions specific and short enough to read in a few minutes; the syllabus and lesson plan carry the detail.

## 5. Set-up steps for the learner (Claude)

Checked against Claude's help center on **2026-10-11**; re-check if this date is old.
1. Open claude.ai/projects (or Projects in the sidebar) and choose **+ New Project**. The name and description are for the learner; Claude can't see them.
2. Choose **Set project instructions** and paste the instructions file.
3. In the project's knowledge panel, choose **+** and add the syllabus, lesson plan and gradebook.
4. Start a chat in the project: "Begin the course."

Notes: free accounts can create up to five projects. Memory is project-scoped and on by default on Free, Pro and Max (on Team and Enterprise it's off by default until an owner turns it on); a chat started with memory off neither uses nor adds to it. Chats in a project don't share context with each other except through memory and the project files, which is why the gradebook matters.

**Other assistants:** ChatGPT and Grok also have project features with instructions and files. The same instructions and files work there; check their current help pages for the steps.

## 6. Running and revising the course

Each session in the project runs as `teach` §5 describes. Every few units, review the gradebook with the learner and revise: speed up where they're strong, add practice where they're not, and update the files. When the course ends, give a final cumulative exam (`assess`), a capstone that meets the competence statement, and an honest summary of what they can now do.

## Anti-patterns

A syllabus from imagination instead of research · citing a standard you didn't check · a lesson plan that skips prerequisites · claiming credit or accreditation · instructions so long nobody reads them · no gradebook · files that disagree with each other.
