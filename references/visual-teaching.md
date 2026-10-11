# Show it: rendered visuals and interactive models in live teaching

Use this whenever a concept has shape: a structure in 3D, a spatial arrangement, a process that unfolds, a quantity that changes with another, a notation the learner must translate. In those cases a rendered picture the learner can operate teaches what a paragraph of description cannot. `tutor` and `teach` both use it in live sessions; `lab` builds the full standalone version; `find-media` supplies vetted figures and videos; `print` makes the paper version.

Source review: **2026-10-11**. Evidence tags as in `subject-playbooks.md`.

## Why

- **Words plus a relevant picture beat words alone for novices** (Mayer, *Multimedia Learning*, 3rd ed., 2021; principles summarized in `find-media` §1). **Moderate–Strong**, mostly short lab lessons; effects shrink with expertise.
- **Multiple representations help only when the learner can translate between them.** Ainsworth's DeFT framework (2006, *Learning and Instruction* 16(3):183–198, doi:10.1016/j.learninstruc.2006.03.001) explains why adding representations sometimes helps and sometimes overloads: the design, the function each representation serves, and the translation task the learner must perform all matter. **Craft/theory**, abstract reviewed. The practical rule: link the views explicitly, and make the learner do the translating.
- **3D models help organic chemistry students translate between 2D diagrams.** Feedback from concrete or virtual 3D models improved diagram-to-diagram translation over verbal feedback, the gain held at a 7-day delay, and the models did not become a crutch (Stull & Hegarty 2015, *Proc. Annual Meeting of the Cognitive Science Society* 37; abstract reviewed). **Moderate**, single study, conference proceedings. In anatomy, 3D visualization improved spatial and factual knowledge in a meta-analysis (Yammine & Violato 2015; see `subject-playbooks.md` §1).
- **Prediction before observation.** Watching without predicting teaches little (Crouch et al. 2004; see `lab` §0). A visual that shows the answer before the learner commits is a leak, not a scaffold.

## The rule

When the concept has shape, **default to rendering it rather than describing it.** Then ask one question about what's on the screen. It's a default, not a mandate: if this learner does better with a worked example, an analogy, talking it through or building it, lean there, and notice which route precedes their unassisted successes (`personalization.md`). Prose carries the teaching; the visual carries the structure; the learner carries the thinking.

Not everything needs a picture. Definitions, quick confirmations, pure procedure the learner already sees, and voice turns usually don't. A visual that isn't carrying the concept is decoration.

## Real images beat generated diagrams for complex anatomy

Hand-authored SVG is excellent for schematics: a circuit, a mechanism, a Newman projection, a pathway, a free-body diagram. It is not yet good enough for complex real-world structure. A generated drawing of a femur's bone markings, a skull's foramina, a brachial plexus or a histology slide is likely to be wrong in ways a novice can't catch, and a wrong figure teaches the error with authority.

For those, in this order:
1. **The learner's own course figures:** their textbook, lecture slides or lab manual, which also match what the exam shows. Ask for the figure or page; use it privately.
2. **Licensed real images and atlases:** photos, radiographs, micrographs and vetted illustrations from open sources (`find-media` §2; e.g., Wikimedia Commons, OpenStax, Radiopaedia, Michigan Histology), linked or embedded with attribution.
3. **3D models** from reputable sources for spatial relations.
4. **Your own SVG only for a schematic** that shows one relationship, labeled "schematic, not to scale."

For quizzing, mask labels on a real image (`find-media` §4) rather than drawing a new one.

## Pick the strongest format the platform supports

1. **Inline interactive widget** (an inline HTML/SVG tool, an artifact, a canvas) — first choice for anything the learner should manipulate.
2. **Inline static diagram** (SVG, rendered image) — for one relationship that doesn't need controls.
3. **A built page** (`lab`) — when they'll return to it, or it needs many steps and scoring.
4. **Mermaid, ASCII or a code block that draws the figure** — when nothing renders.
5. **A vetted link with what to look at** (`find-media` §6b) — when you can't draw it accurately.

In voice, describe the picture in words, then offer to send it in text.

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
| Chemistry | Glassware and reactions with rendered color changes, precipitates and gas evolution driven by the stoichiometry; spot-plate tests; flame tests |
| Earth and environmental science | Stream tables, a groundwater cutaway, a weather instrument station |
| Engineering and technology | Engines, gearboxes, pumps, valves and sensors taken apart and put back together, every number from the model |
| Measurement skills | Calipers, micrometers, dial gauges, graduated cylinders: read the scale, then check against the model's true value |

