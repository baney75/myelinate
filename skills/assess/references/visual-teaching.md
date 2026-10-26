# Show it: rendered visuals and interactive models in live teaching

Use this whenever a concept has shape: a structure in 3D, a spatial arrangement, a process that unfolds, a quantity that changes with another, a notation the learner must translate. In those cases a rendered picture the learner can operate teaches what a paragraph of description cannot. `tutor` and `teach` both use it in live sessions; `lab` builds the full standalone version; `find-media` supplies vetted figures and videos; `print` makes the paper version.

Source review: **2026-10-11**. Evidence tags as in `subject-playbooks.md`. The figure patterns below adapt ideas from Nico Bailon's [visual-explainer](https://github.com/nicobailon/visual-explainer); the root NOTICE.md carries the credit and license notice. Myelinate's wording and code are original.

## Three learning patterns

Use a quiet ground and one accent for the part the learner must inspect now. Each figure makes one claim, stated in a one-sentence caption. If a sentence merely names a visible part, put it beside that part as a label. Draw the path through parts instead of a term in a box. Every arrow gets a relationship verb. Give the same state a shape, position or pattern cue as well as color. Sketch a grid in ASCII before assigning coordinates; keep labels readable at 360 px. If the view needs more than about 12 nodes, begin with a 5 to 8 node overview and split the detail. For comparisons, repeat the same small diagram at the same scale, or toggle before and after in the same coordinates. Number callouts and end their leaders exactly on what they name. These are craft rules, not evidence that a learner learned; ask for an independent use afterward.

1. **Concept maps for retrieval.** Put concepts in nodes and a relationship verb on every link ("causes," "is a kind of," "inhibits"). Have the learner build the map or fill hidden nodes and link labels from memory. Ask them to justify a link, especially one that exposes a possible misconception. Do not hand over a finished map as a substitute for retrieval. An argument in history, a food web, and a software dependency graph can all use the same pattern.
2. **Mechanism and pathway diagrams.** For a circuit, reaction, historical cause, algorithm or biological pathway, show one step at a time. Start on the first step. Before each next step appears, ask the learner to predict what changes and commit an answer. Reveal one new part with one claim in its caption; every arrow says what one part does to the next. No autoplay. Name what the drawing leaves out or treats as fixed. Reduced-motion mode shows each revealed state without animation. A visual must not contain the answer to its current question in a caption, label, alt text or hidden preview.
3. **Step visuals for worked problems.** Show a worked example as frames: one operation and one claim per frame. Then fade later frames to blanks for the learner to complete. Compare each learner step with a worked key before giving a verdict; a plausible explanation is not automatically correct. Use a parallel example for graded work. After a reveal, ask for transfer to a new case so copying the frame is not counted as independent success.

For a small self-contained example, adapt `templates/visual-stepper.html`: it includes a prediction gate and a fill-in concept map. Replace its subject content and key, and check that no future answer appears before commitment.

## Why

- **Words plus a relevant picture beat words alone for novices** (Mayer, *Multimedia Learning*, 3rd ed., 2021; principles summarized in `find-media` §1). **Moderate to Strong**, mostly short lab lessons; effects shrink with expertise.
- **Multiple representations help only when the learner can translate between them.** Ainsworth's DeFT framework (2006, *Learning and Instruction* 16(3):183 to 198, doi:10.1016/j.learninstruc.2006.03.001) explains why adding representations sometimes helps and sometimes overloads: the design, the function each representation serves, and the translation task the learner must perform all matter. **Craft/theory**, abstract reviewed. The practical rule: link the views explicitly, and make the learner do the translating.
- **3D models help organic chemistry students translate between 2D diagrams.** Feedback from concrete or virtual 3D models improved diagram-to-diagram translation over verbal feedback, the gain held at a 7-day delay, and the models did not become a crutch (Stull & Hegarty 2015, *Proc. Annual Meeting of the Cognitive Science Society* 37; abstract reviewed). **Moderate**, single study, conference proceedings. In anatomy, 3D visualization improved spatial and factual knowledge in a meta-analysis (Yammine & Violato 2015; see `subject-playbooks.md` §1).
- **Prediction before observation.** Watching without predicting teaches little (Crouch et al. 2004; see `lab` §0). A visual that shows the answer before the learner commits is a leak, not a scaffold.

## The rule

