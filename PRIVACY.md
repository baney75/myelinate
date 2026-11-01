# Privacy

Effective 2026-11-01. Myelinate is an open-source set of instructions, templates and small local scripts for AI assistants. It is published by Donovan Baney under the MIT License.

**What Myelinate collects:** nothing. It has no server, account, analytics, tracking or telemetry, and the publisher receives no data from anyone who uses it.

**What stays on your device.** In Claude Code, two hook scripts run locally at session start. One prints a single routing line. The other reads `~/.myelinate/learner.json`, which exists only if you asked Myelinate to keep a study record, and prints which reviews are due. That record holds topics and review dates, never health or condition labels, and you can delete it at any time. Neither script uses the network.

**What your assistant does.** Myelinate runs inside an assistant you already use (Claude, ChatGPT, Codex or another). Your conversations, uploads, memory and any web searches the assistant makes are handled by that assistant's provider under its own privacy policy. Myelinate tells the assistant to keep course materials, notes and anything personal out of web searches, public files and shared links, and to ask before saving anything personal to memory.

**Fetching.** If an install is missing one of its own files, the assistant may download it from `raw.githubusercontent.com/baney75/myelinate`. That request goes to GitHub, under GitHub's privacy statement.

**Children.** Myelinate collects no data from anyone, including children. Learners under 18 should use it through an assistant and account their school or guardian permits.

**Changes and contact.** Changes to this policy are made in this file and recorded in the repository history. Questions: open an issue at https://github.com/baney75/myelinate/issues.