**2. Explain an abstract idea by a working object.** Some ideas have no natural picture: a cache, a rate limiter, a feedback loop, an equilibrium, a buffer. For those, invent a real, recognizable machine whose working *is* the concept, and let the learner operate it. A pin-tumbler lock that turns only when every pin matches teaches a cache key; a set of drawers each as deep as its bytes teaches memory layout. Either way, adapted for learning:
1. **Truth first.** Write the model before drawing: the real numbers, thresholds and behavior, in one small module that drives every part, readout and motion. A figure whose machine moves differently from the concept teaches the wrong thing.
2. **One-to-one mapping, said in one sentence:** what moves and what that motion means. For a working-object metaphor, say **where it breaks** (a lock has no eviction; a real cache does); unmarked analogies become misconceptions. For real apparatus, match the learner's actual equipment and procedure (their lab manual's glassware, volumes and steps), and say what the figure simplifies.
3. **Detail serves the mechanism.** Every part belongs to the machine and sits on another part; nothing is decoration. Exactly one part is lit or accented: the one the learner should watch. That's the signaling principle; detail that competes with it is a seductive detail and costs learning (`find-media` §1).
4. **The learner predicts before it moves.** The machine starts at rest; ask what will happen when they turn the knob; then let them turn it.
5. **A framed card:** figure number and a short title on top, the interaction hint and a live readout (computed from the model) at the bottom, the legend and a true caption underneath. Words stay out of the drawing.
6. **Calm, learner-driven motion:** time-based easing, responds to pointer and keyboard, an idle loop only when nobody's touching it, stops when offscreen, and goes still under reduced motion.
7. **Verify like a critic.** Render at desktop and phone width (390 px), in light and dark, at rest and at several moments of motion, and look at every image. Zoom in about 4× on every joint: every line ends on something, nothing passes through anything, nothing pops between frames.
8. **Size it honestly.** A crafted figure of this kind takes far longer than a live-turn diagram (the Anatomy skill sizes its smallest figures at 30–90 minutes). In a live session, use a quick linked diagram; build the crafted figure for a `lab`, a course or a study pack, and say how long it will take first.

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

- **Coordinates.** Build small molecules from ideal geometry (C–C 1.54 Å, C–H 1.09 Å, tetrahedral 109.5°, sp² 120°), or load a real conformer: PubChem 3D SDF for small molecules, RCSB PDB for macromolecules (license notes in `references/media-sources.md`).
- **Libraries.** three.js (cdnjs, with OrbitControls for drag and pinch) for ball-and-stick models you build yourself; 3Dmol.js for files from PubChem or the PDB. Load only from CDNs the platform allows.
- **Sync with the 2D views.** Drive the 3D geometry from the same state as the 2D drawing (a dihedral angle, a ring flip, an R/S choice). Animate the learner's change in 3D so they see the motion, not just the result.
- **Show the hidden atoms.** Skeletal drawings hide hydrogens and carbons. The 3D model shows them all; that is much of its value.
- **Fallback.** If WebGL or the library fails, say so on the page and keep the 2D views working.

## Videos alongside

When a short expert walkthrough would help, suggest one or two **verified** videos with exact title, channel and URL, and say when to watch: before the session for names and parts, or after their first attempt to compare reasoning (`find-media` §6). For a course, prefer videos that match the course's notation. Never replace the learner's own attempt with a video.

## Before you send a visual

- Numbers and structures checked against the key or a source.
- Labels use the course's names; nothing in a caption, legend or alt text gives away the answer you're about to ask for.
- Renders at phone width; controls reachable; works in light and dark mode.
- Model notes for any approximation.
- Your question is ready, and it asks for something they produce.

## Worked example: Newman projections (organic chemistry)

A learner understands Newman projections for butane but can't tell "what goes on top" once ethyl groups appear.

**The recipe** (teach in prose):
1. Pick the bond you sight down. The front carbon is the point where three bonds meet in the center; the back carbon is the circle, with bonds starting at the rim.
2. Inventory each carbon. Every carbon has four bonds; one is the sighted bond, so list the other three. Collapse everything beyond each carbon into one group label (H, CH₃, CH₂CH₃, CH(CH₃)₂). You never draw the inside of an ethyl group.
3. In a line drawing, every vertex and line end is a carbon, and any bond not shown is an H. The drawn zigzag is the all-anti conformation, so the chain pieces start 180° apart.
4. Top and bottom are a choice. Spinning the whole drawing changes nothing; by convention put the largest front group at 12 o'clock. Only the angles between groups matter: 180° anti, 60° gauche, 0° eclipsed.
5. Score a conformation by counting interactions (values below).

**The visual** (one linked widget): a molecule picker and a "sight down" bond picker; the line drawing with numbered carbons, the sighted bond in two colors and a dashed line-of-sight arrow; a ball-and-stick 3D model with Newman-view and side-view buttons; the Newman projection; controls for back carbon ±60°, spin drawing, flip view, back to zigzag; strain hidden behind "Show strain" until the learner predicts.

**The question:** "Try 2,3-dimethylbutane down C2–C3. Which staggered rotation is lowest in energy, and why? Predict before you reveal the strain."

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
| Physiology, biochemistry | Curves from real equations (O₂ saturation, Michaelis–Menten) with parameter sliders; pathway steppers, one step at a time |
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
- Unverified numbers, or an approximation presented as exact.
- A layout that breaks on a phone, or text that disappears in dark mode.
- Starting over from scratch when the learner asks for another view, instead of adding and linking it.
- A wall of explanation inside the widget, or no question after it.