When the concept has shape, **default to rendering it rather than describing it.** Then ask one question about what's on the screen. It's a default, not a mandate: if this learner does better with a worked example, an analogy, talking it through or building it, lean there, and notice which route precedes their unassisted successes (`personalization.md`). Prose carries the teaching; the visual carries the structure; the learner carries the thinking.

Not everything needs a picture. Definitions, quick confirmations, pure procedure the learner already sees, and voice turns usually don't. A visual that isn't carrying the concept is decoration.

## Choose the medium by what carries the lesson

Two kinds of concept need two kinds of picture.

- **Structure, process, mechanism, curve.** The lesson is in the relations: which part connects to which, what changes when a variable moves. An inline schematic carries it well if the assistant can render one (for example with `show_widget`). Otherwise provide a self-contained HTML file, inline SVG, Mermaid or an ASCII sketch, operable where the medium allows.
- **The image itself is the content.** The lesson hinges on what something looks like: an eye, a face, a hand, an anatomical structure, a painting, a literary or philosophical image. A flat schematic of these turns into icons, and an icon carries none of what the lesson needs. Use a crafted artifact page (shading, real proportions, a figure built and checked), a licensed real image, or a generated image you have inspected. Take the time it needs and say so.

**Worked example: the eye in *Alcibiades I* (132c to 133c).** Socrates asks how an eye could see itself. It looks into another eye, and in the pupil, the eye's best part, it sees its own image: the *korē*, the "little doll" (the same word means girl and pupil). So a soul knows itself by looking into another soul, at its best part, where wisdom is. The tiny human figure in the pupil *is* the lesson. A schematic of three rows (eye → pupil, soul → wisdom) restates the answer as boxes. An inline widget with an iris larger than the lids, a figure whose dot-eye sits where an ear would be, and an avatar glyph for the korē teaches nothing and looks broken. The right medium is a crafted page: an almond eye with the iris clipped to the lids, a dark pupil holding a small figure that reads as a person at a glance, and a viewer whose gaze line ends in that pupil. The reference build is `examples/alcibiades-eye.html` (screenshot beside it).

## Geometry, recognizability, and honesty in the frame

1. **Children stay inside their parents.** An iris sits inside the eye opening: draw the almond as a `clipPath` and clip the iris, pupil and highlight to it. Labels sit inside their panels; nothing pokes through a boundary it belongs behind.
2. **Lines end on the meaningful target.** A gaze line, ray, arrow or leader line ends on the thing it's about (the pupil, the focal point, the labeled structure), not on a corner or the panel edge.
3. **Figures are whole, attached and oriented.** A head sits on a neck on shoulders; the eye is on the face, on the side facing what it looks at; a profile looks toward its target.
4. **No icon stand-ins.** Never use a generic UI glyph (user avatar, frown or smile face, emoji-like marks, a stock "person" icon) for the image the lesson hinges on. If you can't draw it recognizably at display size, change the medium.
5. **No scorecards.** Readouts like "Image size: tiny" or "Clarity: small but clear" flatten an idea into a metric and invite the learner to read the card instead of the picture. Add a readout only when the number is the concept (a pH, an energy, a measured length).
6. **Look before you send.** If you have a browser, a headless renderer or a screenshot tool, render the visual and look at the image at the size the learner will see. Zoom on the joints and on the key image. If you have no way to render, say in one line that the figure is unrendered, so the learner knows to report what looks wrong. "Rendered and inspected" is a claim you make only after looking (router rule 16).

## Real images beat generated diagrams for complex anatomy

Hand-authored SVG is excellent for schematics: a circuit, a mechanism, a Newman projection, a pathway, a free-body diagram. It is not yet good enough for complex real-world structure. A generated drawing of a femur's bone markings, a skull's foramina, a brachial plexus or a histology slide is likely to be wrong in ways a novice can't catch, and a wrong figure teaches the error with authority.

For those, in this order:
1. **The learner's own course figures:** their textbook, lecture slides or lab manual, which also match what the exam shows. Ask for the figure or page; use it privately.
2. **Licensed real images and atlases:** photos, radiographs, micrographs and vetted illustrations from open sources (`find-media` §2; e.g., Wikimedia Commons, OpenStax, Radiopaedia, Michigan Histology), linked or embedded with attribution.
3. **3D models** from reputable sources for spatial relations.
4. **Your own SVG only for a schematic** that shows one relationship, labeled "schematic, not to scale."

