---
name: find-media
description: Find, vet, license-check and use diagrams, photos, micrographs, 3D models, simulations and videos (including specific YouTube recommendations) for learning — or draw the figure yourself when nothing good exists.
---

# Find Media

Media earns its place when it shows something words cannot: spatial layout, a process unfolding, a structure in 3D, a real specimen, a quantity changing. It wastes time — or harms learning — when it is decoration, when it is wrong, or when watching replaces doing. This skill covers what to show, where to get it legally, how to check it, and how to make the learner use it actively.

Evidence tags: **Strong**, **Moderate**, **Weak**, **Craft** (as in **memory-hooks**). Source table with URLs and licenses: [media-sources.md](../../references/media-sources.md).

## 0. Rules that override everything else

1. **Every recommendation must exist.** Verify by search or fetch before naming it. Give the exact title, channel or creator, and URL. Never invent a video, figure number, timestamp or license.
2. **License before use.** Record title, author, source and license (TASL) for anything placed in an artifact. "Found on Google Images" is not a license.
3. **Accuracy before beauty.** Check labels, arrows, scale and terminology against the course or a reference. A pretty wrong diagram teaches the error.
4. **Media follows an attempt or prepares one.** It never replaces retrieval and practice.
5. **Course materials stay private.** Use figures from a learner's textbook or slides only in their private study, only when they supplied them, and never publish them.

## 1. When media helps (Mayer's principles)

Mayer's cognitive theory of multimedia learning (Mayer, *Multimedia Learning*, 3rd ed., Cambridge, 2021) is the working model: limited visual and verbal channels, active integration. Principles most relevant here (Moderate–Strong, mostly short lab lessons; effects shrink for experts):

- **Multimedia:** words + relevant pictures beat words alone for novices.
- **Coherence:** cut interesting-but-irrelevant material. Seductive details hurt learning: Sundararajan & Adesope (2020, *Educ Psychol Rev* 32:707–734), meta-analysis of 58 studies, >7,500 students; worse when the distractor sits next to a relevant diagram or stays on screen.
- **Signaling:** highlight what matters (arrows, color for the one changing quantity, headings).
- **Spatial and temporal contiguity:** labels on the figure, not in a legend; narration in sync with the animation.
- **Segmenting:** learner-paced chunks beat one continuous stream.
- **Pre-training:** teach the names and parts before the process animation.
- **Redundancy:** do not read on-screen text aloud word for word over a busy graphic.
- **Expertise reversal:** scaffolds that help novices can slow experts. Strip labels and guidance as the learner improves.

Pick the medium by what must be seen:

| Need | Best medium |
| --- | --- |
| Spatial relationships, 3D anatomy, molecular shape | 3D model or multiple labeled views; physical model kit for stereochemistry |
| Real appearance (tissue section, gross specimen, mineral, manuscript, artifact) | Photograph or micrograph with scale bar and stain named |
| Process over time (action potential, mechanism, orbit) | Short animation or simulation the learner can pause, step, and change |
| Relationships among quantities | Interactive graph (Desmos, GeoGebra, PhET) the learner manipulates |
| Classification and structure of an argument or pathway | Diagram the learner builds or completes |
| Expert reasoning aloud (problem solving, clinical case) | Short worked-example video, then a parallel problem |

## 2. Where to search

Start from sources that state a license and have editorial review. Full table, URLs, licenses and caveats: [media-sources.md](../../references/media-sources.md). Summary:

- **Openly licensed, reusable with attribution (check per item):** Wikimedia Commons (MediaSearch has a license filter; licenses vary per file and Wikimedia does not warrant them); Openverse (aggregator; states it does **not** verify licenses); Servier Medical Art (CC BY 4.0); NIH BioArt Source (per-item: public domain or CC BY); PhET simulations (historical collection CC BY 4.0 with a required attribution line; terms changed for sims published after 2026-03-29); Smithsonian Open Access (CC0); RCSB PDB (data CC0; Molecule of the Month and PDB-101 CC BY 4.0).
- **Open but NonCommercial–ShareAlike:** OpenStax (now CC BY-NC-SA 4.0 across the library; some older editions were CC BY — check the book's license page; third-party images inside may differ); LibreTexts (license varies per page, some "not declared"); Radiopaedia (CC BY-NC-SA 3.0); Michigan Histology (CC BY-NC-SA 4.0; commercial AI training explicitly prohibited); ChemTube3D (CC BY-NC-SA 2.0 UK).
- **Free to view, mixed terms:** NCBI Bookshelf (per-book copyright; embedded figures may be third-party "reprinted with permission"); HHMI BioInteractive (per-resource terms in each "Details" section); MolView, Desmos, GeoGebra (free tools; GeoGebra is non-commercial unless licensed).
- **Proprietary — link, don't copy:** Kenhub (private use only; images licensable separately), TeachMeAnatomy (copies for your own educational needs only), Visible Body (subscription), BioRender (free plan: no publishing figures; standalone redistribution of its icons prohibited on all plans).

Search moves:
- Use the discipline's term plus the view: "nephron diagram labeled SVG", "simple cuboidal epithelium H&E 40x", "SN2 animation".
- Filter by license first (Commons, Openverse), then judge quality.
- For structures, search by PDB ID or molecule name in RCSB and PubChem; for 3D small molecules, MolView or ChemTube3D.
- For histology, use a virtual microscope (Michigan Histology) so the learner pans and zooms, not a single cropped image.

## 3. Vet before use

Check every item against this list:

1. **Exists and loads** at the URL you will give. Record retrieval date.
2. **License** read on the item's own page, not inferred from the site's home page. Record TASL: *Title*, *Author*, *Source* (URL), *License* (with link). Template: "*Title*, by *Author*, *Source URL*, *License* (linked)" — fill it only from fields read on the file page.
3. **Accuracy:** labels point to the right structure; arrows show the right direction (curved arrows start at electrons); scale bars and stains stated; terminology matches the course (e.g., 2,3-BPG vs 2,3-DPG; Terminologia Anatomica vs eponyms); no outdated taxonomy (five-kingdom posters, "Protista" as a single clade) or retracted models.
4. **Level and convention:** matches the course (MCAT vs upper-level biochem; IUPAC vs common names; sign conventions in physics).
5. **Clutter:** cut or crop decoration (coherence). Prefer SVG you can edit.
6. **Accessibility:** alt text that describes what the figure shows; color is never the only code; captions on video.

**Hotlinking:** do not hotlink images into labs or saved pages — URLs break and images change. Download, store beside the artifact, and record the source and license. Exception: embed players (YouTube, PhET, Desmos) by their official embed method.

**Copyrighted textbook figures:** never place them in public artifacts. In a private study session, use only figures the learner supplied, and do not redistribute them. Make an original figure instead when the learner needs something to share.

## 4. Quiz images: mask completely

When a figure becomes a quiz ("label structure 3"):
- Remove or cover every label, leader-line text, legend entry and caption that reveals the answer.
- Rename the file (`fig-07.png`, not `left-ventricle.png`); strip title/alt text that names the answer; replace alt text with a neutral description ("Coronal section of heart, structure marked 3").
- Check SVG source text and `<title>` elements, image metadata, and nearby captions.
- One occluded label per card (see **flashcards**); keep the rest visible only if they do not give it away by elimination.

## 5. Make the figure yourself

Generate when no licensed figure is accurate, when the available ones are cluttered, when you need a blank or masked version, or when the learner should see the exact case from their problem. Often better, because it can show only what matters.

- **SVG** for anatomy schematics, cell diagrams, mechanisms with curved arrows, free-body diagrams. Hand-authored SVG is editable and maskable.
- **Mermaid** for flowcharts, pathways, decision trees, argument maps, timelines.
- **matplotlib (or similar)** for plots from real equations or data: Michaelis–Menten curves with and without inhibitor, titration curves, kinematics graphs, dose–response.
- **Desmos/GeoGebra** links when the learner should drag a parameter.
- **RDKit/SMILES-based** structure drawings for molecules when available; verify stereochemistry.

Rules: label your figure "schematic, not to scale" when it is; verify it as you would any source; have the learner draw it next time (drawing from memory is retrieval).

## 6. Videos and YouTube recommendations

Video is best for watching an expert reason or a process move. It is weakest as a substitute for practice. Brame (2016, *CBE—Life Sci Educ* 15:es6) summarizes: keep it short, signal key points, segment, and add interactivity (guiding questions, pause points). In MOOC logs, engagement dropped sharply beyond about six minutes (Guo, Kim & Rubin 2014, *Proc. ACM Learning@Scale*: observational, engagement not learning).

### Search and verify
1. Search for the **specific concept at the course's level**, e.g., "Chad's Prep E2 elimination", "Ninja Nerd cardiac action potential".
2. **Confirm the video exists:** fetch or search the page; record exact title, channel, URL, upload date, length.
3. **Check accuracy** by watching or reading the transcript/description for the part you will assign, against the course source. If you cannot inspect it, say so: "Not reviewed by me; check against your notes."
4. **Check fit:** level, notation, and convention (e.g., Na⁺/K⁺ stoichiometry, IUPAC names, sign conventions); date (pre-2015 MCAT content may be misaligned with the current outline); length; captions; paywall.
5. **Prefer a specific video over "watch channel X."** Give a timestamp range when you have verified one ("6:10–11:30: the inhibitor graphs"). Never guess timestamps.
6. **Recommend 1–3, not ten.** Say why each one.

### Place it correctly
- **Pre-training:** a short video for names and parts *before* a hard session.
- **After a first attempt:** learner tries a problem, then watches the worked solution, then does a parallel problem unaided.
- **Never as passive substitute** for retrieval or practice.

### Active viewing protocol (give this to the learner)
1. Before playing: write one question the video should answer.
2. **Pause-predict** at each step: "What's the next arrow / next sign / next stage?" then play.
3. After: close it, write or say the key steps from memory, then check.
4. Do one new problem without the video.

### Starter channels (verified 2026-10-06: channel exists, recent upload date checked via channel feed)

**Staleness rule:** this list ages. If today is more than ~90 days after the verification date, re-check a channel (exists, still active, still accurate) before recommending it, and always verify the specific video this session.

Channels are starting points; vet the specific video. Free YouTube; many have paid companion sites.

**Biology, physiology, medicine**
- **Ninja Nerd** (youtube.com/@NinjaNerdOfficial) — long, whiteboard lectures across physiology, anatomy, pathology; active. Caveat: long; assign segments.
- **Khan Academy Medicine / MCAT** (youtube.com/@khanacademymedicine) — MCAT-aligned basics. Caveat: last upload 2021; check against the current AAMC outline.
- **Osmosis from Elsevier** (youtube.com/@osmosis) — concise illustrated disease and physiology overviews; active. Caveat: YouTube videos are a subset; full library and question bank are paid.
- **Armando Hasudungan** (youtube.com/@ArmandoHasudungan) — hand-drawn physiology, pathology and pharmacology; active. Caveat: medical-school framing; check level.
- **CrashCourse** (youtube.com/@crashcourse) — Anatomy & Physiology playlist (49 episodes) and Biology series. Caveat: fast survey-level; not exam-depth.
- **Amoeba Sisters** (youtube.com/@AmoebaSisters) — intro biology, clear analogies; active. Caveat: intro/high-school level.
- **Dirty Medicine** (youtube.com/@DirtyMedicine) — USMLE-style high-yield facts and mnemonics. Caveat: exam-targeted; audit mnemonics (see **memory-hooks**), not for first-pass understanding.

**Chemistry and organic chemistry**
- **Leah4sci** (youtube.com/@Leah4sci) — organic chemistry and MCAT strategy; active. Caveat: MCAT-strategy videos are test-specific; use the concept videos for coursework.
- **The Organic Chemistry Tutor** (youtube.com/@TheOrganicChemistryTutor) — enormous library of worked problems in chemistry, physics, math. Caveat: procedure-heavy, light on why; last upload March 2026.
- **Chad's Prep** (youtube.com/@ChadsPrep) — full general chemistry, organic chemistry, physics and MCAT courses; active. Caveat: a paid companion site holds additional practice.
- **Professor Dave Explains** (youtube.com/@ProfessorDaveExplains) — short tutorials across chemistry, biology, physics, math. Caveat: the channel also posts combative debunking videos; assign tutorials specifically.

**Physics**
- **Flipping Physics** (youtube.com/@FlippingPhysics) — AP and intro physics with clear problem setups; active.
- **Michel van Biezen** (youtube.com/@MichelvanBiezen) — thousands of short worked problems in physics and math. Caveat: last upload January 2025; style is procedure-first.
- **Physics Girl** (youtube.com/@physicsgirl) — conceptual phenomena and demonstrations; uploading again in 2026. Caveat: enrichment, not course-aligned.
- **MIT OpenCourseWare** (youtube.com/@mitocw; ocw.mit.edu) — full lectures; for intro mechanics use **8.01SC Classical Mechanics, Fall 2016** (Chakrabarty, Dourmashkin et al.). Note: in December 2014 MIT removed Walter Lewin's lectures from OCW and edX after finding he had engaged in online sexual harassment of a learner, and revoked his emeritus title; copies of his older 8.01 lectures circulate elsewhere. Present this factually if asked; recommend the MIT-maintained course.

**Math and calculus**
- **3Blue1Brown** — *Essence of calculus* playlist (12 videos; youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr): geometric intuition. Caveat: intuition, not drill; pair with problems.
- **Professor Leonard** (youtube.com/@ProfessorLeonard) — full-length lecture courses, e.g., *Calculus 1 (Full Length Videos)* (playlist PLF797E961509B4EB5); active. Caveat: lectures run long.
- **Khan Academy** (youtube.com/@khanacademy; khanacademy.org) — short videos with practice exercises on the site; active.

**Philosophy and theology** (present theology sources as traditions, not neutral authorities)
- **CrashCourse Philosophy** (playlist, 47 episodes) — broad survey. Caveat: survey-level; read the primary text.
- **Kane B** (youtube.com/@KaneB) — careful lectures on analytic philosophy topics (metaphysics, epistemology, philosophy of religion); active.
- **Wireless Philosophy / Wi-Phi** (youtube.com/@WirelessPhilosophy) — short animated explainers by academic philosophers. Caveat: last upload 2023; wi-phi.com had an expired TLS certificate when checked — link the YouTube channel.
- **BibleProject** (youtube.com/@BibleProject) — animated book overviews and biblical themes; non-denominational nonprofit with a Protestant (evangelical) background; active. Caveat: one interpretive tradition; compare with critical and other confessional scholarship on contested points.
- **Bishop Robert Barron / Word on Fire** (youtube.com/@BishopBarron) — Roman Catholic commentary and sermons; active.
- **Ligonier Ministries** (youtube.com/@Ligonier) — Reformed Protestant teaching (founded by R.C. Sproul); active.
- **Open Yale Courses** (oyc.yale.edu; youtube.com/@YaleCourses) — full university lectures, including religious studies, philosophy, history, and sciences.

When teaching theology, say which tradition a source speaks from, pair sources across traditions on contested points, and keep primary texts central.

## 6b. Show it now (during live teaching)

In a tutoring session, a figure is a teaching move, not a deliverable:
1. Find one vetted figure (or draw a quick SVG/Mermaid/ASCII sketch) that shows the single relationship you're teaching.
2. Show it inline if the platform renders images or widgets; otherwise give a direct link with the figure number and what to look at ("Figure 22.20 — look only at the dashed curve").
3. Ask one question about it ("Where on this curve does exercising muscle sit?"). Hide or cover labels you're about to quiz.
4. Licensing still applies to anything you embed in a saved or shared artifact; a link for private study is fine.

In voice mode, describe the figure in words and offer to send it in text.

## 7. Anti-patterns

- Naming a video, figure or license you have not verified.
- "Watch this channel" with no specific video, or a list of ten.
- Assigning a video in place of retrieval or practice; ending a session with a video.
- Hotlinking images that will break; copying proprietary atlas images into public artifacts.
- Using a course textbook figure in anything shared.
- Quiz images that leak the answer through filename, alt text, caption or a neighboring label.
- Decorative stock images, memes and jokes beside key diagrams (seductive details).
- Trusting an aggregator's license label without opening the source page.
- Generated figures presented as if to scale, or with arrows and labels unchecked.
