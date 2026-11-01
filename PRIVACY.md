# Privacy

Effective 2026-11-01. Myelinate is an open-source set of instructions, templates and small local scripts for AI assistants. It is published by Donovan Baney under the MIT License.

**What Myelinate collects:** nothing. It has no server, account, analytics, tracking or telemetry, and the publisher receives no data from anyone who uses it.

**What stays on your device.** Everything Myelinate itself runs, reads or writes stays on your machine:

- *Session hooks (Claude Code only).* `hooks/route_hint.py` prints one routing line. `hooks/due_reviews.py` reads `~/.myelinate/learner.json` and prints which reviews are due. Neither uses the network.
- *Learner record.* `~/.myelinate/learner.json` exists only if you ask Myelinate to keep your progress. It holds topics, courses and review dates. Myelinate instructs the assistant never to put health or condition labels in it, but the file is plain text the assistant writes, so check it if that matters to you, and delete it any time.
- *Learner profile.* If you ask, the assistant gives you a profile (goals, what helps, what's due) to keep as a file wherever you choose, or saves those points to your assistant's memory (see below).
- *Printing.* `print` may run `scripts/make_pdf.py`, which opens a page the assistant made on your machine in your local headless Chromium and saves it as a PDF. If that page links to outside resources such as a web font or an image, Chromium loads them while rendering, as any browser would.

**What your assistant does.** Myelinate runs inside an assistant you already use (Claude, ChatGPT, Codex or another). Your conversations, uploads, memory and any web searches the assistant makes are handled by that assistant's provider under its own privacy policy. Myelinate tells the assistant to keep course materials, notes and anything personal out of web searches, public files and shared links, and to ask before saving anything personal to memory.

**Fetching.** If an install is missing one of its own files, the assistant may download it from `raw.githubusercontent.com/baney75/myelinate`. That request goes to GitHub, under GitHub's privacy statement.

**Children.** Myelinate collects no data from anyone, including children. Learners under 18 should use it through an assistant and account their school or guardian permits.

**Changes and contact.** Changes to this policy are made in this file and recorded in the repository history. Questions: open an issue at https://github.com/baney75/myelinate/issues.