For quizzing, mask labels on a real image (`find-media` §4) rather than drawing a new one.

## Pick the strongest format the platform supports

1. **Inline interactive widget** (an inline HTML/SVG tool, an artifact, a canvas): choose it first for anything the learner should manipulate.
2. **Inline static diagram** (SVG, rendered image): use it for one relationship that doesn't need controls.
3. **A built page** (`lab`): use it when they'll return to it or it needs many steps and scoring.
4. **Mermaid, ASCII or a code block that draws the figure**: use these when nothing else renders.
5. **A vetted link with what to look at** (`find-media` §6b): use it when you can't draw the figure accurately.

In voice, describe the picture in words, then offer to send it in text.

**Use the strongest available rendering capability.** If the assistant can show an inline widget (for example `show_widget` on claude.ai), read that tool's instructions if needed and show the visual alone. Keep the teaching and question in the reply. If the host offers an artifact or HTML file, use that next; otherwise draw the structure in Markdown, Mermaid or ASCII. A pasted instruction file still works without any tool.

## Build a live-turn widget

A live-turn widget has to load instantly, run anywhere, and teach one relationship. The reference is `examples/chair-flip.html`, about 140 lines that let a learner flip a cyclohexane chair and watch one methyl change from axial to equatorial. It shows the recipe:

1. **No libraries for small geometry.** A 2D canvas with a hand-rolled projection (yaw and pitch, then a painter's sort, far to near) draws a ball-and-stick molecule, vectors or a lattice in about 40 lines. It needs no CDN or WebGL, so nothing can fail to load. Use three.js or 3Dmol.js only for real structure files or large models.
2. **One state value drives everything.** The chair is a function of a single `t` from 0 (chair A) to 1 (chair B). Every atom, color and readout is computed from it, so the views can't disagree.
3. **Color encodes the rule.** Axial is one color and equatorial is another, and the color is recomputed from geometry every frame. Watching a hydrogen change color during the flip teaches "axial swaps with equatorial" without a caption.
4. **Light up only what matters, only when it matters.** The C3 and C5 hydrogens turn amber only when the methyl is axial, because those are what it bumps into. Everything else stays quiet.
5. **Three controls at most:** the variable being taught (Ring flip), an invariance control (move the methyl to the other face: up stays up), and Reset view. Rotation is by dragging, plus arrow keys.
6. **A live state readout that names the position, not the answer.** "Methyl is axial" helps the learner track; the energy comparison they're asked to predict stays out of the widget.
7. **Host theme and phone first.** Read colors from CSS variables (the host's tokens, or your own with a dark set), size the canvas to its container times `devicePixelRatio`, set `touch-action: none` on the canvas, and use 44 px buttons.
8. **Say what the model simplifies,** in a one-line note under it or in your reply. The chair morphs straight from one form to the other to show which position maps to which; the real path goes through half-chair and twist-boat forms.

The reply around the widget follows the usual rhythm: the few rules it illustrates, the caveat, a hands-on check if they have one (a model kit: build it, push the up carbon C1 down and the down carbon C4 up, and track one colored atom), and one question that makes them **operate** the widget and predict: "Set the methyl axial, then flip. Which conformer is lower in energy?" The amber hydrogens are the scaffold for their reason; don't name them in the question.

## Design rules for a teaching visual

1. **Start at the confusion.** Build the view that answers what they asked ("what goes on top?"), not a tour of the topic.
2. **Use the learner's notation and names.** Number atoms, label parts, and name axes the way their course or field does (C3, C4; Kₘ; the textbook's sign convention). If the course draws it a certain way, show that view first.
3. **Link representations; same color means same thing everywhere.** The line drawing, the Newman projection and the 3D model share one color for the front carbon and another for the back carbon. Changing one view updates all of them.
4. **Give them a control that moves the variable being taught.** A rotation button for conformations, a slider for pH, a step button for a mechanism. Learner-paced; never auto-play complex dynamics.
5. **Add an invariance control when the confusion is about what doesn't matter.** "Spin the whole drawing" or "flip the view" shows the learner that orientation is a choice while the relationship stays the same.
6. **Hide the answer until they commit.** Strain energies, product structures, labels being quizzed and their captions stay behind a reveal. Ask for the prediction first.
7. **Compute, don't eyeball.** Every number on the screen comes from a stated model or source. Label approximations plainly ("treats ethyl as equal to methyl, the usual intro-course approximation").
8. **Camera presets that match the 2D convention.** A 3D view needs a button for the textbook's standard view ("Newman view" looks down the bond; "chair view" from the side) plus free rotation.
9. **Small screens and both themes.** Many learners are on a phone: about 380 px wide, at most two columns of controls, 44 px tap targets, text at 12 px or larger, readable in light and dark mode.
10. **Prose outside the widget.** The visual holds labels and controls only. Explanations, the recipe and the question go in your reply.
11. **One question after it.** "Rotate the back carbon until the two biggest groups are anti. How many gauche interactions are left?" Not "does this help?"

## Crafted figures: real apparatus and working objects

Some figures earn more craft than a quick diagram: solid, shaded objects built from accurate parts, moving under the learner's hand, with light, water, flame or heat rendered by a physics model. The approach and the craft and verification rules below are adapted from Anatomy by Ryan (github.com/wheresryan22/anatomy, MIT), a figure-building skill for Claude whose examples include a school ripple tank driven by a wave and optics model and a dial gauge reading a sliding carriage. Use it two ways.

**1. Render the real apparatus or phenomenon.** When the learner will meet the thing itself, a faithful, operable figure prepares them for it:

| Field | Crafted figure |
| --- | --- |
| Lab preparation (any science) | The actual setup before lab day: a titration with buret, stopcock and meniscus read at eye level; a distillation with the thermometer bulb at the side arm; a spectrophotometer's light path; a micropipette's two stops. The learner assembles or operates it and predicts readings |
| Physics | Ripple tank interference, a pendulum or spring-mass rig with live energy readouts, optics benches with real ray paths, circuits on a breadboard with meters that read the model |
| Chemistry | Glassware and reactions with color changes, precipitates and gas evolution driven by the chemistry (indicator and pH, solubility, amounts); spot-plate tests; flame tests |
| Earth and environmental science | Stream tables, a groundwater cutaway, a weather instrument station |
| Engineering and technology | Engines, gearboxes, pumps, valves and sensors taken apart and put back together, every number from the model |
| Measurement skills | Calipers, micrometers, dial gauges, graduated cylinders: read the scale, then check against the model's true value |

**2. Explain an abstract idea by a working object.** Some ideas have no natural picture: a cache, a rate limiter, a feedback loop, an equilibrium, a buffer. For those, invent a real, recognizable machine whose working *is* the concept, and let the learner operate it. A pin-tumbler lock that turns only when every pin matches teaches a cache key; a set of drawers each as deep as its bytes teaches memory layout.

Both kinds of crafted figure follow these rules, adapted for learning:

1. **Truth first.** Write the model before drawing: the real numbers, thresholds and behavior, in one small module that drives every part, readout and motion. A figure whose machine moves differently from the concept teaches the wrong thing.
2. **One-to-one mapping, said in one sentence:** what moves and what that motion means. For a working-object metaphor, say **where it breaks** (a lock has no eviction; a real cache does); unmarked analogies become misconceptions. For real apparatus, match the learner's actual equipment and procedure (their lab manual's glassware, volumes and steps), and say what the figure simplifies.
3. **Detail serves the mechanism.** Every part belongs to the machine and sits on another part; nothing is decoration. Exactly one part is lit or accented: the one the learner should watch. That's the signaling principle; detail that competes with it is a seductive detail and costs learning (`find-media` §1).
4. **The learner predicts before it moves.** The machine starts at rest; ask what will happen when they turn the knob; then let them turn it.
5. **A framed card:** figure number and a short title on top, the interaction hint and a live readout (computed from the model) at the bottom, the legend and a true caption underneath. Words stay out of the drawing.
6. **Calm, learner-driven motion:** time-based easing, responds to pointer and keyboard, an idle loop only when nobody's touching it, stops when offscreen, and goes still under reduced motion.
7. **Verify like a critic.** Render at desktop and phone width (390 px), in light and dark, at rest and at several moments of motion, and look at every image. Zoom in about 4× on every joint: every line ends on something, nothing passes through anything, nothing pops between frames.
8. **Size it honestly.** A crafted figure of this kind takes far longer than a live-turn diagram (the Anatomy skill sizes its smallest figures at 30 to 90 minutes). In a live session, use a quick linked diagram; build the crafted figure for a `lab`, a course or a study pack, and say how long it will take first.
9. **Effects only where lines can't draw it.** Use a shader for light, water, flame, heat, glow or caustics, driven by the physical model, and keep the figure readable without it (some devices can't run WebGL).

If the **Anatomy** skill is installed (`npx skills add wheresryan22/anatomy`), use it to build these figures; its kit, shader layer, audits and capture scripts do the craft and verification above. Despite the name, it draws machines and apparatus, not human anatomy: for bodies, bones and tissues, use real images (above).

## Iterate toward the learner

When the learner says "try again" or asks for another view, read it as a missing translation step. Keep what worked, add the representation they asked for, and **link** it to the existing ones rather than starting over. A good escalation path:

1. A short recipe in prose plus one interactive view of the concept.
2. Add the representation they meet in class (the line drawing with numbered carbons) and draw the line of sight on it.
3. Add the 3D model, synced to both, with every hidden atom shown.

Each step keeps the controls and colors of the last, so the learner never has to relearn the interface.

## 3D models

Use 3D for stereochemistry, conformations, chair cyclohexanes, molecular geometry (VSEPR), crystal lattices, protein structure, anatomy, vectors and fields.

- **Coordinates.** Build small molecules from ideal geometry (C to C 1.54 Å, C to H 1.09 Å, tetrahedral 109.5°, sp² 120°), or load a real conformer: PubChem 3D SDF for small molecules, RCSB PDB for macromolecules (license notes in `references/media-sources.md`).
- **Libraries.** For a few dozen atoms in a live turn, use no library: a canvas projection (`examples/chair-flip.html`). three.js (cdnjs, with OrbitControls for drag and pinch) for larger ball-and-stick models you build yourself; 3Dmol.js for files from PubChem or the PDB. Load only from CDNs the platform allows.
- **Sync with the 2D views.** Drive the 3D geometry from the same state as the 2D drawing (a dihedral angle, a ring flip, an R/S choice). Animate the learner's change in 3D so they see the motion, not just the result.
- **Show the hidden atoms.** Skeletal drawings hide hydrogens and carbons. The 3D model shows them all; that is much of its value.
- **Fallback.** If WebGL or the library fails, say so on the page and keep the 2D views working.

## Videos alongside

When a short expert walkthrough would help, suggest one or two **verified** videos with exact title, channel and URL, and say when to watch: before the session for names and parts, or after their first attempt to compare reasoning (`find-media` §6). For a course, prefer videos that match the course's notation. Never replace the learner's own attempt with a video.

## Before you send a visual (under a minute)

1. **Medium:** is the image itself the content? Then it's a crafted page or a real image, not a flat schematic.
2. **Containment:** every child shape is inside its parent (iris inside the lids, labels inside panels).
3. **Targets:** every gaze line, ray and arrow ends on what it's about.
4. **Recognizable:** the key image reads as what it is at display size; no avatar, face or emoji glyph stands in for it.
5. **No leak, no scorecard:** nothing in the figure, caption, legend or alt text answers your question; no metric readouts unless the metric is the concept.
6. **Numbers and structures** checked against the key or a source; model notes for any approximation.
7. **Phone width and both themes;** controls reachable.
8. **Rendered and inspected,** or you've said it's unrendered.
9. **Your one question is ready,** and it asks for something they produce.

## Worked example: Newman projections (organic chemistry)

A learner understands Newman projections for butane but can't tell "what goes on top" once ethyl groups appear.

**The recipe** (teach in prose):
1. Pick the bond you sight down. The front carbon is the point where three bonds meet in the center; the back carbon is the circle, with bonds starting at the rim.
2. Inventory each carbon. Every carbon has four bonds; one is the sighted bond, so list the other three. Collapse everything beyond each carbon into one group label (H, CH₃, CH₂CH₃, CH(CH₃)₂). You never draw the inside of an ethyl group.
3. In a line drawing, every vertex and line end is a carbon, and any bond not shown is an H. The drawn zigzag is the all-anti conformation, so the chain pieces start 180° apart.
4. Top and bottom are a choice. Spinning the whole drawing changes nothing; by convention put the largest front group at 12 o'clock. Only the angles between groups matter: 180° anti, 60° gauche, 0° eclipsed.
5. Score a conformation by counting interactions (values below).

**The visual** (one linked widget): a molecule picker and a "sight down" bond picker; the line drawing with numbered carbons, the sighted bond in two colors and a dashed line-of-sight arrow; a ball-and-stick 3D model with Newman-view and side-view buttons; the Newman projection; controls for back carbon ±60°, spin drawing, flip view, back to zigzag; strain hidden behind "Show strain" until the learner predicts.

**The question:** "Try 2,3-dimethylbutane down C2 to C3. Which staggered rotation is lowest in energy, and why? Predict before you reveal the strain."

## Chemistry: what to render

| Topic | Render | Learner control |
| --- | --- | --- |
| Particle level (gen chem) | Beaker particle view beside the equation and graph (Johnstone's three levels) | Add solute, heat, change volume |
| Lewis structures, VSEPR | 2D Lewis structure linked to a 3D shape with lone pairs drawn | Add or remove a lone pair or bonded atom |
| Equilibrium, kinetics, titrations | Concentration-vs-time or pH-vs-volume curve from the real equation | Change K, temperature, amount added |
| Conformations | Line drawing ↔ Newman ↔ 3D, numbered atoms | Rotate ±60°, spin, flip, reset |
| Cyclohexane chairs | Chair drawing ↔ 3D chair, axial and equatorial marked | Ring flip; place a substituent axial or equatorial |
| Stereochemistry | Wedge-dash ↔ 3D ↔ Fischer; priorities numbered | Rotate the model; swap two groups and watch R/S invert |
| Mechanisms | Step-by-step arrow-pushing, one step per screen, formal charges shown | Step forward and back; learner places the next arrow before reveal |
| Energy diagrams | Reaction coordinate with intermediates and transition states | Change a substituent, watch the barrier move |
| Spectroscopy | Structure with each proton set colored to its NMR signal | Click a signal, highlight its protons |

**Conformational energy costs** for intro courses (OpenStax *Organic Chemistry*, Table 3.5, adapted from McMurry; checked 2026-10-11): H/H eclipsed 4.0 kJ/mol (1.0 kcal/mol); H/CH₃ eclipsed 6.0 (1.4); CH₃/CH₃ eclipsed 11.0 (2.6); CH₃/CH₃ gauche 3.8 (0.9). Butane: gauche 3.8 kJ/mol above anti; eclipsed CH₃/H 16; eclipsed CH₃/CH₃ 19. Treating ethyl and other alkyls like methyl is an approximation; say so. Use the course's table if it differs, and say which the exam uses.

## Other subjects: what to render

| Subject | Render |
| --- | --- |
| Physiology, biochemistry | Curves from real equations (O₂ saturation, Michaelis to Menten) with parameter sliders; pathway steppers, one step at a time |
| Anatomy, histology | Layer toggles from superficial to deep; cross-section linked to a 3D view; masked-label quiz mode |
| Genetics | Punnett and pedigree builders; meiosis stepper with chromosomes colored by origin |
| Physics | Free-body diagram linked to the motion graph; vector and field views with draggable charges |
| Calculus, math | Function graphs with sliders; secant-to-tangent zoom; area accumulation |
| Statistics | Sampling distributions built live from repeated samples; confidence intervals that miss |
| Programming | Memory and call-stack diagrams that step with the code |
| Philosophy, theology | Argument maps with premises, objections and replies; the learner places the missing premise |
| History | Timelines and maps with layers the learner turns on |
| Languages | Morphology tables and sentence diagrams; audio for pronunciation |

## Anti-patterns

- Describing a 3D structure in a paragraph when a model could be shown.
- A machine metaphor with no stated mapping or no word on where it breaks; a richly detailed figure with no single accented part to watch.
- A widget that reveals the answer before the learner predicts, or a caption that names the masked label.
- Representations that use different colors or names for the same thing, or aren't linked.
- Decorative animation, mascots, particles that encode nothing.
- A flat schematic for a subject whose image is the point; icon glyphs standing in for the key image; shapes poking through their parents; gaze lines ending beside the target.
- Scorecard readouts that reduce the idea to metrics.
- Sending a visual you could have rendered and didn't look at.
- Unverified numbers, or an approximation presented as exact.
- A layout that breaks on a phone, or text that disappears in dark mode.
- Starting over from scratch when the learner asks for another view, instead of adding and linking it.
- A wall of explanation inside the widget, or no question after it.
